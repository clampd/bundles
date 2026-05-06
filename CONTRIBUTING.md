# Contributing to Clampd Bundles

Thanks for wanting to add a bundle. This is a public, Apache-2.0 repo - every bundle here is reused by Clampd customers around the world. Read this before opening a PR.

## What's a "bundle"?

A bundle is a curated, reusable set of detection rules + keywords + a demo agent + policy templates that targets one specific AI agent type, framework, or compliance regime. A bundle is NOT:
- A custom org-specific config (use the dashboard for that)
- A new built-in rule (rules live in `clampd/services` - see that repo's CONTRIBUTING)
- A keyword list alone (use a CSV in `bundles/<category>/_shared/`)

## Scope of a good bundle

Yes:
- **Cursor IDE Agent** - a specific tool with known failure modes
- **GitHub Actions CI** - a specific platform with attack patterns
- **HIPAA** - a regulation with specific PHI definitions
- **Stripe Payment Agent** - a vendor with specific risks

No:
- "Generic LLM rules" - too vague
- "All AI agents" - that's the global default, not a bundle
- A duplicate of something already in `bundles/`

## Required files per PR

Every bundle PR must include all of:

```
bundles/<category>/<bundle-id>.json   # the bundle file (validates against schema/bundle.v1.1.schema.json)
examples/<category>/<bundle-id>/      # runnable demo
  ├── README.md                       # 3-step quickstart
  ├── .env.example                    # config template
  └── run.<ext>                       # working code, <100 LOC
```

If your category doesn't exist yet:
```
bundles/<category>/_category.json     # category defaults
```

## Bundle field requirements

| Field | Required | Notes |
|---|---|---|
| `schema_version` | yes | Must be `"1.1"` |
| `id` | yes | Format `<category>/<name>`. Must match file location. |
| `name` | yes | Human-readable. 3-80 chars. |
| `version` | yes | Semver. New PRs ship as `1.0.0`. |
| `status` | yes | New PRs MUST be `experimental`. CI blocks `stable`. |
| `description` | yes | 30-500 chars. Describe what the bundle catches. |
| `references` | recommended | Vendor docs, OWASP entries, CVEs, research. |
| `rules.rule_ids` | yes | Must reference real `R0xx` IDs in BUILTIN_RULES. CI checks. |
| `keywords.inline` | recommended | Bundle-specific keywords. Avoid duplicating shared lists. |
| `demo_agents` | yes | At least one. Name MUST end in `-demo`. `purpose: "onboarding"` const. |
| `policy_templates` | recommended | Cedar templates with parameters customers fill in. |
| `protected_entities` | recommended | Internal paths, domains, wallet addresses worth defending. |
| `false_positives` | yes | Document at least the known FPs. Empty array is allowed but discouraged. |
| `backtest_hints` | recommended | Help dashboards run reasonable backtests. |

## Demo agents - what they're for

Demo agents exist to help **new users** see Clampd working end-to-end in 30-45 seconds. They are NOT production templates.

Required:
- Name ends in `-demo` (e.g. `cursor-demo`, `postgres-demo`)
- `purpose: "onboarding"` (const)
- Description explicitly says "NOT for production"
- Example integration link to your bundle's `examples/` directory

When a customer enables your bundle, the dashboard will offer to create a demo agent. After learning, the customer creates their REAL agent separately with their actual scopes and allowlist patterns.

## Local validation

Before you open a PR:

```bash
pip install jsonschema
python3 tools/validate.py        # schema + cross-checks
python3 tools/gen-manifest.py    # regenerate manifest.json
git diff manifest.json           # only sha256 + version line should change
```

CI runs the same checks plus:
- `rule_ids` exist in BUILTIN_RULES (services repo lookup)
- `taxonomy` enums match `rule_schema.json`
- Cedar policy templates compile with `parameters[].example` values

## Status promotion: experimental → stable

Bundles ship as `experimental`. Promotion requires:
- ≥30 days since merge
- Telemetry from ≥5 customers showing FP rate <X% (Clampd team verifies)
- Maintainer team approval

Open a separate PR titled `Promote <id> to stable` to request promotion.

## Review

PRs route to the category's CODEOWNERS team via `.github/CODEOWNERS`:
- 1 approval needed for `experimental` bundles
- 2 approvals needed for `stable` promotions
- Schema/tools changes require `@clampd/bundles-maintainers`

## Anti-patterns we'll reject

- Bundle without `examples/` directory
- Demo agent named without `-demo` suffix
- `status: stable` on first PR
- `references: []` (you must justify why this bundle exists)
- Cedar templates without `parameters` field - every template should be parameterized
- Hardcoded customer-specific values (paths, domains) in the bundle - those go in template parameters
- Duplicate of an existing bundle with minor tweaks - open an issue to discuss merging instead

## Questions?

Open a discussion in the repo or ping `@clampd/bundles-maintainers` in a draft PR.
