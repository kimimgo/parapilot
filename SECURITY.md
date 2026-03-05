# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in parapilot, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

### How to Report

1. **GitHub Private Vulnerability Reporting** (preferred):
   Go to [Security Advisories](https://github.com/kimimgo/parapilot/security/advisories/new) and create a new advisory.

2. **Email**: Send details to [kimimgo@gmail.com](mailto:kimimgo@gmail.com)

### What to Include

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Response Timeline

| Action | Timeline |
|--------|----------|
| Acknowledgment | Within 48 hours |
| Initial assessment | Within 5 business days |
| Patch release | Within 7 days of confirmation |

### Disclosure Policy

- Security issues are disclosed **after** a patch is released
- Credit is given to reporters (unless anonymity is requested)

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | Yes       |

## Scope

The following are in scope:
- Path traversal via `PARAPILOT_DATA_DIR`
- MCP protocol injection
- Arbitrary code execution via pipeline DSL
- Dependencies with known CVEs
