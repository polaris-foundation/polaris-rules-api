from typing import Dict

import requests
from environs import Env
from requests import Response

_base_url = Env().str("DHOS_RULES_BASE_URL", "http://dhos-rules-api:5000")


def score_observation_set(obs_set: Dict, jwt: str) -> Response:
    return requests.post(
        f"{_base_url}/dhos/v1/score_observation_set",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
        json=obs_set,
    )


def score_bg_reading(reading: Dict, jwt: str) -> Response:
    return requests.post(
        f"{_base_url}/dhos/v1/score_blood_glucose_reading",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
        json=reading,
    )


def score_bg_reading_v2(reading: Dict, jwt: str) -> Response:
    return requests.post(
        f"{_base_url}/dhos/v2/score_blood_glucose_reading",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
        json=reading,
    )
