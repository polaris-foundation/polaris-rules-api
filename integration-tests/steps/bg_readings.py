from behave import then, when
from behave.runner import Context
from clients import rules_api_client


@when("I score a blood glucose reading of (?P<value>.+) with a tag of (?P<tag>.+)")
def score_observation_sets(context: Context, value: str, tag: str) -> None:
    reading = {"blood_glucose_value": float(value), "prandial_tag_id": tag}
    response = rules_api_client.score_bg_reading(
        reading=reading, jwt=context.system_jwt
    )
    assert response.status_code == 200
    context.scored_reading = response.json()


@then("I see the expected banding is (?P<banding>.+)")
def check_observation_sets(context: Context, banding: str) -> None:
    assert context.scored_reading["banding_id"] == banding


@when(
    "I score a blood glucose reading using custom thresholds with (?P<value>.+) and a tag of (?P<tag>.+)"
)
def score_observation_sets_v2(context: Context, value: str, tag: str) -> None:
    reading = {
        "blood_glucose_value": float(value),
        "prandial_tag_id": tag,
        "thresholds_mmoll": {
            "BEFORE-BREAKFAST": {"high": 10, "low": 5},
            "OTHER": {"high": 0, "low": 0},
        },
    }
    response = rules_api_client.score_bg_reading_v2(
        reading=reading, jwt=context.system_jwt
    )
    assert response.status_code == 200
    context.scored_reading = response.json()
