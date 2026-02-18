import * as fs from 'fs';
import { createHash } from 'crypto';
import { Baseline, Violation } from './types/index.js';

export class BaselineManager {
  createBaseline(violations: Violation[]): Baseline {
    return {
      version: '1.0.0',
      timestamp: new Date().toISOString(),
      violations: violations.map((v) => ({
        file: v.file,
        ruleId: v.ruleId,
        line: v.line,
        hash: this.createViolationHash(v),
      })),
    };
  }

  saveBaseline(baseline: Baseline, filepath: string): void {
    fs.writeFileSync(filepath, JSON.stringify(baseline, null, 2), 'utf-8');
  }

  loadBaseline(filepath: string): Baseline | null {
    if (!fs.existsSync(filepath)) {
      return null;
    }

    const content = fs.readFileSync(filepath, 'utf-8');
    return JSON.parse(content) as Baseline;
  }

  private createViolationHash(violation: Violation): string {
    const content = `${violation.file}:${violation.ruleId}:${violation.line}:${violation.context}`;
    return createHash('sha256').update(content).digest('hex').substring(0, 16);
  }
}
