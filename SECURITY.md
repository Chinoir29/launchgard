# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.2.x   | :white_check_mark: |
| < 1.2   | :x:                |

## Reporting a Vulnerability

The ARCHI-Ω framework team takes security issues seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by:

1. **Email**: Send details to the repository maintainer at [security contact to be added]
2. **GitHub Security Advisory**: Use the "Security" tab in the repository to create a private security advisory

### What to Include

Please include the following information in your report:

- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact of the issue, including how an attacker might exploit it

### Response Timeline

- **Initial Response**: Within 48 hours of report
- **Status Update**: Within 7 days with assessment and timeline
- **Fix Development**: Varies based on severity and complexity
- **Public Disclosure**: After fix is released and users have time to update

### Security Features

ARCHI-Ω v1.2 includes built-in security features:

- **Fail-closed authority**: Prevents unauthorized instruction execution
- **Context firewall**: Anti-injection protection against external content
- **Origin tagging**: Mandatory source attribution for all claims
- **PII/secrets hygiene**: Data minimization and secrets handling rules
- **Proof validation**: Risk-based evidence requirements

### Security Best Practices

When using ARCHI-Ω:

1. **Never commit secrets**: Use environment variables for sensitive data
2. **Validate all inputs**: Always sanitize user-provided data
3. **Keep dependencies updated**: Regularly update PyYAML and other dependencies
4. **Use secure configurations**: Follow the security guidelines in ARCHI-OMEGA-v1.2.md
5. **Enable fail-closed mode**: Ensure AUTO-GOV and fail-closed validation are enabled

### Known Security Considerations

- **LLM Integration**: When using with LLMs, be aware of prompt injection risks
- **External Tools**: AUTO-TOOLS feature requires secure tool implementation
- **Data Privacy**: Handle PII according to GDPR and other regulations
- **Input Validation**: User inputs in YAML/JSON should be validated

### Attribution

We appreciate researchers who responsibly disclose vulnerabilities. With your permission, we will:

- Credit you in the CHANGELOG
- Acknowledge your contribution in the security advisory
- Add you to our Hall of Fame (if you wish)

## Security Updates

Subscribe to repository releases to receive notifications about security updates.

---

**Last Updated**: 2026-02-19  
**Framework Version**: ARCHI-Ω v1.2
