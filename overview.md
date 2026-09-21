# Overview

Opdateres, hver gang strukturen ændres. Se `CLAUDE.md` for regler.

## Mappestruktur
```
site/                    Det eneste, der udgives på nettet
  index.html             Forside med liste over apps (mellem APPS:START og APPS:END)
  robots.txt
  assets/style.css       Fælles design til alle sider
  <app-navn>/            Én mappe pr. app (oprettes af tools/new-app.py)
    index.html           Lille app-side med links
    en/support.html      Engelsk support
    en/privacy.html      Engelsk privacy policy
    da/support.html      Dansk support
    da/privacy.html      Dansk privacy policy
template/                Skabelon, som new-app.py kopierer fra (udgives ikke)
tools/
  config.json            Brand-navn, udgiver og standard support-e-mail
  new-app.py             Opretter en ny app-mappe ud fra skabelonen
  check.py               Tjekker at alt er udfyldt, links virker, og der ingen scripts/tracking er
.github/workflows/pages.yml   Kører check.py og udgiver site/ til GitHub Pages
```

## Adresser
`https://mjammy-inc.github.io/<app-navn>/<sprog>/support.html` og `.../privacy.html`, hvor sprog er `en` eller `da`. Adresserne må aldrig ændres, når en app er sendt til Apple.

## Apps i repoet
Ingen endnu. Kristoffers Subleaf ligger stadig i hans eget repo (`Krissydevelops/krissydevelops.github.io`) og flyttes først, når han og Matteo siger til.

## Status
Bygget lokalt og testet. Repoet er privat. Pages er IKKE slået til endnu (kræver offentligt repo og Matteos ok).
