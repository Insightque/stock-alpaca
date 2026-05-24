# Run Manifests

`wiki/runs/` stores machine-readable provenance for meaningful harness runs.

Use `harness/templates/run-manifest.json` as the starting shape and validate the structure against `harness/run-manifest.schema.json` when tooling is available.

The manifest should record the prompt hash, git commit, policy versions, MCP servers used, data gaps, source references, risk-check result, and submitted paper order IDs when submit mode is used.
