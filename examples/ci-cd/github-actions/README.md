# GitHub Actions - Runnable Example

> **DEMO**. Helps you see Clampd catching CI agent failure modes. Don't ship this workflow to production unchanged.

A workflow that runs an AI-driven release agent against Clampd. 3 scenarios:
1. Tag a release from the trusted workflow path → ALLOWED
2. Try to tag a release from a feature branch's workflow → BLOCKED (trusted_publisher policy)
3. Reference an unpinned third-party action → BLOCKED (no-third-party policy)

See `workflow.yml` and `attack-fixtures/` for the scenarios. Wire the demo agent's API key into the repo's secrets as `CLAMPD_API_KEY`.

After understanding the flow → delete the demo agent and create your real CI agent with your team's actual repo allowlist.
