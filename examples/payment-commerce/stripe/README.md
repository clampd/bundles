# Stripe Payment Agent - Runnable Example

> **DEMO**. Use Stripe TEST keys only (sk_test_*). The bundle blocks live keys for the demo agent.

A Python agent that initiates 3 Stripe charges through Clampd:
1. $5 charge to a verified vendor → ALLOWED
2. $1500 charge → BLOCKED (above human-in-loop threshold)
3. $5 charge to an unverified recipient → BLOCKED (recipient_allowlist)

See `run.py` and `attack-fixtures/` for refund-abuse / payout-redirection scenarios.

After understanding → delete the demo agent. Your real payment agent must:
- Use a separate API key with narrower scopes
- Have a human-curated `verified_recipients` list
- Configure `human_required_above_cents` per your risk tolerance
