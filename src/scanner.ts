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
  ProofLevel,
  TestabilityLevel,
  RiskClass,
  SensitivityFactor,
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

    // ARCHI-Ω v1.2: Calculate risk distribution
    const riskDistribution: Record<RiskClass, number> = {
      R0: 0,
      R1: 0,
      R2: 0,
      R3: 0,
    };
    filteredViolations.forEach((v) => {
      if (v.riskClass) {
        riskDistribution[v.riskClass]++;
      }
    });

    // ARCHI-Ω v1.2: Generate sensitivity map
    const sensitivityMap = this.generateSensitivityMap(
      filteredViolations,
      claimLedger,
      options.mode
    );

    return {
      timestamp: new Date().toISOString(),
      mode: options.mode,
      filesScanned: files.length,
      violations: filteredViolations,
      claimLedger,
      sensitivityMap,
      summary: {
        errors,
        warnings,
        passed: errors === 0,
        riskDistribution,
      },
    };
  }

  // ARCHI-Ω v1.2: Generate sensitivity map (top 5 factors)
  private generateSensitivityMap(
    violations: Violation[],
    claims: ClaimLedgerEntry[],
    mode: ScanMode
  ): SensitivityFactor[] {
    const factors: SensitivityFactor[] = [];

    // Factor 1: Scan mode
    factors.push({
      factor: 'Scan Mode',
      impact: mode === 'light' ? 'Switching to max mode would check recency triggers and claim tagging' : 'Switching to light mode would skip recency and claim checks',
      threshold: 'mode=max vs mode=light',
      test: `PASS if mode=${mode === 'light' ? 'max' : 'light'} detects ${mode === 'light' ? 'more' : 'fewer'} violations`,
    });

    // Factor 2: Baseline usage
    factors.push({
      factor: 'Baseline File',
      impact: 'Using a baseline would ignore existing violations, allowing incremental adoption',
      threshold: 'baseline present vs absent',
      test: 'PASS if baseline filters out grandfathered violations',
    });

    // Factor 3: Secret detection
    const secretViolations = violations.filter((v) => v.ruleId.startsWith('SEC-'));
    if (secretViolations.length > 0) {
      factors.push({
        factor: 'Exposed Secrets',
        impact: `${secretViolations.length} secret(s) detected - high security risk`,
        threshold: 'secrets > 0',
        test: 'FAIL if any secrets detected; PASS if all secrets removed or redacted',
      });
    }

    // Factor 4: Claims needing sources
    const unverifiedClaims = claims.filter((c) => c.needsSource && c.testStatus !== 'PASS');
    if (unverifiedClaims.length > 0) {
      factors.push({
        factor: 'Unverified Claims',
        impact: `${unverifiedClaims.length} claim(s) need sources for recency/instability triggers`,
        threshold: 'unverified claims > 0',
        test: 'PASS if claims tagged and sourced; FAIL if claims remain UNKNOWN',
      });
    }

    // Factor 5: Risk class distribution
    const r2Count = violations.filter((v) => v.riskClass === 'R2').length;
    if (r2Count > 0) {
      factors.push({
        factor: 'High-Risk Violations (R2)',
        impact: `${r2Count} high-impact violation(s) detected (security/finance/legal)`,
        threshold: 'R2 violations > 0',
        test: 'FAIL while R2 violations exist; PASS when all R2 violations resolved',
      });
    }

    return factors.slice(0, 5); // Top 5
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
            // ARCHI-Ω v1.2: Determine risk class based on rule category
            const riskClass = this.determineRiskClass(rule.id);

            violations.push({
              file,
              line: i + 1,
              column: match.index + 1,
              ruleId: rule.id,
              severity: rule.severity,
              message: rule.description,
              context: this.getContext(lines, i, match.index, pattern.length),
              riskClass,
            });
          }
        }
      }
    }

    return violations;
  }

  // ARCHI-Ω v1.2: Determine risk class based on rule ID
  private determineRiskClass(ruleId: string): RiskClass {
    // R3 = illegal/dangerous (STOP), R2 = high impact, R1 = operational, R0 = low
    if (ruleId.startsWith('SEC-')) return 'R2'; // Security issues are high risk
    if (ruleId.startsWith('OVER-')) return 'R1'; // Overpromises are operational risk
    if (ruleId.startsWith('REC-')) return 'R1'; // Recency triggers need attention
    if (ruleId.startsWith('CLAIM-')) return 'R0'; // Claim tagging issues are lower risk
    return 'R1'; // Default to operational risk
  }

  private extractClaims(file: string, lines: string[]): ClaimLedgerEntry[] {
    const claims: ClaimLedgerEntry[] = [];
    const claimTagPattern = /\[(USER|DED|HYP|UNKNOWN)\]/g;
    let claimCounter = 1;

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      let match;

      while ((match = claimTagPattern.exec(line)) !== null) {
        const tag = match[1] as 'USER' | 'DED' | 'HYP' | 'UNKNOWN';
        const claimText = this.extractClaimText(line, match.index);

        // Check if claim needs source (contains recency triggers)
        const needsSource = this.containsRecencyTrigger(claimText);

        // ARCHI-Ω v1.2: Determine proof level based on tag
        const proofLevel = this.determineProofLevel(tag, needsSource);

        // ARCHI-Ω v1.2: Determine testability
        const testability = this.determineTestability(tag, claimText);

        // ARCHI-Ω v1.2: Extract dependencies (simplified - look for references)
        const dependencies = this.extractDependencies(claimText);

        // ARCHI-Ω v1.2: Test status based on proof level and needs source
        const testStatus = this.determineTestStatus(proofLevel, needsSource);

        claims.push({
          claimId: `CLAIM-${file.replace(/[^a-zA-Z0-9]/g, '_')}-${i + 1}-${claimCounter}`,
          claim: claimText,
          tag,
          file,
          line: i + 1,
          needsSource,
          proofLevel,
          dependencies,
          testability,
          testStatus,
        });
        claimCounter++;
      }
    }

    return claims;
  }

  // ARCHI-Ω v1.2: Determine proof level based on claim tag
  private determineProofLevel(
    tag: 'USER' | 'DED' | 'HYP' | 'UNKNOWN',
    needsSource: boolean
  ): ProofLevel {
    // S0 = user data, S1 = deduction, S2 = external source needed, S3 = testable, S4 = cross-checked
    switch (tag) {
      case 'USER':
        return 'S0'; // User-reported data
      case 'DED':
        return needsSource ? 'S2' : 'S1'; // Deduction, may need external verification
      case 'HYP':
        return 'S1'; // Hypothesis - reasoning level
      case 'UNKNOWN':
        return needsSource ? 'S2' : 'S0'; // Unknown provenance
    }
  }

  // ARCHI-Ω v1.2: Determine testability level
  private determineTestability(tag: string, claimText: string): TestabilityLevel {
    // T0 = untestable, T1 = implicit, T2 = explicit PASS/FAIL, T3 = reproducible with metrics
    if (tag === 'USER') return 'T1'; // User reports - implicit testability
    if (tag === 'DED') {
      // Deductions with metrics are T3
      if (/\d+%|\d+ms|\d+\s*(seconds|minutes|hours|bytes|MB|GB)/.test(claimText)) return 'T3';
      return 'T2'; // Deductions are generally testable
    }
    if (tag === 'HYP') return 'T2'; // Hypotheses need explicit tests
    return 'T1'; // Unknown - implicit at best
  }

  // ARCHI-Ω v1.2: Extract claim dependencies
  private extractDependencies(claimText: string): string[] {
    const deps: string[] = [];
    // Look for references to other components/systems
    const refPatterns = [
      /depends on ([A-Za-z0-9-]+)/gi,
      /requires ([A-Za-z0-9-]+)/gi,
      /uses ([A-Za-z0-9-]+)/gi,
    ];

    for (const pattern of refPatterns) {
      const matches = claimText.matchAll(pattern);
      for (const match of matches) {
        if (match[1]) deps.push(match[1]);
      }
    }

    return deps;
  }

  // ARCHI-Ω v1.2: Determine test status
  private determineTestStatus(
    proofLevel: ProofLevel,
    needsSource: boolean
  ): 'PASS' | 'FAIL' | 'UNKNOWN' {
    // If needs source but proof level is low, mark as UNKNOWN
    if (needsSource && (proofLevel === 'S0' || proofLevel === 'S1')) return 'UNKNOWN';
    // If proof level is adequate (S2+), mark as PASS
    if (proofLevel === 'S2' || proofLevel === 'S3' || proofLevel === 'S4') return 'PASS';
    // Otherwise UNKNOWN
    return 'UNKNOWN';
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
