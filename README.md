# mjammy-inc.github.io

Fælles offentlige support- og privacy-sider til MJAMMYs apps.

## Repoer og ansvar

Hver app har ét særskilt repo til sin kode, tests og byggeopsætning. Dette repo samler de offentlige support- og privacy-sider: én mappe pr. app under `site/`, på dansk og engelsk.

Appkode og tests hører i appens private kode-repo. Byggede apps opbevares i de godkendte buildtjenester. Adgangskoder, tokens og private nøgler opbevares kun i tjenesternes sikre opbevaring og gemmes aldrig i Gitrepoer. Repoets navn, organisationens navn og eksisterende Apple-adresser bevares.

## Status

Kontrolleret 1. oktober 2026: repoet er offentligt, og hjemmesiden er tilgængelig. GitHub Actions gennemførte kontrol og Pages-deployment 30. september. Der er endnu ingen appmapper i `site/`; kontrollen gennemgik 0 apps.

Udgiver og standard support-e-mail i `tools/config.json` er endnu ikke udfyldt. De skal aftales eller angives eksplicit pr. app.

## Ny app på 3 trin

1. Kør `python3 tools/new-app.py mit-app-navn "Mit App Navn"`. Angiv den aftalte supportadresse og udgiver med `--email` og `--publisher`, hvis de ikke er udfyldt i `tools/config.json`.
2. Udfyld alle felter markeret `[FILL IN ...]` eller `[UDFYLD ...]`. Kontrollér teksten mod appens faktiske data, køb, notifikationer og tjenester.
3. Kør `python3 tools/check.py`, og opret en pull request. Kontrollen skal være grøn før sammenfletning.

## Review og udgivelse

Pull requests kører sidekontrol. En merge til `main` publicerer ikke automatisk efter denne opsætning.

Efter godkendt slutreview kan `Check and deploy to Pages` køres manuelt på `main` med `publish` valgt. Uden tilvalget udføres kun kontrollen. Gem hvilken version og hvilke sider godkendelsen omfatter. Det manuelle tilvalg er ikke i sig selv bevis på menneskelig godkendelse.

Læs `CLAUDE.md` for reglerne, især at navne og adresser ikke må ændres efter Apple har dem.

## Se siderne lokalt
```bash
cd site && python3 -m http.server 8000
```
Åbn derefter http://localhost:8000 i en browser.
