import { describe, it, expect } from 'vitest';
import { BaselineManager } from '../src/baseline.js';
import { Violation } from '../src/types/index.js';
import * as fs from 'fs';
import * as path from 'path';

describe('BaselineManager', () => {
  const testBaselinePath = path.join(process.cwd(), 'tests/fixtures/test-baseline.json');

  it('should create baseline from violations', () => {
    const manager = new BaselineManager();
    const violations: Violation[] = [
      {
        file: 'test.md',
        line: 1,
        column: 1,
        ruleId: 'OVER-001',
        severity: 'error',
        message: 'Test violation',
        context: 'test context',
      },
    ];

    const baseline = manager.createBaseline(violations);

    expect(baseline.version).toBe('1.0.0');
    expect(baseline.violations.length).toBe(1);
    expect(baseline.violations[0].file).toBe('test.md');
    expect(baseline.violations[0].ruleId).toBe('OVER-001');
    expect(baseline.violations[0].hash).toBeDefined();
  });

  it('should save and load baseline', () => {
    const manager = new BaselineManager();
    const violations: Violation[] = [
      {
        file: 'test.md',
        line: 1,
        column: 1,
        ruleId: 'OVER-001',
        severity: 'error',
        message: 'Test violation',
        context: 'test context',
      },
    ];

    const baseline = manager.createBaseline(violations);
    manager.saveBaseline(baseline, testBaselinePath);

    expect(fs.existsSync(testBaselinePath)).toBe(true);

    const loaded = manager.loadBaseline(testBaselinePath);
    expect(loaded).not.toBeNull();
    expect(loaded?.violations.length).toBe(1);

    // Cleanup
    fs.unlinkSync(testBaselinePath);
  });

  it('should return null for non-existent baseline', () => {
    const manager = new BaselineManager();
    const loaded = manager.loadBaseline('/non/existent/path.json');
    expect(loaded).toBeNull();
  });
});
