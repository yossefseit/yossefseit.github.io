#!/usr/bin/env python3
"""Dependency-free structural checks for the static portfolio."""

from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
PRIMARY_ORIGIN = "https://gentle-smoke-06d712d0f.7.azurestaticapps.net"
LOCAL_ATTRIBUTES = {
    "a": ("href",),
    "img": ("src",),
    "link": ("href",),
    "script": ("src",),
    "source": ("src",),
}

errors: list[str] = []
checked_references = 0


def fail(message: str) -> None:
    errors.append(message)


class SiteHTMLParser(HTMLParser):
    def __init__(self, source: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.source = source
        self.ids: set[str] = set()
        self.references: list[tuple[str, str]] = []
        self.h1_count = 0
        self.lang = ""
        self.title = ""
        self.description = ""
        self.viewport = ""
        self.canonical = ""
        self.metadata: dict[str, str] = {}
        self.images: list[dict[str, str]] = []
        self._capture_title = False
        self._json_ld_buffer: list[str] | None = None
        self.json_ld_blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs_list: list[tuple[str, str | None]]) -> None:
        attrs = {name: value or "" for name, value in attrs_list}

        element_id = attrs.get("id")
        if element_id:
            if element_id in self.ids:
                fail(f"{self.source.relative_to(ROOT)}: duplicate id #{element_id}")
            self.ids.add(element_id)

        if tag == "html":
            self.lang = attrs.get("lang", "")
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "title":
            self._capture_title = True
        elif tag == "meta" and attrs.get("name", "").lower() == "description":
            self.description = attrs.get("content", "").strip()
        elif tag == "meta" and attrs.get("name", "").lower() == "viewport":
            self.viewport = attrs.get("content", "").strip()
        elif tag == "meta" and (attrs.get("name") or attrs.get("property")):
            metadata_key = (attrs.get("name") or attrs.get("property") or "").lower()
            self.metadata[metadata_key] = attrs.get("content", "").strip()
        elif tag == "link" and attrs.get("rel", "").lower() == "canonical":
            self.canonical = attrs.get("href", "").strip()
        elif tag == "img":
            self.images.append(attrs)
            if "alt" not in attrs:
                fail(f"{self.source.relative_to(ROOT)}: image is missing an alt attribute")
            if not attrs.get("width") or not attrs.get("height"):
                fail(f"{self.source.relative_to(ROOT)}: image is missing width or height")
        elif tag == "style":
            fail(f"{self.source.relative_to(ROOT)}: inline <style> is not allowed")
        elif tag == "script":
            script_type = attrs.get("type", "").lower()
            if script_type == "application/ld+json":
                self._json_ld_buffer = []
            elif not attrs.get("src"):
                fail(f"{self.source.relative_to(ROOT)}: executable inline script is not allowed")

        if tag == "div" and ("aria-label" in attrs or "aria-labelledby" in attrs) and not attrs.get("role"):
            fail(
                f"{self.source.relative_to(ROOT)}: labelled div requires an explicit semantic role"
            )

        if tag == "a" and attrs.get("target") == "_blank":
            rel_tokens = set(attrs.get("rel", "").lower().split())
            missing = {"noopener", "noreferrer"} - rel_tokens
            if missing:
                fail(
                    f"{self.source.relative_to(ROOT)}: target=_blank link is missing "
                    f"{', '.join(sorted(missing))}"
                )

        for attribute in LOCAL_ATTRIBUTES.get(tag, ()):
            value = attrs.get(attribute)
            if value:
                self.references.append((attribute, value))

        srcset = attrs.get("srcset")
        if srcset:
            for candidate in srcset.split(","):
                path = candidate.strip().split()[0]
                if path:
                    self.references.append(("srcset", path))

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._capture_title = False
        elif tag == "script" and self._json_ld_buffer is not None:
            self.json_ld_blocks.append("".join(self._json_ld_buffer))
            self._json_ld_buffer = None

    def handle_data(self, data: str) -> None:
        if self._capture_title:
            self.title += data
        if self._json_ld_buffer is not None:
            self._json_ld_buffer.append(data)


def resolve_local_reference(source: Path, raw_reference: str) -> Path | None:
    parsed = urlparse(raw_reference)
    if parsed.scheme in {"http", "https", "mailto", "tel", "data"} or raw_reference.startswith("//"):
        return None

    path_text = unquote(parsed.path)
    if not path_text:
        return source

    if path_text == "/":
        return ROOT / "index.html"

    if path_text.startswith("/"):
        candidate = ROOT / path_text.lstrip("/")
    else:
        candidate = source.parent / path_text

    try:
        candidate = candidate.resolve()
        candidate.relative_to(ROOT)
    except (OSError, ValueError):
        fail(f"{source.relative_to(ROOT)}: reference escapes repository root: {raw_reference}")
        return None

    if candidate.is_dir():
        candidate /= "index.html"
    return candidate


def validate_html(source: Path) -> None:
    global checked_references

    parser = SiteHTMLParser(source)
    try:
        parser.feed(source.read_text(encoding="utf-8"))
        parser.close()
    except Exception as exc:  # HTMLParser errors are rare, but should fail CI clearly.
        fail(f"{source.relative_to(ROOT)}: parser failure: {exc}")
        return

    relative = source.relative_to(ROOT)
    if parser.lang != "en":
        fail(f"{relative}: expected html lang=\"en\"")
    if parser.h1_count != 1:
        fail(f"{relative}: expected exactly one h1, found {parser.h1_count}")
    if not parser.title.strip():
        fail(f"{relative}: missing document title")
    elif len(parser.title.strip()) > 70:
        fail(f"{relative}: title exceeds 70 characters")
    if not parser.viewport:
        fail(f"{relative}: missing viewport meta tag")

    if relative == Path("404.html"):
        if parser.canonical:
            fail(f"{relative}: 404 page should not declare a canonical URL")
    else:
        if not 80 <= len(parser.description) <= 170:
            fail(f"{relative}: meta description should be 80–170 characters")
        route = "/" if relative == Path("index.html") else f"/{relative.parent.as_posix()}/"
        expected_canonical = f"{PRIMARY_ORIGIN}{route}"
        if parser.canonical != expected_canonical:
            fail(f"{relative}: canonical URL should be {expected_canonical}")
        required_social_metadata = (
            "og:title",
            "og:description",
            "og:url",
            "og:image",
            "og:image:alt",
            "twitter:card",
            "twitter:title",
            "twitter:description",
            "twitter:image",
        )
        for metadata_key in required_social_metadata:
            if not parser.metadata.get(metadata_key):
                fail(f"{relative}: missing social metadata {metadata_key}")
        if parser.metadata.get("og:url") != expected_canonical:
            fail(f"{relative}: og:url should be {expected_canonical}")

    for block_number, block in enumerate(parser.json_ld_blocks, start=1):
        try:
            json.loads(block)
        except json.JSONDecodeError as exc:
            fail(f"{relative}: invalid JSON-LD block {block_number}: {exc}")

    if relative == Path("projects/azure-secure-hub-spoke/index.html"):
        architecture_images = [
            image for image in parser.images
            if image.get("src", "").endswith("azure-secure-hub-spoke.svg")
        ]
        if len(architecture_images) != 1:
            fail(f"{relative}: expected one optimized SVG architecture image")
        elif architecture_images[0].get("loading") != "lazy":
            fail(f"{relative}: below-the-fold architecture image must load lazily")

    for attribute, reference in parser.references:
        parsed = urlparse(reference)
        if parsed.path == "" and parsed.fragment:
            if parsed.fragment not in parser.ids:
                fail(f"{relative}: missing in-page target #{parsed.fragment}")
            continue

        if (
            relative != Path("index.html")
            and parsed.path
            and not parsed.path.startswith("/")
            and not parsed.scheme
        ):
            fail(f"{relative}: local runtime reference must be root-relative: {reference}")

        local_path = resolve_local_reference(source, reference)
        if local_path is None:
            continue

        checked_references += 1
        if not local_path.exists():
            fail(f"{relative}: {attribute} references missing file {reference}")

        if parsed.fragment and local_path.suffix.lower() == ".html" and local_path.exists():
            target_parser = SiteHTMLParser(local_path)
            target_parser.feed(local_path.read_text(encoding="utf-8"))
            if parsed.fragment not in target_parser.ids:
                fail(f"{relative}: {reference} points to a missing fragment")


def validate_css(source: Path) -> None:
    global checked_references

    css = source.read_text(encoding="utf-8")
    for raw_reference in re.findall(r"url\(\s*['\"]?([^'\"\)]+)", css):
        local_path = resolve_local_reference(source, raw_reference.strip())
        if local_path is None:
            continue
        checked_references += 1
        if not local_path.exists():
            fail(f"{source.relative_to(ROOT)}: url() references missing file {raw_reference}")


def validate_configuration() -> None:
    config_path = ROOT / "staticwebapp.config.json"
    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"staticwebapp.config.json: invalid JSON: {exc}")
        return

    headers = {key.lower(): value for key, value in config.get("globalHeaders", {}).items()}
    csp = headers.get("content-security-policy", "")
    if "'unsafe-inline'" in csp or "'unsafe-eval'" in csp:
        fail("staticwebapp.config.json: CSP contains an unsafe script/style directive")
    for directive in ("default-src", "script-src", "style-src", "object-src", "frame-ancestors"):
        if directive not in csp:
            fail(f"staticwebapp.config.json: CSP is missing {directive}")

    index_source = (ROOT / "index.html").read_text(encoding="utf-8")
    json_ld_match = re.search(
        r'<script type="application/ld\+json">([\s\S]*?)</script>',
        index_source,
    )
    if not json_ld_match:
        fail("index.html: JSON-LD block was not found for CSP validation")
    else:
        digest = base64.b64encode(
            hashlib.sha256(json_ld_match.group(1).encode("utf-8")).digest()
        ).decode("ascii")
        expected_hash = f"'sha256-{digest}'"
        if expected_hash not in csp:
            fail("staticwebapp.config.json: CSP hash does not match the JSON-LD block")
    for header in (
        "content-security-policy",
        "permissions-policy",
        "referrer-policy",
        "strict-transport-security",
        "x-content-type-options",
    ):
        if header not in headers:
            fail(f"staticwebapp.config.json: missing security header {header}")

    override = config.get("responseOverrides", {}).get("404", {})
    if override.get("rewrite") != "/404.html":
        fail("staticwebapp.config.json: 404 response must rewrite to /404.html")


def validate_sitemap_and_robots() -> None:
    sitemap_path = ROOT / "sitemap.xml"
    try:
        tree = ElementTree.parse(sitemap_path)
    except (OSError, ElementTree.ParseError) as exc:
        fail(f"sitemap.xml: invalid XML: {exc}")
        return

    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = [node.text or "" for node in tree.findall(".//s:loc", namespace)]
    expected = [
        f"{PRIMARY_ORIGIN}/",
        f"{PRIMARY_ORIGIN}/projects/",
        f"{PRIMARY_ORIGIN}/projects/azure-secure-hub-spoke/",
    ]
    if locations != expected:
        fail(f"sitemap.xml: expected {expected}")
    if any("#" in location for location in locations):
        fail("sitemap.xml: fragment URLs are not indexable documents")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    expected_sitemap = f"Sitemap: {PRIMARY_ORIGIN}/sitemap.xml"
    if expected_sitemap not in robots:
        fail("robots.txt: sitemap URL does not match the production origin")


def main() -> int:
    html_files = sorted(
        path
        for path in ROOT.rglob("*.html")
        if path.name != "google44e5d5b1f8d82e66.html" and ".git" not in path.parts
    )
    for html_file in html_files:
        validate_html(html_file)
    for css_file in sorted((ROOT / "assets").glob("*.css")):
        validate_css(css_file)

    validate_configuration()
    validate_sitemap_and_robots()

    required_files = (
        "assets/cv.pdf",
        "assets/og-cover.png",
        "assets/favicon.svg",
        "assets/site.css",
        "assets/site.js",
        "assets/azure-secure-hub-spoke.svg",
        "assets/azure-secure-hub-spoke.png",
        "projects/index.html",
        "projects/azure-secure-hub-spoke/index.html",
        "infra/main.bicep",
    )
    for relative in required_files:
        if not (ROOT / relative).is_file():
            fail(f"required file is missing: {relative}")

    if errors:
        print(f"Site validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(
        f"Site validation passed: {len(html_files)} HTML documents and "
        f"{checked_references} local references checked."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
