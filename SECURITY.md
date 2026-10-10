# Security Policy

## Scope

Security reports may cover the UnitySubAgentHub registry, schemas, validators, ArtistSubAgent backend source, Unity package, CLI, CI workflows, and repository automation.

Historical MyUnityMCP source is not part of the current product surface. Its provenance is frozen under `tests/fixtures/legacy/MyUnityMCP-v1.1.1/` and Git tag `v1.1.1`.

## Reporting a vulnerability

Do not disclose suspected vulnerabilities in a public issue or pull request.

Prefer GitHub's private vulnerability reporting / Security Advisory flow when it is available for this repository. If private reporting is unavailable, contact the repository owner through GitHub and avoid including exploit details in public content.

Include, when possible:

- affected path, version, or commit
- impact and required preconditions
- minimal reproduction steps
- whether the issue affects Hub metadata, validation, CLI, Unity package, CI, or generated artifacts
- suggested mitigation, if known

## Security boundaries

UnitySubAgentHub is not a runtime, Control Plane, resolver, installer, or execution authority. Security fixes must not introduce those responsibilities into Hub validation.

Do not weaken:

- optional specialist installation
- fail-closed eligibility
- explicit approval boundaries
- project / environment binding
- evidence provenance
- repository-relative path validation
- immutable historical provenance
