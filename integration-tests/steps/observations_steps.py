import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

from behave import step
from behave.runner import Context
from clients import rules_api_client
from dateutil import parser
from she_logging import logger

MANDATORY_VITAL_SIGNS = [
    "temperature",
    "heart rate",
    "systolic blood pressure",
    "diastolic blood pressure",
    "respiratory rate",
    "spo2",
    "acvpu",
]


@step(
    "o2 (?P<observation_type>mask|mask percentage) value (?P<observation_value>.*) is in the observation set"
)
def add_o2_therapy_metadata_obs_to_obs_set(
    context: Context, observation_type: str, observation_value: str
) -> None:
    obs: Dict = _find_obs_in_obs_set(
        observation_set=context.observation_set, observation_type="o2_therapy_status"
    )
    if observation_type == "mask":
        obs["observation_metadata"]["mask"] = observation_value
    elif observation_type == "mask percentage":
        obs["observation_metadata"]["mask_percent"] = (
            int(observation_value) if observation_value else None
        )


@step(
    "(?P<observation_type>.+) value (?P<observation_value>.*) is in the observation set"
)
def add_obs_to_obs_set(
    context: Context, observation_type: str, observation_value: str
) -> None:
    obs: Dict = _find_obs_in_obs_set(
        observation_set=context.observation_set, observation_type=observation_type
    )

    if len(observation_value) == 0 and observation_type in MANDATORY_VITAL_SIGNS:
        # no value provided for mandatory vital sign - partial observation
        logger.info(
            "no value provided for %s, setting obs set as partial", observation_type
        )
        del context.observation_set["observations"][
            context.observation_set["observations"].index(obs)
        ]
        context.observation_set["is_partial"] = True
    else:
        if observation_type == "consciousness acvpu":
            obs["observation_string"] = observation_value
        else:
            obs["observation_value"] = (
                float(observation_value)
                if observation_type == "temperature"
                else int(observation_value)
            )


@step("I see the observation set is (?P<obs_set_type>full|partial)")
def assert_partial_observation(context: Context, obs_set_type: str) -> None:
    assert context.scored_obs_set["is_partial"] == (obs_set_type == "partial")


@step("there exists an observation set")
def get_obs_set_from_template(context: Context) -> None:
    file: Path = Path(__file__).parent.parent / "resources" / "obs_set_template.json"
    context.observation_set = json.loads(file.read_text())


@step("I score the observation set according to (?P<score_system>\w+) rules")
def score_obs_set(context: Context, score_system: str) -> None:
    context.observation_set["score_system"] = score_system
    logger.debug(
        "obs set to score (%s): %s",
        score_system,
        json.dumps(context.observation_set, indent=4),
    )

    response = rules_api_client.score_observation_set(
        obs_set=context.observation_set, jwt=context.system_jwt
    )
    assert response.status_code == 200
    context.scored_obs_set = response.json()
    logger.debug("scored: %s", json.dumps(context.scored_obs_set, indent=4))


@step("I see the overall score is (?P<score_value>\d+)")
def assert_int_value_in_scored_obs_set(context: Context, score_value: str) -> None:
    logger.debug(
        "overall score: expected=%s actual=%s",
        int(score_value),
        context.scored_obs_set["score_value"],
    )
    assert int(score_value) == context.scored_obs_set["score_value"]


@step(
    "I see the (?P<observation_type>score severity|obx abnormal flags) is (?P<score_value>.+)"
)
def assert_string_value_in_scored_obs_set(
    context: Context, observation_type: str, score_value: str
) -> None:
    key: str = observation_type.replace(" ", "_")
    logger.debug(
        "%s: expected=%s actual=%s",
        observation_type,
        score_value,
        context.scored_obs_set[key],
    )
    assert score_value == context.scored_obs_set[key]


@step("I see the (?P<observation_type>.*) score is missing")
def assert_obs_score_missing(context: Context, observation_type: str) -> None:
    try:
        actual: Dict = _find_obs_in_obs_set(
            observation_set=context.scored_obs_set, observation_type=observation_type
        )
        assert "score_value" not in actual
    except AssertionError:
        # `observation_type` not in the partial obs set, just verify this is really a partial obs set
        assert context.scored_obs_set["is_partial"]


@step("I see the (?P<observation_type>.*) score is (?P<score_value>\d*)")
def assert_obs_in_scored_obs_set(
    context: Context, observation_type: str, score_value: str
) -> None:
    logger.debug("obs type: %s", observation_type)
    if len(score_value) > 0:
        expected: Dict = _find_obs_in_obs_set(
            observation_set=context.observation_set, observation_type=observation_type
        )
        expected["score_value"] = int(score_value)
        actual: Dict = _find_obs_in_obs_set(
            observation_set=context.scored_obs_set, observation_type=observation_type
        )
        logger.debug("expected: %s", json.dumps(expected))
        logger.debug("actual: %s", json.dumps(actual))
        assert expected == actual
    else:
        key: str = observation_type.replace(" ", "_")
        logger.debug("asserting %s not in scored obs set", key)
        assert key not in [
            obs["observation_type"] for obs in context.scored_obs_set["observations"]
        ]


@step(
    "I see the next observation set is due in (?P<next_obs_set_delta>[\d|\.]+)(?P<next_obs_set_delta_unit>h|m)"
)
def assert_next_obs_due_time(
    context: Context, next_obs_set_delta: str, next_obs_set_delta_unit: str
) -> None:
    obs_set_datetime: datetime = parser.parse(context.observation_set["record_time"])
    next_obs_set_due_datetime: datetime = parser.parse(
        context.scored_obs_set["time_next_obs_set_due"]
    )

    if next_obs_set_delta_unit == "h":
        delta: timedelta = timedelta(hours=int(next_obs_set_delta))
    else:
        delta = timedelta(minutes=int(next_obs_set_delta))

    assert obs_set_datetime + delta == next_obs_set_due_datetime


def _find_obs_in_obs_set(observation_set: Dict, observation_type: str) -> Dict:
    key: str = observation_type.replace(" ", "_")
    observation: List[Dict] = [
        obs for obs in observation_set["observations"] if obs["observation_type"] == key
    ]
    assert len(observation) == 1
    return observation[0]
