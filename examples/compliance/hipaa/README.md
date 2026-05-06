# HIPAA - Runnable Example

> **DEMO ONLY**. This does NOT make your stack HIPAA-compliant. Real HIPAA needs a signed BAA, full risk assessment, and your audit-log retention configured.

A Python agent simulating a clinical Q&A bot. 3 scenarios:
1. Question without PHI: "What are common diabetes symptoms?" → ALLOWED
2. Question with PHI: "Patient John Doe, MRN: 123456, has..." → FLAGGED + redacted in audit
3. Attempt to send PHI to a non-BAA endpoint → BLOCKED (deny_phi_to_third_party policy)

See `run.py` for the integration pattern.

After understanding → delete the demo agent. Real HIPAA setup requires:
- Signed BAA with your LLM provider (OpenAI, Anthropic, etc.)
- `baa_allowlist` populated with ONLY your covered endpoints
- Audit log retention ≥6 years per HIPAA §164.316(b)(2)
- Your full risk assessment per §164.308(a)(1)(ii)(A)
