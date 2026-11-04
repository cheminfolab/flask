# Frontend (React + TypeScript + Vite)

Overview and setup are in the [main README](../README.md).

## Scripts

| Command | Purpose |
|---|---|
| `npm run dev` | dev server on http://localhost:3000; `/api` is proxied to the backend at `http://127.0.0.1:8000` (override with `VITE_DEV_API_TARGET`) |
| `npm test` | unit tests (Vitest) |
| `npm run lint` | ESLint (CI requires zero problems) |
| `npm run build` | type-check (`tsc -b`) and production build into `dist/` |
| `npm run gen:api` | regenerate `src/types/api.gen.ts` from `../openapi/schema.yml` |

## Structure

| Path | Contents |
|---|---|
| `src/lib/api.ts` | the single API client: attaches the access token, refreshes it once for concurrent requests, retries once after 401, builds `/resource/<id>/` URLs, turns errors into messages |
| `src/hooks/useAxios.tsx` | returns that client (kept for existing components) |
| `src/contexts/AuthContext.tsx` | login, logout, registration, current user |
| `src/types/api.gen.ts` | **generated** backend types; do not edit |
| `src/types/api.ts` | readable aliases for the generated types (`Substance`, `Experiment`, ...) |
| `src/components/ui/` | shadcn/ui components |
| `src/pages/` | routed pages |

## Working with backend types

Never write backend data types by hand. After an API change:

```bash
cd backend && python manage.py spectacular --file ../openapi/schema.yml --validate --fail-on-warn
cd ../frontend && npm run gen:api
```

then use or add an alias in `src/types/api.ts`. CI fails if `api.gen.ts` does not match the schema.

Route guards (`PrivateRoute`) only improve navigation; access control is enforced by the backend.
