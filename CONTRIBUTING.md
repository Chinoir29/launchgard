# Contributing to LaunchGuard

Thank you for your interest in contributing to LaunchGuard! This document provides guidelines for contributing.

## Development Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Chinoir29/launchgard.git
   cd launchgard
   ```

2. **Install dependencies:**

   ```bash
   npm install
   ```

3. **Build the project:**

   ```bash
   npm run build
   ```

4. **Run tests:**
   ```bash
   npm test
   ```

## Project Structure

```
launchgard/
├── src/                # Source code
│   ├── cli.ts         # CLI entry point
│   ├── scanner.ts     # Core scanning logic
│   ├── reporter.ts    # Report generation
│   ├── baseline.ts    # Baseline management
│   ├── rules/         # Rule loading
│   └── types/         # TypeScript types
├── rules/             # Rule definitions (YAML)
├── schemas/           # JSON schemas
├── tests/             # Test files
├── examples/          # Example files and workflows
└── .github/workflows/ # CI/CD workflows
```

## Making Changes

### Adding a New Rule

1. Update `rules/base.yml` with your new rule:

   ```yaml
   - id: 'NEW-001'
     name: 'Rule name'
     description: 'Rule description'
     severity: 'error' # or 'warning'
     enabled: true
     patterns:
       - 'pattern1'
       - 'pattern2'
   ```

2. Add tests in `tests/rsuite-fixtures.test.ts`:

   ```typescript
   it('[FAIL] NEW-001: Should fail on pattern', async () => {
     const testFile = path.join(fixtureDir, 'new-001-fail.md');
     fs.writeFileSync(testFile, 'Text with pattern1');

     const scanner = new Scanner();
     const report = await scanner.scan({ mode: 'light', files: [testFile] });

     expect(report.violations.filter((v) => v.ruleId === 'NEW-001').length).toBeGreaterThan(0);
   });
   ```

3. Update documentation in `README.md` and `METHODOLOGY.md`.

### Code Style

- Use TypeScript for all source code
- Follow the existing code style (enforced by ESLint and Prettier)
- Run `npm run format` before committing
- Run `npm run lint` to check for issues

### Testing

- Write unit tests for new functionality
- Write R-SUITE fixture tests for new rules
- Ensure all tests pass: `npm test`
- Aim for high test coverage

### Commits

Use clear, descriptive commit messages:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation changes
- `test:` for test changes
- `refactor:` for code refactoring
- `chore:` for maintenance tasks

Example: `feat: add support for TypeScript file scanning`

## Pull Request Process

1. **Fork the repository** and create your branch from `main`:

   ```bash
   git checkout -b feature/my-new-feature
   ```

2. **Make your changes** following the guidelines above.

3. **Test thoroughly:**

   ```bash
   npm run build
   npm test
   npm run lint
   ```

4. **Commit your changes** with clear messages.

5. **Push to your fork:**

   ```bash
   git push origin feature/my-new-feature
   ```

6. **Open a Pull Request** with:
   - Clear title and description
   - Reference to any related issues
   - Screenshots/examples if applicable

## Code Review

- All PRs require review before merging
- Address review feedback promptly
- Keep PRs focused on a single feature/fix
- Ensure CI passes

## Reporting Issues

When reporting issues, include:

- LaunchGuard version
- Node.js version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Sample files (if applicable)

## Questions?

Open an issue with the `question` label, or reach out in discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
