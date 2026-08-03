# DevMind frontend

React and Vite client for DevMind.

## Local development

```powershell
npm install
Copy-Item .env.example .env.local
npm run dev
```

`VITE_API_BASE_URL` is public browser configuration. Never place database
credentials, JWT secrets, or AI-provider keys in this directory.

## Validation

```powershell
npm run typecheck
npm run lint
npm run build
```

