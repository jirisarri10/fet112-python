# FET112 Python SDK

**Check the monitored security environment before your agent acts.**

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

FET112 v1 evaluates the **current monitored Ethereum security environment**. It does **not** classify the destination, amount, asset, authorization, profitability, executability, or safety of the proposed action itself. Those action-specific checks remain `NOT_EVALUATED`.

## CLI

```bash
fet112 check demo-destination --amount 1 --asset FET
```

For the complete contracts, evidence model, MCP and A2A interfaces, see https://www.fet112.com/developers.
