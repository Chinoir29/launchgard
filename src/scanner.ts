import * as fs from 'fs';
import { glob } from 'glob';
import {
  ScanOptions,
  Violation,
  ClaimLedgerEntry,
  RuleSet,
  Rule,
  ScanReport,
  ScanMode,
} from './types/index.js';
import { loadRules } from './rules/loader.js';
import { createHash } from 'crypto';

export class Scanner {
  private rules: RuleSet;
  private baseline: Map<string, Set<string>> = new Map();

  constructor(rulesPath?: string) {
    this.rules = loadRules(rulesPath);
  }

  async loadBaseline(baselineFile: string): Promise<void> {
    if (!fs.existsSync(baselineFile)) {
      return;
    }

    const content = fs.readFileSync(baselineFile, 'utf-8');
    const baseline = JSON.parse(content);

    for (const violation of baseline.violations) {
      const key = `${violation.file}:${violation.ruleId}:${violation.line}`;
      if (!this.baseline.has(key)) {
        this.baseline.set(key, new Set());
      }
      this.baseline.get(key)!.add(violation.hash);
    }
  }

  async scan(options: ScanOptions): Promise<ScanReport> {
    if (options.baselineFile) {
      await this.loadBaseline(options.baselineFile);
    }

    const files = await this.resolveFiles(options.files);
    const violations: Violation[] = [];
    const claimLedger: ClaimLedgerEntry[] = [];

    for (const file of files) {
      const content = fs.readFileSync(file, 'utf-8');
      const lines = content.split('\n');

      // Scan for violations
      violations.push(...this.scanFile(file, lines, options.mode));

      // Extract claims for ledger
      claimLedger.push(...this.extractClaims(file, lines));
    }

    // Filter out baselined violations
    const filteredViolations = violations.filter((v) => !this.isBaselined(v));

    // Sort for deterministic output
    filteredViolations.sort((a, b) => {
      if (a.file !== b.file) return a.file.localeCompare(b.file);
      if (a.line !== b.line) return a.line - b.line;
      return a.column - b.column;
    });

    claimLedger.sort((a, b) => {
      if (a.file !== b.file) return a.file.localeCompare(b.file);
      return a.line - b.line;
    });

    const errors = filteredViolations.filter((v) => v.severity === 'error').length;
    const warnings = filteredViolations.filter((v) => v.severity === 'warning').length;

    return {
      timestamp: new Date().toISOString(),
      mode: options.mode,
      filesScanned: files.length,
      violations: filteredViolations,
      claimLedger,
      summary: {
        errors,
        warnings,
        passed: errors === 0,
      },
    };
  }

  private async resolveFiles(patterns: string[]): Promise<string[]> {
    const files: Set<string> = new Set();

    for (const pattern of patterns) {
      // Check if it's a direct file
      if (fs.existsSync(pattern) && fs.statSync(pattern).isFile()) {
        if (this.isMarkdownOrYaml(pattern)) {
          files.add(pattern);
        }
      } else {
        // Treat as glob pattern
        const matches = await glob(pattern, { nodir: true });
        for (const match of matches) {
          if (this.isMarkdownOrYaml(match)) {
            files.add(match);
          }
        }
      }
    }

    return Array.from(files).sort();
  }

  private isMarkdownOrYaml(filename: string): boolean {
    return /\.(md|markdown|yml|yaml)$/i.test(filename);
  }

  private scanFile(file: string, lines: string[], mode: ScanMode): Violation[] {
    const violations: Violation[] = [];

    // Always check secrets (critical)
    violations.push(...this.checkRules(file, lines, this.rules.rules.secretDetection));

    // Always check overpromises (high priority)
    violations.push(...this.checkRules(file, lines, this.rules.rules.overpromises));

    if (mode === 'max') {
      // In max mode, check everything
      violations.push(...this.checkRules(file, lines, this.rules.rules.recencyTriggers));
      violations.push(...this.checkRules(file, lines, this.rules.rules.claimTagging));
    }

    return violations;
  }

  private checkRules(file: string, lines: string[], rules: Rule[]): Violation[] {
    const violations: Violation[] = [];

    for (const rule of rules) {
      if (!rule.enabled) continue;

      for (const pattern of rule.patterns || []) {
        const regex = new RegExp(pattern, 'gi');

        for (let i = 0; i < lines.length; i++) {
          const line = lines[i];
          let match;

          while ((match = regex.exec(line)) !== null) {
            violations.push({
              file,
              line: i + 1,
              column: match.index + 1,
              ruleId: rule.id,
              severity: rule.severity,
              message: rule.description,
              context: this.getContext(lines, i, match.index, pattern.length),
            });
          }
        }
      }
    }

    return violations;
  }

  private extractClaims(file: string, lines: string[]): ClaimLedgerEntry[] {
    const claims: ClaimLedgerEntry[] = [];
    const claimTagPattern = /\[(USER|DED|HYP|UNKNOWN)\]/g;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      let match;

      while ((match = claimTagPattern.exec(line)) !== null) {
        const tag = match[1] as 'USER' | 'DED' | 'HYP' | 'UNKNOWN';
        const claimText = this.extractClaimText(line, match.index);

        // Check if claim needs source (contains recency triggers)
        const needsSource = this.containsRecencyTrigger(claimText);

        claims.push({
          claim: claimText,
          tag,
          file,
          line: i + 1,
          needsSource,
        });
      }
    }

    return claims;
  }

  private extractClaimText(line: string, tagIndex: number): string {
    // Extract text around the tag (simplified approach)
    const start = Math.max(0, tagIndex - 50);
    const end = Math.min(line.length, tagIndex + 100);
    let text = line.substring(start, end).trim();

    // Clean up
    if (start > 0) text = '...' + text;
    if (end < line.length) text = text + '...';

    return text;
  }

  private containsRecencyTrigger(text: string): boolean {
    const triggers = ['202', 'latest', 'current', 'recent', 'price', 'cost', 'law', 'legal'];
    return triggers.some((trigger) => text.toLowerCase().includes(trigger));
  }

  private getContext(lines: string[], lineIndex: number, column: number, length: number): string {
    const line = lines[lineIndex];
    const start = Math.max(0, column - 20);
    const end = Math.min(line.length, column + length + 20);
    let context = line.substring(start, end);

    if (start > 0) context = '...' + context;
    if (end < line.length) context = context + '...';

    return context;
  }

  private isBaselined(violation: Violation): boolean {
    const key = `${violation.file}:${violation.ruleId}:${violation.line}`;
    const hashes = this.baseline.get(key);
    if (!hashes) return false;

    const hash = this.createViolationHash(violation);
    return hashes.has(hash);
  }

  private createViolationHash(violation: Violation): string {
    const content = `${violation.file}:${violation.ruleId}:${violation.line}:${violation.context}`;
    return createHash('sha256').update(content).digest('hex').substring(0, 16);
  }
}
