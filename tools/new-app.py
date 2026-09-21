#!/usr/bin/env python3
"""Opretter en ny app i site/<app-navn>/ ud fra template/ og tilføjer den til forsiden.

Brug:
    python3 tools/new-app.py mit-app-navn "Mit App Navn"
    python3 tools/new-app.py mit-app-navn "Mit App Navn" --email hjælp@example.com --publisher "Navn"

Hænger sammen med: template/ (kilden), tools/config.json (brand, udgiver, e-mail),
site/index.html (listen mellem APPS:START og APPS:END) og tools/check.py (som bagefter tjekker resultatet).
Overskriver aldrig en eksisterende app-mappe. Kun Pythons standardbibliotek.
"""
import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
TEMPLATE = ROOT / "template"
CONFIG = ROOT / "tools" / "config.json"
RESERVED = {"assets", "template", "tools"}
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def fail(message):
    print("FEJL: " + message)
    sys.exit(1)


def load_config():
    with open(CONFIG, encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Opret en ny apps support- og privacy-sider.")
    parser.add_argument("slug", help="mappenavn og del af adressen, små bogstaver og bindestreger, fx mit-app-navn")
    parser.add_argument("name", help="appens visningsnavn, fx \"Mit App Navn\"")
    parser.add_argument("--email", help="support-e-mail (ellers bruges tools/config.json)")
    parser.add_argument("--publisher", help="udgiver-navn (ellers bruges tools/config.json)")
    args = parser.parse_args()

    config = load_config()
    email = args.email or config.get("support_email", "")
    publisher = args.publisher or config.get("publisher", "")
    brand = config.get("brand", "")

    if not SLUG_RE.match(args.slug) or args.slug in RESERVED:
        fail("mappenavnet må kun være små bogstaver, tal og bindestreger (fx mit-app-navn) og må ikke være %s" % ", ".join(sorted(RESERVED)))
    if not email or not publisher:
        fail("support-e-mail og udgiver-navn mangler. Angiv dem med --email og --publisher, eller udfyld tools/config.json.")
    if "@" not in email:
        fail("support-e-mailen ser ikke rigtig ud: " + email)

    target = SITE / args.slug
    if target.exists():
        fail("%s findes allerede. Scriptet overskriver aldrig en eksisterende app." % target.relative_to(ROOT))

    replacements = {
        "{{APP_NAME}}": html.escape(args.name),
        "{{APP_NAME_URL}}": quote(args.name),
        "{{APP_SLUG}}": args.slug,
        "{{BRAND}}": html.escape(brand),
        "{{PUBLISHER}}": html.escape(publisher),
        "{{SUPPORT_EMAIL}}": html.escape(email),
    }

    shutil.copytree(TEMPLATE, target)
    for page in target.rglob("*.html"):
        text = page.read_text(encoding="utf-8")
        for key, value in replacements.items():
            text = text.replace(key, value)
        page.write_text(text, encoding="utf-8")

    add_to_front_page(args.slug, args.name)

    print("Oprettet site/%s/ med 4 sider (dansk og engelsk) og tilføjet den til forsiden." % args.slug)
    print("")
    print("Adresser, når det er udgivet:")
    for lang in ("en", "da"):
        for page in ("support", "privacy"):
            print("  https://mjammy-inc.github.io/%s/%s/%s.html" % (args.slug, lang, page))
    print("")
    print("Næste skridt: udfyld alle gule felter ([FILL IN ...] og [UDFYLD ...]), og kør derefter:")
    print("  python3 tools/check.py")


def add_to_front_page(slug, name):
    index = SITE / "index.html"
    text = index.read_text(encoding="utf-8")
    marker = "<!-- APPS:END -->"
    if marker not in text:
        fail("site/index.html mangler linjen %s" % marker)
    item = (
        '    <li><strong>%s</strong><span>'
        '<a href="%s/en/support.html">Support</a> '
        '<a href="%s/en/privacy.html">Privacy policy</a> '
        '<a href="%s/da/support.html">Support (dansk)</a> '
        '<a href="%s/da/privacy.html">Privatlivspolitik</a>'
        "</span></li>\n"
    ) % (html.escape(name), slug, slug, slug, slug)
    index.write_text(text.replace(marker, item + marker), encoding="utf-8")


if __name__ == "__main__":
    main()
