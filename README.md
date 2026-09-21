# mjammy-inc.github.io

Support- og privacy-sider til vores apps (kræves af Apple i App Store Connect).

## Ny app på 3 trin
1. `python3 tools/new-app.py mit-app-navn "Mit App Navn"` opretter `site/mit-app-navn/` med fire sider (dansk og engelsk).
2. Udfyld alle felter markeret `[FILL IN ...]` eller `[UDFYLD ...]` (de er gule, når du åbner siderne).
3. `python3 tools/check.py` skal sige "Alt ok", før noget flettes til `main`.

Læs `CLAUDE.md` for reglerne, især at navne og adresser ikke må ændres efter Apple har dem.

## Se siderne lokalt
```bash
cd site && python3 -m http.server 8000
```
Åbn derefter http://localhost:8000 i en browser.
