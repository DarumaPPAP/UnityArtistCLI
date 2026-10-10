#!/usr/bin/env python3
"""UnitySubAgentHubのRepository AuthorityとArtist version mirrorを検証する。"""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
MAP_PATH = ROOT / "Hub/repository-authority.yaml"
EXPECTED_REPOSITORY = "DarumaPPAP/UnitySubAgentHub"
EXPECTED_RUNTIME_OWNER = "DarumaPPAP/UnityAgent"


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain a mapping")
    return value


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must contain an object")
    return value


def _require_path(relative: str, errors: list[str]) -> None:
    if not (ROOT / relative).exists():
        errors.append(f"authority path does not exist: {relative}")


def _artist_version(manifest_path: Path) -> str:
    manifest = _load_yaml(manifest_path)
    identity = manifest.get("identity")
    if not isinstance(identity, dict) or not isinstance(identity.get("version"), str):
        raise ValueError("Artist manifest identity.version is missing")
    return identity["version"]


def public_release_workflows(workflow_root: Path) -> list[str]:
    """Allow the named read-only observation Canary, never public publication."""
    forbidden = []
    publishing_actions = ("softprops/action-gh-release", "ncipollo/release-action", "actions/create-release", "actions/upload-release-asset")
    publishing_commands = re.compile(r"\bgh\s+release\s+(?:create|upload|edit|delete)\b|\bgh\s+api\b(?=[^\n]*releases)(?=[^\n]*(?:(?:--method(?:=|\s+)|-X\s*)(?:POST|PATCH|DELETE)\b|(?:--(?:raw-)?field(?:=|\s+)|-[fF]\s*)))|\bcurl\b[^\n]*/releases", re.IGNORECASE)
    for path in sorted((*workflow_root.glob("*.yml"), *workflow_root.glob("*.yaml"))):
        canary = path.name == "unity-prerelease-canary.yml"
        try:
            workflow = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not isinstance(workflow, dict):
                raise ValueError("workflow mapping required")
            unsafe = "release" in path.name.lower() and not canary
            if canary and workflow.get("permissions", {}).get("contents") != "read":
                unsafe = True
            def inspect(node):
                nonlocal unsafe
                if isinstance(node, dict):
                    for key, value in node.items():
                        if key == "uses" and isinstance(value, str) and value.lower().split("@")[0] in publishing_actions:
                            unsafe = True
                        if key == "run" and isinstance(value, str) and publishing_commands.search(value):
                            unsafe = True
                        if canary and key == "permissions" and (value == "write-all" or isinstance(value, dict) and value.get("contents") == "write"):
                            unsafe = True
                        inspect(value)
                elif isinstance(node, list):
                    for value in node:
                        inspect(value)
            inspect(workflow)
            if unsafe:
                forbidden.append(path.name)
        except (OSError, ValueError, AttributeError, yaml.YAMLError):
            forbidden.append(path.name)
    return forbidden


def validate_repository() -> list[str]:
    errors: list[str] = []

    try:
        authority = _load_yaml(MAP_PATH)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"cannot read Hub/repository-authority.yaml: {exc}"]

    if authority.get("schema_version") != "1.0":
        errors.append("authority map schema_version must be 1.0")
    if authority.get("kind") != "repository_authority_map":
        errors.append("authority map kind must be repository_authority_map")
    if authority.get("repository") != EXPECTED_REPOSITORY:
        errors.append(f"authority map repository must be {EXPECTED_REPOSITORY}")

    authorities = authority.get("authorities")
    if not isinstance(authorities, dict):
        return errors + ["authority map authorities must be a mapping"]

    required_paths = (
        "registry_index",
        "manifest_root",
        "registry_schema",
        "manifest_schema",
        "architecture",
        "legacy_provenance",
    )
    for key in required_paths:
        value = authorities.get(key)
        if not isinstance(value, str) or not value:
            errors.append(f"authorities.{key} must be a repository-relative path")
            continue
        _require_path(value, errors)

    artist_backend = authorities.get("artist_backend_version")
    if not isinstance(artist_backend, dict):
        return errors + ["authorities.artist_backend_version must be a mapping"]
    source = artist_backend.get("source")
    mirrors = artist_backend.get("mirrors")
    if source != "Hub/SubAgents/artist_subagent/manifest.yaml":
        errors.append("ArtistSubAgent manifest must remain the Artist backend version source")
    if not isinstance(mirrors, dict):
        return errors + ["artist_backend_version.mirrors must be a mapping"]

    if isinstance(source, str):
        _require_path(source, errors)
    for name, value in mirrors.items():
        if not isinstance(value, str) or not value:
            errors.append(f"Artist version mirror {name} must be a repository-relative path")
            continue
        _require_path(value, errors)

    external = authority.get("external_authorities")
    if not isinstance(external, dict):
        errors.append("external_authorities must be a mapping")
    else:
        for key in ("runtime_and_resolution", "public_distribution"):
            entry = external.get(key)
            if not isinstance(entry, dict) or entry.get("repository") != EXPECTED_RUNTIME_OWNER:
                errors.append(f"{key} authority must be {EXPECTED_RUNTIME_OWNER}")

    rules = authority.get("rules")
    if not isinstance(rules, dict):
        errors.append("rules must be a mapping")
    else:
        if rules.get("independent_release") is not False:
            errors.append("UnitySubAgentHub must not declare an independent public release")
        if rules.get("hub_is_runtime") is not False:
            errors.append("UnitySubAgentHub must not declare itself as Runtime")
        if rules.get("hub_is_control_plane") is not False:
            errors.append("UnitySubAgentHub must not declare itself as Control Plane")

    try:
        version = _artist_version(ROOT / "Hub/SubAgents/artist_subagent/manifest.yaml")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(str(exc))
        version = ""

    try:
        package_version = _read_json(ROOT / "Packages/com.darumappap.artist-subagent/package.json").get("version")
        if version and package_version != version:
            errors.append(f"Artist UPM package version {package_version!r} does not mirror manifest {version!r}")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        errors.append(f"Artist package.json: {exc}")

    try:
        project_text = (ROOT / "cli/artist/UnityArtist.Cli.csproj").read_text(encoding="utf-8")
        project_match = re.search(r"<Version>([^<]+)</Version>", project_text)
        project_version = project_match.group(1) if project_match else None
        if version and project_version != version:
            errors.append(f"UnityArtist.Cli.csproj version {project_version!r} does not mirror manifest {version!r}")
    except OSError as exc:
        errors.append(f"UnityArtist.Cli.csproj: {exc}")

    try:
        program_text = (ROOT / "cli/artist/Program.cs").read_text(encoding="utf-8")
        runtime_versions = re.findall(r'private const string (?:Version|SemanticVersion) = "([^"]+)";', program_text)
        if len(runtime_versions) != 2:
            errors.append("Program.cs must declare Version and SemanticVersion exactly once")
        elif version and any(value != version for value in runtime_versions):
            errors.append(f"Program.cs version constants {runtime_versions!r} do not mirror manifest {version!r}")
    except OSError as exc:
        errors.append(f"Program.cs: {exc}")

    try:
        matrix = _load_yaml(ROOT / "ci/compatibility/support-matrix.yaml")
        matrix_version = matrix.get("package_version")
        if version and matrix_version != version:
            errors.append(f"support-matrix package_version {matrix_version!r} does not mirror manifest {version!r}")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"support-matrix.yaml: {exc}")

    release_workflows = public_release_workflows(ROOT / ".github/workflows")
    if release_workflows:
        errors.append(f"Hub must not own public release workflows: {release_workflows}")

    if (ROOT / "VERSION").exists():
        errors.append("root VERSION is prohibited because Hub has no independent public release version")

    if (ROOT / "Legacy").exists():
        errors.append("Legacy source tree must not be restored to current main; use frozen provenance and Git tag v1.1.1")

    return errors


def main() -> int:
    errors = validate_repository()
    if errors:
        for error in errors:
            print(f"[ERROR] {error}")
        print(f"Repository authority validation: {len(errors)} error(s)")
        return 1
    print("Repository authority validation: 0 error(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
