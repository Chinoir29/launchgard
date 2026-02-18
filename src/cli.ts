#!/usr/bin/env node

import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';
import { Scanner } from './scanner.js';
import { Reporter } from './reporter.js';
import { BaselineManager } from './baseline.js';
import * as fs from 'fs';

interface CliArguments {
  mode: 'light' | 'max';
  files: string[];
  baseline?: string;
  'create-baseline'?: string;
  output?: string;
  verbose?: boolean;
}

async function main() {
  const argv = (await yargs(hideBin(process.argv))
    .usage('Usage: $0 [options] <files...>')
    .option('mode', {
      alias: 'm',
      type: 'string',
      choices: ['light', 'max'],
      default: 'light',
      description: 'Scan mode: light (secrets + overpromises) or max (all rules)',
    })
    .option('baseline', {
      alias: 'b',
      type: 'string',
      description: 'Path to baseline file to ignore existing violations',
    })
    .option('create-baseline', {
      type: 'string',
      description: 'Create a baseline file from current violations',
    })
    .option('output', {
      alias: 'o',
      type: 'string',
      default: '.',
      description: 'Output directory for reports',
    })
    .option('verbose', {
      alias: 'v',
      type: 'boolean',
      default: false,
      description: 'Verbose output',
    })
    .demandCommand(1, 'You must provide at least one file or pattern to scan')
    .example('$0 README.md', 'Scan a single file')
    .example('$0 --mode max "**/*.md"', 'Scan all markdown files in max mode')
    .example('$0 --baseline .baseline.json "**/*.md"', 'Scan with baseline')
    .example('$0 --create-baseline .baseline.json "**/*.md"', 'Create baseline')
    .help()
    .alias('h', 'help')
    .version('0.1.0')
    .alias('V', 'version')
    .parse()) as CliArguments;

  try {
    const files = argv._;
    const scanner = new Scanner();
    const reporter = new Reporter();

    if (argv.verbose) {
      console.log('LaunchGuard starting...');
      console.log(`Mode: ${argv.mode}`);
      console.log(`Files: ${files.join(', ')}`);
    }

    const report = await scanner.scan({
      mode: argv.mode,
      files: files as string[],
      baselineFile: argv.baseline,
      outputDir: argv.output,
    });

    // Handle baseline creation
    if (argv['create-baseline']) {
      const baselineManager = new BaselineManager();
      const baseline = baselineManager.createBaseline(report.violations);
      baselineManager.saveBaseline(baseline, argv['create-baseline']);
      console.log(`✅ Baseline created: ${argv['create-baseline']}`);
      console.log(
        `   Captured ${baseline.violations.length} violations to ignore in future scans`
      );
    }

    // Write reports
    await reporter.writeReports(report, argv.output);

    // Console output
    console.log(reporter.generateConsoleOutput(report));

    if (argv.verbose) {
      console.log(`\nReports written to:`);
      console.log(`  - ${argv.output}/report.json`);
      console.log(`  - ${argv.output}/report.md`);
    }

    // Exit codes: 0 = pass, 1 = fail (errors), 2 = error (exception)
    process.exit(report.summary.passed ? 0 : 1);
  } catch (error) {
    console.error('❌ Error:', error instanceof Error ? error.message : String(error));
    process.exit(2);
  }
}

main();
