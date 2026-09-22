#!/usr/bin/env python3
"""Synchronize the resume build's PDF artifacts into a dedicated directory."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


class SyncError(ValueError):
    """Raised when the build output is not a safe, complete PDF manifest."""


def _collect_artifacts(source: Path) -> list[Path]:
    if not source.is_dir():
        raise SyncError(f"build output directory does not exist: {source}")

    artifacts = sorted(path for path in source.glob("*.pdf") if path.is_file())
    if not artifacts:
        raise SyncError(f"build output contains no PDF artifacts: {source}")

    names = {path.name for path in artifacts}
    if "cv.pdf" not in names:
        raise SyncError("build output is missing cv.pdf")
    if not any(name.startswith("resume-") for name in names):
        raise SyncError("build output is missing resume variant PDFs")

    invalid = sorted(
        name
        for name in names
        if name != "cv.pdf" and not name.startswith("resume-")
    )
    if invalid:
        raise SyncError(
            "build output contains unexpected PDF artifacts: " + ", ".join(invalid)
        )

    return artifacts


def sync_pdfs(source: Path, destination: Path) -> list[str]:
    """Copy the current PDF manifest and remove stale PDFs from destination.

    The source manifest is validated before the destination is created or
    changed. Only files ending in ``.pdf`` are removed from the destination;
    other site assets are left untouched.
    """

    source = source.resolve()
    destination = destination.resolve()
    artifacts = _collect_artifacts(source)

    if source == destination:
        raise SyncError("build output and destination must be different directories")

    destination.mkdir(parents=True, exist_ok=True)
    existing_pdfs = sorted(destination.glob("*.pdf"))
    non_files = [path for path in existing_pdfs if not path.is_file()]
    if non_files:
        names = ", ".join(path.name for path in non_files)
        raise SyncError(f"destination contains non-file PDF paths: {names}")

    for path in existing_pdfs:
        path.unlink()
    for artifact in artifacts:
        shutil.copy2(artifact, destination / artifact.name)

    return [artifact.name for artifact in artifacts]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Synchronize CV and resume variant PDFs into a site directory."
    )
    parser.add_argument("source", type=Path, help="directory containing built PDFs")
    parser.add_argument("destination", type=Path, help="dedicated PDF destination")
    args = parser.parse_args()

    try:
        names = sync_pdfs(args.source, args.destination)
    except SyncError as error:
        parser.error(str(error))

    for name in names:
        print(f"synced {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
