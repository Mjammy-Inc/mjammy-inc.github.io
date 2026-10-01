# Overview

Opdateres, hver gang strukturen ændres. Se `CLAUDE.md` for regler.

## Repoopdeling
Hver app har ét selvstændigt kode-repo med egne tests og byggeopsætning. Dette fælles repo indeholder de offentlige support- og privacy-sider. Et særskilt kode-repo flytter ikke appens eksisterende Apple-URLer.

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
  check.py               Kontrollerer udfyldte felter, interne filer/links og udvalgte forbudte tags/nøglemønstre
.github/workflows/pages.yml   PR-kontrol; manuel Pages-udgivelse af godkendt main-version
```

## Adresser
`https://mjammy-inc.github.io/<app-navn>/<sprog>/support.html` og `.../privacy.html`, hvor sprog er `en` eller `da`. Adresserne må aldrig ændres, når en app er sendt til Apple.

## Apps i repoet
Ingen appmapper i `site/` ved kontrollen 1. oktober 2026. Subleafs eksisterende support- og privacy-sider ligger stadig i hans eget repo (`Krissydevelops/krissydevelops.github.io`) og flyttes først, når han og Matteo siger til.

## Status
Kontrolleret 1. oktober 2026: repoet er offentligt og hjemmesiden er tilgængelig. GitHub Actions gennemførte kontrol og Pages-deployment 30. september 2026 (kørsel 36762240070). Loggen viste 0 kontrollerede apps. Det dokumenterer fungerende sidekontrol og deployment, ikke færdige app-sider.

Udgiver og standard support-e-mail i `tools/config.json` er endnu ikke udfyldt.

Pull requests kører kontrol. Offentlig deployment kræver efter denne opsætning en manuel kørsel på `main` med `publish` valgt og en konkret godkendelse fra slutreview.

`check.py` kontrollerer statiske filer og udvalgte mønstre. Visuel brugervenlighed, faktisk privacy-adfærd, maillevering og appens funktioner kontrolleres særskilt.
