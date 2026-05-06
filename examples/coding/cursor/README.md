# Cursor IDE Agent — Runnable Example

> **This is a DEMO**. It exists to help you see Clampd in action. Don't ship this code to production — write your own integration once you understand the flow.

## What this shows

Three things, in 45 seconds:
1. A simulated Cursor agent makes 3 file-write requests through Clampd
2. Two requests succeed (writing to project root)
3. One request gets blocked (writing to `~/.ssh/authorized_keys`) — Clampd alert visible in dashboard

## Prerequisites

- Python 3.10+
- A Clampd dashboard account with the `coding/cursor` bundle enabled
- Your demo agent's API key (shown after enabling the bundle)

## Run

```bash
git clone https://github.com/clampd/bundles
cd bundles/examples/coding/cursor

cp .env.example .env
# paste your API key into .env

pip install clampd
python run.py
```

Expected output:
```
[1/3] write README.md to project root          → ALLOWED  (200 OK)
[2/3] write src/auth.py to project root        → ALLOWED  (200 OK)
[3/3] write ~/.ssh/authorized_keys             → BLOCKED  (403 — boundary_allowlist + R109)
```

Open your dashboard → Audit page → see the blocked request with full reason chain.

## Trying the attack fixtures

`attack-fixtures/` has 5 more scenarios that should each get blocked:

```bash
python run.py --fixture .env-leak
python run.py --fixture rm-rf
python run.py --fixture git-force-push
python run.py --fixture aws-creds-write
python run.py --fixture eval-input
```

Each maps to a specific rule. Watch the dashboard to see which rule fired.

## After you understand the flow

**Delete the demo agent** (dashboard → Agents → cursor-demo → Delete) and create your real agent with:
- Your team's actual scope grants (probably narrower than demo)
- Your project's specific allowlist patterns
- Your real boundary thresholds

The bundle's rules + keywords + protected entities apply org-wide regardless of which agent triggered them. Demo agent goes away; protection stays.
