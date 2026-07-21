# Security Policy

## Scope

Case Intake Suite is a local-only tool. It has no network-facing components, no authentication system, and no external API integrations. The attack surface is limited to the local file system and the local Flask server (127.0.0.1 only).

## Supported Versions

| Version | Supported |
|---|---|
| 1.x (main) | Yes |

## Reporting a Vulnerability

If you find a security issue in this project, please open a GitHub Issue marked `[SECURITY]` or contact the maintainer directly via GitHub.

Do not disclose vulnerabilities publicly before they have been reviewed and patched.

## Out of Scope

- Vulnerabilities in third-party packages (report to those projects directly).
- Issues arising from running the Flask server in a production or internet-facing configuration (this tool is not designed for that).

## Intended Use

This tool is designed for local use only. Running `app.py` binds to `127.0.0.1:5000`. Do not expose it on a public network interface.
