---
name: stock-alpaca-secret-hygiene
description: Protect stock-alpaca secrets and provider credentials. Use when reading .env, editing provider wrappers/caches/preflight code, inspecting provider/account artifacts or logs that may contain credentials, preparing wiki entries from provider payloads, or diagnosing Alpha Vantage, FRED, Firecrawl, SEC EDGAR, Alpaca, or other API output.
---

# Stock Alpaca Secret Hygiene

Use this skill whenever a task touches credentials, provider payloads, caches, logs, or artifacts.

## Boundary

This is a cross-cutting safety skill. It does not decide trading policy, provider coverage status, or runtime recovery order; it only constrains how sensitive values are handled while those skills run.

## Rules

1. Never print, summarize, copy, or commit API keys or secret values.
2. Do not include key values in final answers, wiki pages, raw source notes, cache files, tests, or fixtures.
3. Do not pass secrets through command lines when an environment variable or MCP config already provides them.
4. When showing `.env` status, report only whether required variables are present, never their values.
5. Treat provider response URLs, error payloads, and cache keys as potentially sensitive.

## Provider Artifacts

- For Alpha Vantage and similar providers, store key-scoped state using a non-reversible fingerprint, not the key.
- Sanitize URLs and payloads before writing provider errors into `wiki/evidence-store/sources/`.
- Do not preserve old cache entries that contain raw provider keys.
- Prefer explicit gap categories such as `auth`, `timeout`, `provider_error`, or `empty_response` over copying raw error text.

## Before Finishing

When a task changed provider wrappers, preflight code, notifications, or artifacts:

1. Run the relevant unit tests.
2. Search only for known leaked literals if the user already exposed them in context; do not echo matches.
3. Report the count/status of sensitive-value checks without revealing the values.
