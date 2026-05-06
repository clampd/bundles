# PostgreSQL Query Agent - Runnable Example

> **DEMO**. Throwaway code to see Clampd guarding DB queries.

Connects a Python agent to local Postgres, runs 3 queries:
1. `SELECT * FROM users LIMIT 100` → ALLOWED (within row cap)
2. `SELECT * FROM users` (10M rows) → BLOCKED (row cap exceeded)
3. `DROP TABLE users` → BLOCKED (R001 + dangerous_command keyword)

See `run.py`, `.env.example`, and `attack-fixtures/` for SQL injection / privilege escalation scenarios.

After understanding → delete the demo agent and create your real DB agent with explicit table allowlist (not `public.*`).
