# FET112 Python SDK

**Check the monitored security environment before your agent acts.**

[![PyPI](https://img.shields.io/pypi/v/fet112)](https://pypi.org/project/fet112/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://pypi.org/project/fet112/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Autonomous agents are starting to move real money. FET112 is the **security checkpoint they call before acting**: it evaluates the current monitored Ethereum security environment and returns a plain, honest decision — `CONTINUE`, `REVIEW`, or `STOP`.

No dashboards to watch. No promises it can't keep. Just one call before every action.

## ⚡ Quickstart

```bash
pip install fet112
```

```python
from fet112 import pre_action_check

result = pre_action_check(
    "demo-destination",
    action="transfer",
    amount="1",
    asset="FET",
)
print(result.decision)  # CONTINUE, REVIEW, or STOP
```

Or from the command line:

```bash
fet112 check demo-destination --amount 1 --asset FET
```

## Why FET112

| Without FET112 | With FET112 |
| --- | --- |
| Agent transfers funds immediately | Agent calls `pre_action_check()` first |
| Security context unknown at action time | Decision reflects the **current monitored environment** |
| Failures discovered after the damage | `STOP` / `REVIEW` returned **before** the action executes |
| "It seemed safe" | `CONTINUE` / `REVIEW` / `STOP` — no adjectives, a decision |

FET112 doesn't sell trust. It sells **an honest answer with defined scope** — including the answer "I don't evaluate that."

## Honest scope (what FET112 does — and does not — evaluate)

FET112 v1 evaluates the **current monitored Ethereum security environment**.

It does **not** classify the destination, amount, asset, authorization, profitability, executability, or safety of the proposed action itself. Those action-specific checks remain `NOT_EVALUATED` — and the SDK tells you so, every time.

That's not a limitation buried in a footnote. It's the contract. An agent that knows the limits of its own answers is safer than one that doesn't.

## What you get

- `pre_action_check(...)` — one call, one decision: `CONTINUE`, `REVIEW`, or `STOP`
- `NOT_EVALUATED` transparency — the SDK always declares what was not assessed
- Python 3.10 – 3.14 support
- CLI included (`fet112 check ...`)
- MIT licensed, tested, published on PyPI

## For the complete picture

Full contracts, the evidence model, MCP and A2A interfaces, and the monitored-metrics catalog (transfers, staking, IBC, contracts, security, attestations):

👉 **[fet112.com/developers](https://www.fet112.com/developers)**

## Status

- ✅ `v0.1.0` released on [PyPI](https://pypi.org/project/fet112/)
- ✅ Trusted publishing workflow configured
- ✅ Test suite included

## License

[MIT](LICENSE)
