# route-api (deprecated / disabled)

This folder is retained only as a historical backup of the former Google Cloud Run / Firestore / Google Routes implementation.

## Current production architecture

ぷらっと東海 now runs in free static mode on GitHub Pages.

- Production UI: `index.html`, `new-pan.html`
- Data: repository static JSON under `data/`
- PWA: `manifest.webmanifest`, `sw.js`
- Automatic Cloud Run deployment: disabled
- Automatic Places audit using the old Cloud Run endpoint: disabled

The default `npm start` command does **not** launch this API.
For historical inspection only, the old server can be started explicitly with `npm run start:legacy`.

Do not reconnect this service to production without a deliberate architecture review and explicit approval.
