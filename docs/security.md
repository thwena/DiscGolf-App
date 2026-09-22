# Security model

- Production startup rejects secrets shorter than 32 characters.
- Initial administrator creation requires a separate bootstrap token and is permanently disabled once any user exists.
- Passwords are hashed with pwdlib's current recommended Argon2 configuration.
- Access tokens are short-lived, signed, and validated by the application. Token revocation and refresh-token rotation are required before public release.
- Every future resource query must scope ownership or round membership in the query itself; knowing an object ID is never authorization.
- OIDC identities will bind `(provider, subject)` to an internal UUID. Unverified or matching email addresses will not auto-link accounts.
- The application expects HTTPS at an operator-provided reverse proxy. Trusted hostnames must be configured explicitly.
- Uploaded files will require size/type validation and generated storage names before uploads are enabled.

Do not commit `.env`, databases, exports, uploads, tokens, or real user data. Remove the bootstrap token after first-user creation.
