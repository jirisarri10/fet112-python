from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

_VALID_DECISIONS = {"CONTINUE", "REVIEW", "STOP"}


@dataclass(frozen=True, slots=True)
class PreActionResult:
    """Result of FET112's pre-action environment assessment.

    Important: FET112 v1 evaluates the monitored environment. It does not
    classify the destination, amount, asset, authorization, profitability,
    executability, or transaction safety of the proposed action itself.
    """

    decision: str
    decision_basis: str | None
    action_hash: str | None
    environment_assessment: Mapping[str, Any]
    action_assessment: Mapping[str, Any]
    reason_codes: tuple[str, ...]
    report_hash: str | None
    raw: Mapping[str, Any]

    @property
    def environment_clear(self) -> bool:
        """True only when FET112 returns CONTINUE for the monitored environment.

        This is deliberately not named ``safe``: the proposed action itself is
        NOT_EVALUATED by FET112 v1.
        """
        return self.decision == "CONTINUE"

    @classmethod
    def from_payload(cls, payload: Mapping[str, Any]) -> "PreActionResult":
        decision = payload.get("decision")
        if not isinstance(decision, str) or decision not in _VALID_DECISIONS:
            from .errors import FET112ProtocolError
            raise FET112ProtocolError("missing or invalid pre_action_check decision")

        environment = payload.get("environment_assessment")
        action = payload.get("action_assessment")
        if not isinstance(environment, Mapping):
            environment = {}
        if not isinstance(action, Mapping):
            action = {}

        reasons = payload.get("reason_codes")
        if isinstance(reasons, list):
            reason_codes = tuple(str(item) for item in reasons)
        else:
            reason_codes = ()

        attestation = payload.get("report_attestation")
        report_hash = attestation.get("report_hash") if isinstance(attestation, Mapping) else None
        if report_hash is not None and not isinstance(report_hash, str):
            report_hash = None

        return cls(
            decision=decision,
            decision_basis=payload.get("decision_basis") if isinstance(payload.get("decision_basis"), str) else None,
            action_hash=payload.get("action_hash") if isinstance(payload.get("action_hash"), str) else None,
            environment_assessment=environment,
            action_assessment=action,
            reason_codes=reason_codes,
            report_hash=report_hash,
            raw=payload,
        )
