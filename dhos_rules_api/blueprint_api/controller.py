from typing import Dict

import requests
from flask import Response
from flask import current_app as app
from flask_batteries_included.helpers.error_handler import (
    EntityNotFoundException,
    ServiceUnavailableException,
)
from marshmallow import INCLUDE
from she_logging import logger
from she_logging.request_id import current_request_id

from dhos_rules_api.blueprint_api import trustomer
from dhos_rules_api.helpers import obs_set_utils
from dhos_rules_api.models.blood_glucose import (
    BloodGlucoseBanding,
    BloodGlucoseThresholds,
)


def request_headers() -> Dict:
    return {"X-Request-ID": current_request_id()}


def score_observation_set(observation_set: Dict) -> Dict:
    score_system = observation_set.get("score_system")
    # Check scoring system.
    if score_system not in ["news2", "meows"]:
        raise ValueError(f"Obs set posted with unknown scoring system {score_system}")

    score_request: Dict = obs_set_utils.ews_from_observation_set_dict(observation_set)

    logger.debug("Scoring obs set")
    url: str = f"{app.config['DHOS_RULES_ENGINE_URL']}/{score_system}"
    try:
        response = requests.post(url, headers=request_headers(), json=score_request)
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        raise ServiceUnavailableException("Could not contact rules engine")

    except requests.exceptions.HTTPError as e:
        logger.error("Could not run %s rules engine", score_system)
        raise ServiceUnavailableException(e)

    logger.debug(
        "Received result from %s rules engine",
        score_system,
        extra={"result": response.json()},
    )
    return obs_set_utils.build_obs_set_response(observation_set, response.json())


def score_blood_glucose_reading(
    bg_reading: Dict,
) -> Dict:
    trustomer_config = trustomer.get_trustomer_config()
    thresholds: Dict = trustomer_config["gdm_config"]["blood_glucose_thresholds_mmoll"]
    return score_blood_glucose_reading_common(bg_reading, thresholds)


def score_blood_glucose_reading_v2(
    bg_reading: Dict,
) -> Dict:
    thresholds: Dict = bg_reading.pop("thresholds_mmoll")
    return score_blood_glucose_reading_common(
        bg_reading, BloodGlucoseThresholds().dump(thresholds)
    )


def score_blood_glucose_reading_common(
    bg_reading: Dict,
    thresholds_mmol: Dict,
) -> Dict:
    trimmed_bg_reading = {k: v for k, v in bg_reading.items() if v is not None}
    trimmed_bg_reading["blood_glucose_thresholds_mmoll"] = thresholds_mmol

    logger.debug("Scoring BG reading", extra={"reading": trimmed_bg_reading})
    url: str = f"{app.config['DHOS_RULES_ENGINE_URL']}/bg_reading"
    try:
        response = requests.post(
            url, headers=request_headers(), json=trimmed_bg_reading
        )
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailableException("Could not contact rules engine")
    except requests.exceptions.HTTPError as e:
        logger.error("Could not run BG readings rules engine")
        raise ServiceUnavailableException(e)

    logger.debug(
        "Received result from BG reading rules engine",
        extra={"result": response.json()},
    )
    return BloodGlucoseBanding(unknown=INCLUDE).load(response.json())


def retrieve_rule_definition(filename: str) -> Response:
    url: str = f"{app.config['DHOS_RULES_ENGINE_URL']}/rule_definition/{filename}"
    try:
        response = requests.get(url, headers=request_headers())
    except requests.exceptions.ConnectionError:
        raise ServiceUnavailableException("Could not contact rules engine")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            logger.error("Attempt to get invalid bundle file: '%s'", filename)
            raise EntityNotFoundException("Could not find that rule bundle file")
        else:
            logger.error("Could not retrieve bundle file")
            raise ServiceUnavailableException(e)

    logger.debug("Received contents of file %s", filename)
    content_type = response.headers.get("Content-Type", "application/json")
    return Response(
        response=response.content,
        status=response.status_code,
        content_type=content_type,
    )
