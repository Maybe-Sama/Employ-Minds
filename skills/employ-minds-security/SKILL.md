---
name: employ-minds-security
description: Security and destructive-change gate for trust boundaries, auth, secrets, data, dependencies, and injection surfaces.
---
# Employ-Minds Security

Trigger for auth/authz, permissions, secrets, payments, migrations, production data, cryptography, executable dependency changes, destructive operations, or untrusted-input boundaries.

Review:
- authentication versus authorization; object/tenant ownership;
- validation and canonicalization at trust boundaries;
- SQL/NoSQL, shell, template, path traversal, SSRF and similar injection surfaces;
- prompt/tool injection when an agent can act on untrusted content;
- secret exposure in code, logs, errors, fixtures, CI and generated artifacts;
- destructive actions, idempotency, rollback, recovery and auditability;
- dependency provenance/version constraints and unsafe install hooks;
- least privilege for tokens, filesystem, network, cloud and database access;
- replay/double-submit/race conditions around money or state transitions.

Do not “fix” security by silently weakening a requirement. Material unresolved findings block CRITICAL completion.
