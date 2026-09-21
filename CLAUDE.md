# mjammy-inc.github.io

## Om projektet
Ét fælles repo med alle vores apps offentlige support- og privacy-sider, som Apple kræver i App Store Connect. Hver app får sin egen mappe med support og privacy på dansk og engelsk. Siderne udgives gratis via GitHub Pages på `https://mjammy-inc.github.io/<app>/...`.

## Tech stack
- Almindelig HTML og CSS, ingen frameworks, ingen JavaScript, ingen cookies, ingen tracking
- Fælles design i `site/assets/style.css`
- To små Python-scripts (kun standardbibliotek): `tools/new-app.py` og `tools/check.py`
- Udgivelse: GitHub Actions (`.github/workflows/pages.yml`) uploader kun mappen `site/`

## Regler for Claude
- Opdater altid overview.md, når der sker en strukturel ændring i projektet (nye filer, nye moduler/services, ændret arkitektur) uden at blive bedt om det.
- **Omdøb ALDRIG dette repo eller GitHub-organisationens brugernavn (`Mjammy-Inc`).** Adresserne er indtastet hos Apple, og Apple kan kun få dem rettet ved at sende en ny app-version ind. Brandet og teksten på siderne kan ændres frit.
- **Ændr aldrig en apps mappenavn eller filnavne, efter appen er sendt til Apple.** Adressen ligger fast.
- Ny app: kør `python3 tools/new-app.py`, udfyld alle markerede felter, kør `python3 tools/check.py`. Arbejd på en gren (branch), og flet først til `main`, når checket er grønt. Udgivelsen kører `check.py` og stopper, hvis noget mangler, så en halvfærdig privacy policy aldrig kommer live.
- Privacy-teksten skal passe til, hvad den konkrete app faktisk gør, og til svarene i App Privacy i App Store Connect. Skriv aldrig noget, der ikke er sandt. Det er ikke juridisk rådgivning.
- Læg aldrig nøgler, passwords eller andre hemmeligheder her. Repoet er offentligt. `.env` står i `.gitignore`.
- Spørg før: gøre repoet offentligt, slå Pages til, pushe til `main`, omdøbe eller slette noget.
- Tilføj ikke scripts, formularer, iframes, analytics, cookies eller eksterne ressourcer til siderne uden en ny beslutning. Privacy-siderne lover, at der ingen er, og `check.py` fejler, hvis der er.
- Se `../mjammy-vibecode-headquarters/beslutninger.md` (2026-09-21) for hvorfor strukturen er valgt.
