import { describe, it, expect } from 'vitest';
import { Scanner } from '../src/scanner.js';
import * as fs from 'fs';
import * as path from 'path';

describe('Scanner', () => {
  it('should detect overpromises', async () => {
    const testFile = path.join(process.cwd(), 'tests/fixtures/test-overpromise.md');

    // Create test file
    fs.writeFileSync(
      testFile,
      'This product is guaranteed to work perfectly and is unique in the world.'
    );

    const scanner = new Scanner();
    const report = await scanner.scan({
      mode: 'light',
      files: [testFile],
    });

    expect(report.violations.length).toBeGreaterThan(0);
    expect(report.violations.some((v) => v.ruleId === 'OVER-001')).toBe(true);
    expect(report.summary.passed).toBe(false);

    // Cleanup
    fs.unlinkSync(testFile);
  });

  it('should detect secrets', async () => {
    const testFile = path.join(process.cwd(), 'tests/fixtures/test-secret.md');

    // Create test file with a fake GitHub token pattern
    fs.writeFileSync(testFile, 'My token: ghp_1234567890123456789012345678901234');

    const scanner = new Scanner();
    const report = await scanner.scan({
      mode: 'light',
      files: [testFile],
    });

    expect(report.violations.length).toBeGreaterThan(0);
    expect(report.violations.some((v) => v.ruleId === 'SEC-001')).toBe(true);
    expect(report.summary.passed).toBe(false);

    // Cleanup
    fs.unlinkSync(testFile);
  });

  it('should pass when no violations', async () => {
    const testFile = path.join(process.cwd(), 'tests/fixtures/test-clean.md');

    // Create clean test file
    fs.writeFileSync(testFile, '[DED] This product uses standard encryption methods.');

    const scanner = new Scanner();
    const report = await scanner.scan({
      mode: 'light',
      files: [testFile],
    });

    expect(report.summary.errors).toBe(0);
    expect(report.summary.passed).toBe(true);

    // Cleanup
    fs.unlinkSync(testFile);
  });

  it('should extract claims to ledger', async () => {
    const testFile = path.join(process.cwd(), 'tests/fixtures/test-claims.md');

    // Create test file with tagged claims
    fs.writeFileSync(
      testFile,
      '[USER] Users report improved performance.\n[DED] This uses AES-256 encryption.\n[HYP] This may reduce costs.'
    );

    const scanner = new Scanner();
    const report = await scanner.scan({
      mode: 'max',
      files: [testFile],
    });

    expect(report.claimLedger.length).toBeGreaterThanOrEqual(3);
    expect(report.claimLedger.some((c) => c.tag === 'USER')).toBe(true);
    expect(report.claimLedger.some((c) => c.tag === 'DED')).toBe(true);
    expect(report.claimLedger.some((c) => c.tag === 'HYP')).toBe(true);

    // Cleanup
    fs.unlinkSync(testFile);
  });

  it('should respect light vs max mode', async () => {
    const testFile = path.join(process.cwd(), 'tests/fixtures/test-mode.md');

    // Create test file with recency trigger
    fs.writeFileSync(testFile, 'The latest 2026 version is available.');

    const scanner = new Scanner();

    // Light mode - should not check recency
    const lightReport = await scanner.scan({
      mode: 'light',
      files: [testFile],
    });

    // Max mode - should check recency
    const maxReport = await scanner.scan({
      mode: 'max',
      files: [testFile],
    });

    expect(maxReport.violations.length).toBeGreaterThan(lightReport.violations.length);

    // Cleanup
    fs.unlinkSync(testFile);
  });
});
