import * as core from '@actions/core';
import * as fs from 'fs';
import { Scanner } from '../src/scanner.js';
import { Reporter } from '../src/reporter.js';
import { BaselineManager } from '../src/baseline.js';

async function run() {
  try {
    // Get inputs
    const mode = core.getInput('mode') as 'light' | 'max';
    const filesInput = core.getInput('files');
    const baseline = core.getInput('baseline') || undefined;
    const createBaseline = core.getInput('create-baseline') || undefined;
    const failOnWarnings = core.getInput('fail-on-warnings') === 'true';

    const files = filesInput.split(/\s+/).filter((f) => f.length > 0);

    core.info(`LaunchGuard starting in ${mode} mode...`);
    core.info(`Scanning: ${files.join(', ')}`);

    // Run scan
    const scanner = new Scanner();
    const reporter = new Reporter();

    const report = await scanner.scan({
      mode,
      files,
      baselineFile: baseline,
      outputDir: './launchgard-reports',
    });

    // Create baseline if requested
    if (createBaseline) {
      const baselineManager = new BaselineManager();
      const baselineData = baselineManager.createBaseline(report.violations);
      baselineManager.saveBaseline(baselineData, createBaseline);
      core.info(`✅ Baseline created: ${createBaseline}`);
    }

    // Write reports
    await reporter.writeReports(report, './launchgard-reports');

    // Set outputs
    core.setOutput('passed', report.summary.passed ? 'true' : 'false');
    core.setOutput('errors', report.summary.errors.toString());
    core.setOutput('warnings', report.summary.warnings.toString());
    core.setOutput('report-path', './launchgard-reports');

    // Log results
    core.info('\n' + reporter.generateConsoleOutput(report));

    // Display report summary
    if (report.summary.errors > 0) {
      core.error(`❌ Found ${report.summary.errors} error(s)`);
    }
    if (report.summary.warnings > 0) {
      core.warning(`⚠️  Found ${report.summary.warnings} warning(s)`);
    }

    // Fail if needed
    if (!report.summary.passed) {
      core.setFailed('LaunchGuard scan failed with errors');
    } else if (failOnWarnings && report.summary.warnings > 0) {
      core.setFailed('LaunchGuard scan failed (warnings treated as failures)');
    } else {
      core.info('✅ LaunchGuard scan passed');
    }
  } catch (error) {
    core.setFailed(error instanceof Error ? error.message : String(error));
  }
}

run();
