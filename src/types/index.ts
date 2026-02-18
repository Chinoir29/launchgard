export type ClaimTag = 'USER' | 'DED' | 'HYP' | 'UNKNOWN';

export type ScanMode = 'light' | 'max';

export interface ScanOptions {
  mode: ScanMode;
  files: string[];
  baselineFile?: string;
  outputDir?: string;
}

export interface Violation {
  file: string;
  line: number;
  column: number;
  ruleId: string;
  severity: 'error' | 'warning';
  message: string;
  context?: string;
}

export interface ClaimLedgerEntry {
  claim: string;
  tag: ClaimTag;
  file: string;
  line: number;
  needsSource: boolean;
}

export interface ScanReport {
  timestamp: string;
  mode: ScanMode;
  filesScanned: number;
  violations: Violation[];
  claimLedger: ClaimLedgerEntry[];
  summary: {
    errors: number;
    warnings: number;
    passed: boolean;
  };
}

export interface Rule {
  id: string;
  name: string;
  description: string;
  severity: 'error' | 'warning';
  enabled: boolean;
  patterns?: string[];
}

export interface RuleSet {
  version: string;
  rules: {
    claimTagging: Rule[];
    overpromises: Rule[];
    recencyTriggers: Rule[];
    secretDetection: Rule[];
  };
}

export interface Baseline {
  version: string;
  timestamp: string;
  violations: Array<{
    file: string;
    ruleId: string;
    line: number;
    hash: string;
  }>;
}
