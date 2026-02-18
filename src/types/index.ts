export type ClaimTag = 'USER' | 'DED' | 'HYP' | 'UNKNOWN';

export type ScanMode = 'light' | 'max';

// ARCHI-Ω v1.2: Proof levels (epistemic foundation)
export type ProofLevel = 'S0' | 'S1' | 'S2' | 'S3' | 'S4';

// ARCHI-Ω v1.2: Risk classes
export type RiskClass = 'R0' | 'R1' | 'R2' | 'R3';

// ARCHI-Ω v1.2: Testability levels (TRACE)
export type TestabilityLevel = 'T0' | 'T1' | 'T2' | 'T3';

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
  riskClass?: RiskClass; // ARCHI-Ω v1.2: Risk classification
}

export interface ClaimLedgerEntry {
  claimId: string; // ARCHI-Ω v1.2: Unique identifier
  claim: string;
  tag: ClaimTag;
  file: string;
  line: number;
  needsSource: boolean;
  proofLevel: ProofLevel; // ARCHI-Ω v1.2: S0-S4
  dependencies: string[]; // ARCHI-Ω v1.2: Claim dependencies
  testability: TestabilityLevel; // ARCHI-Ω v1.2: T0-T3
  testStatus: 'PASS' | 'FAIL' | 'UNKNOWN'; // ARCHI-Ω v1.2: Test result
}

export interface ScanReport {
  timestamp: string;
  mode: ScanMode;
  filesScanned: number;
  violations: Violation[];
  claimLedger: ClaimLedgerEntry[];
  sensitivityMap?: SensitivityFactor[]; // ARCHI-Ω v1.2: Top 5 factors
  summary: {
    errors: number;
    warnings: number;
    passed: boolean;
    riskDistribution?: Record<RiskClass, number>; // ARCHI-Ω v1.2
  };
}

// ARCHI-Ω v1.2: Sensitivity analysis
export interface SensitivityFactor {
  factor: string;
  impact: string;
  threshold: string;
  test: string; // PASS/FAIL condition
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
