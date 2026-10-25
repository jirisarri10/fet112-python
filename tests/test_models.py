from fet112.models import PreActionResult


def test_pre_action_result_parses_core_fields():
    payload = {
        "schema": "fet112.pre-action-response.v1",
        "decision": "REVIEW",
        "decision_basis": "ENVIRONMENT_REQUIRES_REVIEW_ACTION_RISK_NOT_EVALUATED",
        "reason_codes": ["STATISTICAL_ANOMALY"],
        "action_hash": "sha256:action",
        "environment_assessment": {"state": "REVIEW"},
        "action_assessment": {"state": "NOT_EVALUATED"},
        "report_attestation": {"report_hash": "sha256:report"},
    }
    result = PreActionResult.from_payload(payload)
    assert result.decision == "REVIEW"
    assert result.environment_clear is False
    assert result.report_hash == "sha256:report"
    assert result.action_assessment["state"] == "NOT_EVALUATED"


def test_continue_means_environment_clear_not_action_safe():
    result = PreActionResult.from_payload({
        "decision": "CONTINUE",
        "environment_assessment": {},
        "action_assessment": {"state": "NOT_EVALUATED"},
    })
    assert result.environment_clear is True
    assert not hasattr(result, "safe")
