# DevilSec Website

> **Note:** The website is currently under active development as it is being fully redesigned.

This repository contains the main DevilSec website.


## Development
### Repository Setup
- `git clone https://github.com/devilsec/website.git`/`git clone git@github.com:devilsec/website.git`
- `cd website`
- `npm install`

### Running
- `npm run watch` / `npm run start`
- Vist the generated site at [http://localhost:8080/](http://localhost:8080/).

### Linting

- Lint JS: `npm run lint-js`
- Lint CSS/SCSS: `npm run lint-css`
- Lint all code files: `npm run lint`

#### To apply the linting configuration and fix the file formatting:

- Apply JS linting: `npm run fix-js`
- Apply CSS/SCSS linting: `npm run fix-css`
- Apply linting for all code files: `npm run lint-fix`

### Building
- `npm run build`
- Visit the generated site in the `dist/` directory.
