# Example: Using LaunchGuard in Your Repository

This directory contains example workflows for using LaunchGuard.

## Basic Usage

Create `.github/workflows/launchgard.yml`:

```yaml
name: LaunchGuard Quality Check

on:
  pull_request:
    paths:
      - '**.md'
      - '**.yml'
      - '**.yaml'

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run LaunchGuard
        uses: Chinoir29/launchgard@v0.1.0
        with:
          mode: 'light'
          files: '**/*.md **/*.yml **/*.yaml'
      
      - name: Upload reports
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: launchgard-reports
          path: launchgard-reports/
```

## With Baseline

```yaml
name: LaunchGuard with Baseline

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run LaunchGuard
        uses: Chinoir29/launchgard@v0.1.0
        with:
          mode: 'max'
          files: '**/*.md'
          baseline: '.launchgard-baseline.json'
```

## Strict Mode (Fail on Warnings)

```yaml
name: LaunchGuard Strict

on: [push, pull_request]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run LaunchGuard
        uses: Chinoir29/launchgard@v0.1.0
        with:
          mode: 'max'
          files: '**/*.md **/*.yml'
          fail-on-warnings: 'true'
```

## Advanced: Create Baseline

```yaml
name: Create LaunchGuard Baseline

on:
  workflow_dispatch:

jobs:
  create-baseline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Create Baseline
        uses: Chinoir29/launchgard@v0.1.0
        with:
          mode: 'light'
          files: '**/*.md'
          create-baseline: '.launchgard-baseline.json'
      
      - name: Commit Baseline
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add .launchgard-baseline.json
          git commit -m "chore: update LaunchGuard baseline"
          git push
```
