# Connor Schaaf portfolio

Static website centered on Unreal Blueprints and game design documentation.

## Editing

- `scripts/project_content.json` contains project descriptions, contribution statements, and credits.
- `scripts/profile_content.json` contains Connor’s introduction and About-page wording.
- `scripts/build_portfolio.py` contains the shared HTML templates, page layouts, and media links.
- `css/style.css` and `js/main.js` contain styling and small interactions.
- `assets/site` contains selected web media. `assets/docs` contains the full Locomotion GDD, Hope technical requirements, and four standalone documentation samples.

Run `python scripts/build_portfolio.py` to update the root HTML pages and the deployable `dist` folder. Serve `dist` with `python -m http.server 4173 --directory dist`.

## Content

The portfolio includes Locomotion, Project: Hope, Mags & Magic, and The Trials of the Arcane Academy. The Documents page includes six game design and technical documentation samples. Team artwork and footage are credited alongside specific contribution statements.

The résumé was replaced with the supplied `Connor_Schaaf_Resume_Final.pdf` on November 6, 2026. Published PDFs are unchanged copies of the supplied files. Local research, personal downloads, credentials, and working archives are excluded from this repository.

## Hosting

GitHub Pages publishes the root of the `main` branch at https://schaafconnor0-collab.github.io/ConnorSchaafPortfolio/. The renderer uses that address for canonical links and social-preview images. Rebuild and commit both the source files and generated HTML when updating the portfolio.
