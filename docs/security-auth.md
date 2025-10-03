
# Security & Auth

- **OIDC (Auth0/Keycloak)**: JWT access tokens validated via JWKS (gateway).
- **SSE proxy**: `/api/sse` keeps tokens in cookies; no query tokens.
- **Simulate proxy**: `/api/simulate` forwards securely to gateway.
- **Secrets**: Kubernetes Secrets & restricted RBAC.
- **Audit**: events JSONL and Prometheus metrics for traceability.
