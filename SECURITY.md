# Security Policy

## Supported Versions
This project is intended for learning, experimentation, and portfolio use.
Only the most recent version available on the `main` branch is actively maintained and supported.

Older commits, releases, forks, or downstream uses are not monitored for security vulnerabilities.

## Data and Credential Security
* **Secrets and Credentials:** API keys (especially GenAI or cloud credentials) and database passwords must never be committed. Manage these via environment variables or `.env` files that are properly gitignored.
* **Sensitive Data:** Do not commit Personally Identifiable Information (PII), financial records, or proprietary raw datasets to this repository under any circumstances.

## Reporting a Security Vulnerability
If you discover a security vulnerability or suspect a security-related issue, report it responsibly.

❌ **Do not open a public GitHub issue** for security findings.
Public disclosure before remediation can cause unnecessary risk.

✅ **Report the issue privately** using one of the following methods:
* Contact the repository owner through their GitHub profile
* Use a private communication channel if one is explicitly provided

Your report should include:
* A clear description of the vulnerability
* Affected files, components, or workflows
* Steps to reproduce the issue, if applicable
* Potential impact and severity (data exposure, integrity, availability, etc.)
* Any suggested mitigations, if known

Well-documented reports lead to faster and more effective resolution.

## Review and Response Process
After a vulnerability is reported:
* The report will be reviewed as soon as reasonably possible
* Valid issues will be prioritized based on risk and impact
* Reasonable efforts will be made to provide a fix or mitigation

This project does not guarantee response or remediation timelines, but all good-faith reports will be evaluated.

## Disclosure Policy
* Security issues will not be publicly disclosed until a fix or mitigation is available, when feasible
* Coordinated disclosure is preferred to minimize risk to users
* Public acknowledgement may be provided after resolution, at the project maintainer’s discretion

## Scope
This security policy applies to:
* Source code in this repository
* Machine learning pipelines and training workflows
* Data handling, preprocessing, and storage logic
* Dependency definitions and configuration included in the project

The following are **out of scope**:
* Third-party datasets
* External services, platforms, or APIs used for experimentation
* Vulnerabilities introduced by local environments, forks, or modified versions of this repository

## Limitations
This is not a production system. Security best practices are applied where reasonable, but the project is provided **as-is** without guarantees of security, stability, or ongoing support.
