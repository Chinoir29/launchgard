import { describe, it, expect } from 'vitest';
import { Reporter } from '../src/reporter.js';
import { ScanReport } from '../src/types/index.js';

describe('Reporter', () => {
  const mockReport: ScanReport = {
    timestamp: '2026-01-01T00:00:00.000Z',
    mode: 'light',
    filesScanned: 1,
    violations: [
      {
        file: 'test.md',
        line: 1,
        column: 10,
        ruleId: 'OVER-001',
        severity: 'error',
        message: 'Detects overpromising language',
        context: 'guaranteed to work',
      },
    ],
    claimLedger: [
      {
        claim: '[DED] Uses AES-256',
        tag: 'DED',
        file: 'test.md',
        line: 5,
        needsSource: false,
      },
    ],
    summary: {
      errors: 1,
      warnings: 0,
      passed: false,
    },
  };

  it('should generate markdown report', () => {
    const reporter = new Reporter();
    const markdown = reporter.generateMarkdown(mockReport);

    expect(markdown).toContain('# LaunchGuard Scan Report');
    expect(markdown).toContain('❌ FAIL');
    expect(markdown).toContain('OVER-001');
    expect(markdown).toContain('Claim Ledger');
  });

  it('should generate console output', () => {
    const reporter = new Reporter();
    const output = reporter.generateConsoleOutput(mockReport);

    expect(output).toContain('LaunchGuard Scan Results');
    expect(output).toContain('❌ FAIL');
    expect(output).toContain('Errors:        1');
  });

  it('should show PASS for clean reports', () => {
    const cleanReport: ScanReport = {
      ...mockReport,
      violations: [],
      summary: { errors: 0, warnings: 0, passed: true },
    };

    const reporter = new Reporter();
    const output = reporter.generateConsoleOutput(cleanReport);

    expect(output).toContain('✅ PASS');
  });
});
