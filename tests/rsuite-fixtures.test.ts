import { describe, it, expect, beforeEach, afterEach } from 'vitest';
import { Scanner } from '../src/scanner.js';
import * as fs from 'fs';
import * as path from 'path';

/**
 * R-SUITE Fixture Tests
 * Rules Suite for Uniform Integrity Testing & Enforcement
 * 
 * Each test validates a specific rule's PASS/FAIL behavior
 */

describe('R-SUITE: Overpromise Rules', () => {
  const fixtureDir = path.join(process.cwd(), 'tests/fixtures/rsuite');
  
  beforeEach(() => {
    if (!fs.existsSync(fixtureDir)) {
      fs.mkdirSync(fixtureDir, { recursive: true });
    }
  });

  afterEach(() => {
    // Cleanup fixture files
    if (fs.existsSync(fixtureDir)) {
      const files = fs.readdirSync(fixtureDir);
      files.forEach(file => {
        fs.unlinkSync(path.join(fixtureDir, file));
      });
    }
  });

  it('[PASS] OVER-001: Should pass when no overpromises', async () => {
    const testFile = path.join(fixtureDir, 'over-001-pass.md');
    fs.writeFileSync(testFile, '[DED] This product is designed to provide secure authentication.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'light', files: [testFile] });

    expect(report.violations.filter(v => v.ruleId === 'OVER-001').length).toBe(0);
    expect(report.summary.passed).toBe(true);
  });

  it('[FAIL] OVER-001: Should fail on "guaranteed"', async () => {
    const testFile = path.join(fixtureDir, 'over-001-fail-guaranteed.md');
    fs.writeFileSync(testFile, 'This product is guaranteed to work perfectly.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'light', files: [testFile] });

    expect(report.violations.filter(v => v.ruleId === 'OVER-001').length).toBeGreaterThan(0);
    expect(report.summary.passed).toBe(false);
  });

  it('[FAIL] OVER-001: Should fail on "unique in the world"', async () => {
    const testFile = path.join(fixtureDir, 'over-001-fail-unique.md');
    fs.writeFileSync(testFile, 'Our approach is unique in the world.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'light', files: [testFile] });

    expect(report.violations.filter(v => v.ruleId === 'OVER-001').length).toBeGreaterThan(0);
    expect(report.summary.passed).toBe(false);
  });

  it('[FAIL] OVER-001: Should fail on "100% secure"', async () => {
    const testFile = path.join(fixtureDir, 'over-001-fail-100percent.md');
    fs.writeFileSync(testFile, 'We provide 100% secure authentication.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'light', files: [testFile] });

    expect(report.violations.filter(v => v.ruleId === 'OVER-001').length).toBeGreaterThan(0);
    expect(report.summary.passed).toBe(false);
  });
});

describe('R-SUITE: Secret Detection Rules', () => {
  const fixtureDir = path.join(process.cwd(), 'tests/fixtures/rsuite');
  
  beforeEach(() => {
    if (!fs.existsSync(fixtureDir)) {
      fs.mkdirSync(fixtureDir, { recursive: true });
    }
  });

  afterEach(() => {
    if (fs.existsSync(fixtureDir)) {
      const files = fs.readdirSync(fixtureDir);
      files.forEach(file => {
        fs.unlinkSync(path.join(fixtureDir, file));
      });
    }
  });

  it('[PASS] SEC-001: Should pass when no GitHub tokens', async () => {
    const testFile = path.join(fixtureDir, 'sec-001-pass.md');
    fs.writeFileSync(testFile, 'Configure your GitHub token in settings.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'light', files: [testFile] });

    expect(report.violations.filter(v => v.ruleId === 'SEC-001').length).toBe(0);
    expect(report.summary.passed).toBe(true);
  });

  it('[FAIL] SEC-001: Should fail on GitHub token pattern', async () => {
    const testFile = path.join(fixtureDir, 'sec-001-fail-ghp.md');
    fs.writeFileSync(testFile, 'Token: ghp_1234567890123456789012345678901234');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'light', files: [testFile] });

    expect(report.violations.filter(v => v.ruleId === 'SEC-001').length).toBeGreaterThan(0);
    expect(report.summary.passed).toBe(false);
  });

  it('[PASS] SEC-002: Should pass when no OpenAI keys', async () => {
    const testFile = path.join(fixtureDir, 'sec-002-pass.md');
    fs.writeFileSync(testFile, 'Configure your OpenAI API key.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'light', files: [testFile] });

    expect(report.violations.filter(v => v.ruleId === 'SEC-002').length).toBe(0);
    expect(report.summary.passed).toBe(true);
  });

  it('[FAIL] SEC-002: Should fail on OpenAI key pattern', async () => {
    const testFile = path.join(fixtureDir, 'sec-002-fail-sk.md');
    fs.writeFileSync(testFile, 'Key: sk-123456789012345678901234567890123456789012345678');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'light', files: [testFile] });

    expect(report.violations.filter(v => v.ruleId === 'SEC-002').length).toBeGreaterThan(0);
    expect(report.summary.passed).toBe(false);
  });
});

describe('R-SUITE: Recency Trigger Rules', () => {
  const fixtureDir = path.join(process.cwd(), 'tests/fixtures/rsuite');
  
  beforeEach(() => {
    if (!fs.existsSync(fixtureDir)) {
      fs.mkdirSync(fixtureDir, { recursive: true });
    }
  });

  afterEach(() => {
    if (fs.existsSync(fixtureDir)) {
      const files = fs.readdirSync(fixtureDir);
      files.forEach(file => {
        fs.unlinkSync(path.join(fixtureDir, file));
      });
    }
  });

  it('[PASS] REC-001: Should pass in light mode (recency not checked)', async () => {
    const testFile = path.join(fixtureDir, 'rec-001-pass-light.md');
    fs.writeFileSync(testFile, 'The latest 2026 version is available.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'light', files: [testFile] });

    // In light mode, recency is not checked
    expect(report.violations.filter(v => v.ruleId === 'REC-001').length).toBe(0);
  });

  it('[FAIL] REC-001: Should warn on year 2026 in max mode', async () => {
    const testFile = path.join(fixtureDir, 'rec-001-fail-2026.md');
    fs.writeFileSync(testFile, 'In 2026, this feature will be available.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'max', files: [testFile] });

    expect(report.violations.filter(v => v.ruleId === 'REC-001').length).toBeGreaterThan(0);
  });

  it('[FAIL] REC-001: Should warn on "latest" in max mode', async () => {
    const testFile = path.join(fixtureDir, 'rec-001-fail-latest.md');
    fs.writeFileSync(testFile, 'Use the latest version for best performance.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'max', files: [testFile] });

    expect(report.violations.filter(v => v.ruleId === 'REC-001').length).toBeGreaterThan(0);
  });

  it('[FAIL] REC-001: Should warn on price references in max mode', async () => {
    const testFile = path.join(fixtureDir, 'rec-001-fail-price.md');
    fs.writeFileSync(testFile, 'Current price is $99/month.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'max', files: [testFile] });

    expect(report.violations.filter(v => v.ruleId === 'REC-001').length).toBeGreaterThan(0);
  });
});

describe('R-SUITE: Claim Ledger', () => {
  const fixtureDir = path.join(process.cwd(), 'tests/fixtures/rsuite');
  
  beforeEach(() => {
    if (!fs.existsSync(fixtureDir)) {
      fs.mkdirSync(fixtureDir, { recursive: true });
    }
  });

  afterEach(() => {
    if (fs.existsSync(fixtureDir)) {
      const files = fs.readdirSync(fixtureDir);
      files.forEach(file => {
        fs.unlinkSync(path.join(fixtureDir, file));
      });
    }
  });

  it('[PASS] Should extract [USER] tagged claims', async () => {
    const testFile = path.join(fixtureDir, 'claim-user.md');
    fs.writeFileSync(testFile, '[USER] Users report 50% faster processing.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'max', files: [testFile] });

    expect(report.claimLedger.length).toBeGreaterThan(0);
    expect(report.claimLedger.some(c => c.tag === 'USER')).toBe(true);
  });

  it('[PASS] Should extract [DED] tagged claims', async () => {
    const testFile = path.join(fixtureDir, 'claim-ded.md');
    fs.writeFileSync(testFile, '[DED] This uses AES-256 encryption.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'max', files: [testFile] });

    expect(report.claimLedger.length).toBeGreaterThan(0);
    expect(report.claimLedger.some(c => c.tag === 'DED')).toBe(true);
  });

  it('[PASS] Should extract [HYP] tagged claims', async () => {
    const testFile = path.join(fixtureDir, 'claim-hyp.md');
    fs.writeFileSync(testFile, '[HYP] This may reduce latency by 30%.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'max', files: [testFile] });

    expect(report.claimLedger.length).toBeGreaterThan(0);
    expect(report.claimLedger.some(c => c.tag === 'HYP')).toBe(true);
  });

  it('[PASS] Should extract [UNKNOWN] tagged claims', async () => {
    const testFile = path.join(fixtureDir, 'claim-unknown.md');
    fs.writeFileSync(testFile, '[UNKNOWN] Industry standard practice.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'max', files: [testFile] });

    expect(report.claimLedger.length).toBeGreaterThan(0);
    expect(report.claimLedger.some(c => c.tag === 'UNKNOWN')).toBe(true);
  });

  it('[PASS] Should flag claims with recency triggers as needing source', async () => {
    const testFile = path.join(fixtureDir, 'claim-needs-source.md');
    fs.writeFileSync(testFile, '[USER] Current price is $99/month according to surveys.');

    const scanner = new Scanner();
    const report = await scanner.scan({ mode: 'max', files: [testFile] });

    const claim = report.claimLedger.find(c => c.tag === 'USER');
    expect(claim).toBeDefined();
    expect(claim?.needsSource).toBe(true);
  });
});

describe('R-SUITE: Deterministic Output', () => {
  const fixtureDir = path.join(process.cwd(), 'tests/fixtures/rsuite');
  
  beforeEach(() => {
    if (!fs.existsSync(fixtureDir)) {
      fs.mkdirSync(fixtureDir, { recursive: true });
    }
  });

  afterEach(() => {
    if (fs.existsSync(fixtureDir)) {
      const files = fs.readdirSync(fixtureDir);
      files.forEach(file => {
        fs.unlinkSync(path.join(fixtureDir, file));
      });
    }
  });

  it('[PASS] Should produce identical results on repeated scans', async () => {
    const testFile = path.join(fixtureDir, 'deterministic.md');
    fs.writeFileSync(testFile, 'This is guaranteed to work. Token: ghp_1234567890123456789012345678901234');

    const scanner1 = new Scanner();
    const report1 = await scanner1.scan({ mode: 'light', files: [testFile] });

    const scanner2 = new Scanner();
    const report2 = await scanner2.scan({ mode: 'light', files: [testFile] });

    // Compare violations (excluding timestamp)
    expect(report1.violations.length).toBe(report2.violations.length);
    expect(report1.summary.errors).toBe(report2.summary.errors);
    expect(report1.summary.warnings).toBe(report2.summary.warnings);
    
    // Verify violations are in same order
    for (let i = 0; i < report1.violations.length; i++) {
      expect(report1.violations[i].file).toBe(report2.violations[i].file);
      expect(report1.violations[i].line).toBe(report2.violations[i].line);
      expect(report1.violations[i].ruleId).toBe(report2.violations[i].ruleId);
    }
  });
});
