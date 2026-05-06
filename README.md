# Clampd Bundles

Curated detection rules, keywords, demo agents, and policy templates for AI agent runtime security.

Apache-2.0. Built and maintained by the Clampd community.

## What's a bundle?

One JSON file per category-specific use case. Each bundle ships:
- **Rule references** — which of Clampd's 152+ built-in rules apply to this agent type
- **Keywords** — secrets, dangerous commands, sensitive paths specific to the use case
- **Demo agent** — a throwaway agent config for onboarding (not for production!)
- **Policy templates** — Cedar policies with parameters customers fill in
- **Protected entities** — internal paths, brand domains, wallet addresses to defend
- **False-positive notes** — known FPs and how to handle them
- **Sensitivity dial** — strict/balanced/permissive presets per bundle

Plus a runnable `examples/<category>/<bundle>/` directory with <100 LOC of code showing the bundle in action against attack fixtures.

## Categories

| Category | Bundles | Examples of what's in here |
|---|---|---|
| `coding` | cursor, claude-code, aider, cline, continue-dev, github-copilot-chat, generic | IDE coding agents — secret leak protection, file-write allowlists |
| `ci-cd` | github-actions, gitlab-ci, circleci, jenkins, argocd, tekton | CI agents — secrets in workflow logs, supply chain attacks |
| `browser` | playwright, puppeteer, selenium, browser-use | Browser automation — credential phishing, navigation hijacking |
| `database` | postgres, mysql, mongodb, redis, snowflake, bigquery | DB query agents — bulk dumps, schema mutation, PII queries |
| `devops` | kubernetes, terraform, ansible, aws-cli, gcp-cli, azure-cli | Infra agents — privilege escalation, region exfil |
| `email-comms` | gmail-mcp, outlook-mcp, slack-mcp, discord-mcp | Comms agents — external send detection, attachment exfil |
| `customer-support` | zendesk, intercom, salesforce, hubspot | Support agents — PII leak, mass-update protection |
| `payment-commerce` | stripe, paypal, x402, shopify | Payment agents — recipient verification, vendor allowlist |
| `rag-research` | generic-rag, perplexity-clone, notebooklm, research-agent | Research agents — citation injection, document leak |
| `ml-model` | model-training, model-deploy, data-pipeline, feature-store | ML agents — training data exfil, model theft |
| `web3-defi` | wallet-agent, dex-trader, nft-minter | Web3 agents — wallet drainer, contract impersonation |
| `multi-agent` | autogen, crewai, langgraph, agno, openai-swarm | Multi-agent frameworks — delegation hash validation |
| `compliance` | hipaa, gdpr, pci-dss, soc2, eu-ai-act | Regulatory bundles — auto-tag rules to regulations |

## How to use

In your Clampd dashboard:

1. **Bundles tab** → enable the bundle that matches your agent
2. **Optional**: create the demo agent to see traffic flow end-to-end
3. **Optional**: open the linked `examples/` directory and run the demo
4. **Required**: create your REAL agent with your team's actual scopes (not the demo)
5. **Required**: parameterize the policy templates with your specific values
6. **Recommended**: backtest the bundle against your last 7 days of audit events before activating

CLI users (GitOps): `clampd bundles apply -f bundles.yaml`

## Status lifecycle

| Status | Meaning | Promotion path |
|---|---|---|
| `experimental` | Newly merged. Use at your own risk. May change. | 30 days + telemetry from ≥5 customers + FP rate <X% → `stable` |
| `stable` | Battle-tested. Backwards-compatible within minor versions. | If superseded → `deprecated` |
| `deprecated` | Replaced or removed. Migrate to successor noted in description. | Removed in next major |

New PRs default to `experimental`. The merge bot blocks `status: stable` on first PR.

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). PRs require:
- Schema validation (`tools/validate.ts`)
- All `rule_ids` exist in BUILTIN_RULES
- Cedar policy templates compile with default parameters
- `examples/<category>/<bundle>/` directory included
- At least one approval from the category's CODEOWNER team

## License

Apache 2.0. See [LICENSE](./LICENSE).
