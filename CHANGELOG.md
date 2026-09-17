# Changelog

All notable changes to the CEYO public presentation layer are documented here.

## [0.4.0] - 2026-09-16

### Architecture alignment

- clarified the distinction between the current public protocol profile and the broader CEYO target architecture;
- established `NDR-US/ceyo-protocol` as the canonical public technical authority;
- aligned project authorship and ownership language around Brian Covarrubias;
- clarified that hashing/signatures provide integrity/authenticity while encryption is a separate confidentiality mechanism;
- removed duplicate protocol/reference implementations from the presentation repository to prevent technical drift;
- removed the site-local Python verifier and unused Python requirements;
- aligned proprietary contribution and licensing language;
- normalized the site release version.

## [0.3.0] - 2026-03-18

### Changed

- `contact.html`: replaced broken Formspree placeholder form with mailto link;
- `how.html`: corrected page title;
- `SECURITY.md`: standardized contact email to `security@ceyo.ai`;
- `SUPPORT.md`: removed stale references to deleted documentation.

### Added

- expanded `.gitignore` coverage for environment files, IDE directories, caches, coverage, and package artifacts.

### Fixed

- broken Trust Center links;
- malformed requirements filename.

## [0.2.0] - 2026-03-11

### Changed

- rewrote the public-facing site as a static HTML presentation layer;
- hardened public-facing pages;
- replaced the previous open-source license with proprietary All Rights Reserved terms;
- rewrote the repository README.

### Added

- public verification/explanation materials;
- navigation and resource integration.

## [0.1.0] - Initial prototype

Initial public repository structure and demonstration materials for the CEYO evidentiary-infrastructure concept.
