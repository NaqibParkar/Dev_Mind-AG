# Security

## Reporting

Please report security issues privately to the repository owner instead of
opening a public issue containing credentials or exploit details.

## Secret handling

- Keep database URLs, JWT secrets, and provider keys out of Git.
- Store local secrets in ignored `.env` files.
- Store production secrets in the deployment platform's secret manager.
- Treat every `VITE_*` value as public browser configuration.
- Rotate a credential immediately if it is committed, logged, or shared.

## Required repository cleanup

The Neon database credential and a database file existed in earlier commits.
Before considering the incident resolved:

1. Rotate the Neon password and review database access logs.
2. Rewrite Git history to remove the credential, `Backend/devmind.db`, and
   `Backend/.venv`.
3. Force-push the cleaned branches and tags.
4. Ask collaborators to delete old clones and clone the repository again.

History rewriting should happen only after the current file changes have been
reviewed and all collaborators have been notified.

