#!/usr/bin/env python3
"""Stage only the public static surface for the GitHub Pages artifact."""

from pathlib import Path
import shutil


ROOT = Path(__file__).resolve().parents[1]
DESTINATION = ROOT / "_site"
PUBLIC_FILES = (
    "index.html",
    "404.html",
    "robots.txt",
    "sitemap.xml",
    "google44e5d5b1f8d82e66.html",
    "Yossef_Mohammed_Ali_CV.pdf",
)
PUBLIC_DIRECTORIES = (
    "about",
    "assets",
    "experience",
    "infrastructure",
    "projects",
    "skills",
)


def main() -> None:
    if DESTINATION.exists():
        shutil.rmtree(DESTINATION)
    DESTINATION.mkdir()

    for relative in PUBLIC_FILES:
        source = ROOT / relative
        if not source.is_file():
            raise SystemExit(f"Required public file is missing: {relative}")
        shutil.copy2(source, DESTINATION / relative)

    for relative in PUBLIC_DIRECTORIES:
        source = ROOT / relative
        if not source.is_dir():
            raise SystemExit(f"Required public directory is missing: {relative}")
        shutil.copytree(source, DESTINATION / relative)

    (DESTINATION / ".nojekyll").touch()
    files = [path for path in DESTINATION.rglob("*") if path.is_file()]
    size = sum(path.stat().st_size for path in files)
    print(f"Staged {len(files)} public files in _site ({size / 1024 / 1024:.1f} MiB).")


if __name__ == "__main__":
    main()
