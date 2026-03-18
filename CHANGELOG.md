# Changelog

All notable changes to the CEYO project will be documented in this file.

The format loosely follows Keep a Changelog principles.

---

## [0.3.0] - 2026-03-18

### Changed

• contact.html: replaced broken Formspree placeholder form with mailto link
• how.html: corrected page title (was "Compliance", now "How It Works")
• SECURITY.md: standardized contact email to security@ceyo.ai
• SUPPORT.md: removed stale references to deleted docs/ directory

### Added

• .gitignore: added .env, IDE directories, pytest cache, coverage, egg-info

### Fixed

• Broken "Trust Center" footer link across 4 pages (now points to trust.html)
• Malformed requirements filename (was "requirements.txt (root)")

---

## [0.2.0] - 2026-03-11

Site rewrite and hardening.

### Changed

• Rewrote public-facing site as static HTML presentation layer
• Institutional-grade hardening across all 17 pages
• Replaced MIT license with proprietary All Rights Reserved
• Rewrote README as clean public-facing presentation layer

### Added

• Interactive in-browser artifact verifier (verify.html)
• Wire verify.html into site navigation and CTAs

### Fixed

• Broken ethics nav link across all pages
• Stale sample artifacts; updated tooling and error messages

---

## [0.1.0] - Initial Prototype

Initial public repository structure.

### Added

Reference components:

• Example artifact workflow
• Sample artifact records
• Minimal verification demonstration

Repository structure:

• example_artifact/ — sample envelope and verification script
• tools/ — reference implementation and CLI verifier
• Protocol specifications maintained in ceyo-protocol repository

This release represents the initial prototype and conceptual architecture for the CEYO evidentiary infrastructure.
