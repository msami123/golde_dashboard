# Smart Gold Landing Page

Premium fintech-style marketing page for the Smart Gold portfolio app.

## Stack

- React 18 + TypeScript + Vite
- Tailwind CSS
- lucide-react icons

## Development

```bash
cd landing
npm install
npm run dev
```

Open http://localhost:5173 — CTAs link to `/login` on the Flask app.

## Production build

```bash
cd landing
npm run build
```

Flask serves `landing/dist` at `/` for visitors. Logged-in users are redirected to `/dashboard`.

## Fonts

Add TT Norms Pro files to `public/fonts/`:

- `tt-norms-pro-regular.woff2` (400)
- `tt-norms-pro-semibold.woff2` (600)

Until then, the page uses system UI fallbacks.
