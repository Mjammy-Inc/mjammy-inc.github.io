#!/usr/bin/env python3
"""Tjekker at siderne i site/ er klar til at blive udgivet. Stopper (exit 1), hvis noget er galt.

Brug:
    python3 tools/check.py             # tjekker site/
    python3 tools/check.py --site DIR  # tjekker en anden mappe (bruges til test)

Tjekker: udfyldte felter (ingen [FILL IN], [UDFYLD], TODO eller {{...}} tilbage), at hver app har alle
seks filer, at alle interne links og billeder findes, at der ingen scripts, formularer, iframes eller eksterne
ressourcer er (privacy-siderne lover det), og at der ikke ligger noget, der ligner en nøgle eller hemmelighed.

Hænger sammen med: .github/workflows/pages.yml (kører dette før udgivelse), tools/new-app.py og template/.
Kun Pythons standardbibliotek (virker på Python 3.9+).
"""
import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_APP_FILES = [
    "index.html",
    "en/support.html",
    "en/privacy.html",
    "da/support.html",
    "da/privacy.html",
]
UNFILLED_RE = re.compile(r"\{\{[A-Z_]+\}\}|\[FILL IN|\[UDFYLD|TODO")
FORBIDDEN_TAGS = {"script", "form", "iframe", "embed", "object", "input", "button", "video", "audio"}
SECRET_RES = [
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "privat nøgle"),
    (re.compile(r"\bAKIA[0-9A-Z]{16}\b"), "AWS-nøgle"),
    (re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"), "GitHub-token"),
    (re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"), "API-nøgle (sk-...)"),
    (re.compile(r"\bsk_(live|test)_[A-Za-z0-9]{10,}\b"), "Stripe-nøgle"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{10,}\b"), "JWT/login-token"),
]


class PageParser(HTMLParser):
    """Samler links, billeder og tags fra én HTML-side."""

    def __init__(self):
        super().__init__()
        self.links = []  # (attribut, værdi)
        self.tags = []
        self.lang = None
        self.title = ""
        self.has_viewport = False
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append(tag)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "title":
            self._in_title = True
        if tag == "meta" and attrs.get("name") == "viewport":
            self.has_viewport = True
        for attr in ("href", "src"):
            if attrs.get(attr):
                self.links.append((tag + " " + attr, attrs[attr]))

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def check_page(page, site, errors):
    rel = page.relative_to(site)
    text = page.read_text(encoding="utf-8")

    unfilled = UNFILLED_RE.findall(text)
    if unfilled:
        errors.append("%s: %d felt(er) er ikke udfyldt (fx %s)" % (rel, len(unfilled), unfilled[0]))

    parser = PageParser()
    parser.feed(text)
    if not parser.lang:
        errors.append("%s: mangler lang på <html>" % rel)
    if not parser.title.strip():
        errors.append("%s: mangler <title>" % rel)
    if not parser.has_viewport:
        errors.append("%s: mangler viewport (siden vil se dårlig ud på telefon)" % rel)
    for tag in sorted(set(parser.tags) & FORBIDDEN_TAGS):
        errors.append("%s: må ikke indeholde <%s> (privacy-siderne lover ingen scripts, formularer eller tracking)" % (rel, tag))

    for kind, value in parser.links:
        check_link(page, site, rel, kind, value, errors)


def check_link(page, site, rel, kind, value, errors):
    value = value.strip()
    if value.startswith(("#", "mailto:")):
        return
    if value.startswith("http://"):
        errors.append("%s: %s bruger http:// (skal være https): %s" % (rel, kind, value))
        return
    if value.startswith("https://"):
        if kind in ("link href", "img src", "source src"):
            errors.append("%s: må ikke hente %s udefra (ingen eksterne ressourcer): %s" % (rel, kind.split()[0], value))
        return
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", value):
        errors.append("%s: ukendt linktype: %s" % (rel, value))
        return
    path_part = value.split("#")[0].split("?")[0]
    if not path_part:
        return
    base = site if path_part.startswith("/") else page.parent
    target = (base / path_part.lstrip("/")).resolve()
    if path_part.endswith("/"):
        target = target / "index.html"
    if not target.exists():
        errors.append("%s: %s peger på noget, der ikke findes: %s" % (rel, kind, value))
    elif site.resolve() not in target.parents and target != site.resolve():
        errors.append("%s: %s peger uden for site/: %s" % (rel, kind, value))


def check_apps(site, errors, warnings):
    front = (site / "index.html").read_text(encoding="utf-8") if (site / "index.html").exists() else ""
    apps = [d for d in sorted(site.iterdir()) if d.is_dir() and d.name != "assets"]
    for app in apps:
        for name in REQUIRED_APP_FILES:
            if not (app / name).exists():
                errors.append("%s/: mangler %s" % (app.name, name))
        if ('href="%s/' % app.name) not in front:
            warnings.append("%s/ er ikke på forsiden (site/index.html)" % app.name)
    return apps


def check_secrets(site, errors):
    for path in list(ROOT.glob(".env*")) + list(site.rglob(".env*")):
        errors.append("%s: en .env-fil må ikke ligge i repoet" % path.relative_to(ROOT))
    scan = [p for p in site.rglob("*") if p.is_file()] + [p for p in (ROOT / "tools").glob("*") if p.is_file()]
    for path in scan:
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for pattern, label in SECRET_RES:
            if pattern.search(text):
                errors.append("%s: ligner en hemmelighed (%s). Fjern den, og lav en ny nøgle." % (path.relative_to(ROOT), label))


def main():
    parser = argparse.ArgumentParser(description="Tjek at siderne er klar til udgivelse.")
    parser.add_argument("--site", default=str(ROOT / "site"), help="mappen med siderne (standard: site/)")
    args = parser.parse_args()
    site = Path(args.site).resolve()

    errors, warnings = [], []
    for required in ("index.html", "assets/style.css", "robots.txt"):
        if not (site / required).exists():
            errors.append("site/: mangler %s" % required)

    apps = check_apps(site, errors, warnings) if site.exists() else []
    for page in sorted(site.rglob("*.html")):
        check_page(page, site, errors)
    check_secrets(site, errors)

    for warning in warnings:
        print("ADVARSEL: " + warning)
    if errors:
        print("")
        for error in errors:
            print("FEJL: " + error)
        print("")
        print("%d fejl. Ret dem, og kør checket igen. Intet bliver udgivet, før det er grønt." % len(errors))
        sys.exit(1)
    print("Alt ok. %d app(s) tjekket: %s" % (len(apps), ", ".join(a.name for a in apps) or "ingen endnu"))


if __name__ == "__main__":
    main()
