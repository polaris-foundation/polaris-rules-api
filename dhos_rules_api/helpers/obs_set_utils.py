from typing import Dict, Optional, Union

from she_logging import logger

from dhos_rules_api.blueprint_api import trustomer


def ews_from_observation_set_dict(obs_set: Dict) -> Dict:
    trustomer_config: Dict = trustomer.get_trustomer_config()
    score_system_config = trustomer_config["send_config"].get(obs_set["score_system"])
    if not score_system_config:
        raise ValueError(
            "Missing scoring system configuration for % in trustomer config",
            obs_set["score_system"],
        )
    ews: Dict = {
        "respiratory_rate": _find_observation_value(obs_set, "respiratory_rate"),
        "heart_rate": _find_observation_value(obs_set, "heart_rate"),
        "oxygen_saturation": _find_observation_value(obs_set, "spo2"),
        "systolic_blood_pressure": _find_observation_value(
            obs_set, "systolic_blood_pressure"
        ),
        "consciousness_acvpu": _find_observation_value(obs_set, "consciousness_acvpu"),
        "temperature": _find_observation_value(obs_set, "temperature"),
        "time": obs_set["record_time"],
        "nurse_concern": _find_observation_value(obs_set, "nurse_concern"),
        **_find_o2_therapy(obs_set),
        "config": score_system_config,
    }

    if obs_set["score_system"] == "news2":
        ews["spo2_scale"] = obs_set.get("spo2_scale") or 1  # Default to 1

    if obs_set["score_system"] == "meows":
        ews["diastolic_blood_pressure"] = _find_observation_value(
            obs_set, "diastolic_blood_pressure"
        )

    trimmed_request = {k: v for k, v in ews.items() if v is not None}

    return trimmed_request


def build_obs_set_response(obs_set: Dict, scores: Dict) -> Dict:
    _set_obs_score(obs_set, scores["respiratory_rate_score"], name="respiratory_rate")
    _set_obs_score(obs_set, scores["heart_rate_score"], name="heart_rate")
    _set_obs_score(obs_set, scores["oxygen_saturation_score"], name="spo2")
    if obs_set["score_system"] == "news2":
        _set_obs_score(obs_set, scores["o2_therapy_score"], name="o2_therapy_status")
        _set_obs_score(
            obs_set, scores["blood_pressure_score"], name="systolic_blood_pressure"
        )
    if obs_set["score_system"] == "meows":
        _set_obs_score(
            obs_set,
            scores["systolic_blood_pressure_score"],
            name="systolic_blood_pressure",
        )
        _set_obs_score(
            obs_set,
            scores["diastolic_blood_pressure_score"],
            name="diastolic_blood_pressure",
        )

    _set_obs_score(obs_set, scores["consciousness_score"], name="consciousness_acvpu")
    _set_obs_score(obs_set, scores["temperature_score"], name="temperature")
    obs_set["score_value"] = scores["overall_score"]
    obs_set["score_severity"] = scores["overall_severity"]
    obs_set["score_string"] = scores["overall_score_display"]
    obs_set["is_partial"] = scores["partial_set"]
    obs_set["time_next_obs_set_due"] = scores["time_next_obs_set_due"]
    obs_set["monitoring_instruction"] = scores["monitoring_instruction"]
    obs_set["empty_set"] = scores.get("empty_set")
    obs_set["ranking"] = scores["ranking"]
    obs_set["obx_reference_range"] = scores["obx_reference_range"]
    obs_set["obx_abnormal_flags"] = scores["obx_abnormal_flags"]
    return obs_set


def _find_observation(obs_set: Dict, name: str) -> Optional[Dict]:
    matches = [i for i in obs_set["observations"] if i["observation_type"] == name]
    if len(matches) == 0:
        return None
    if len(matches) > 1:
        logger.warning("Multiple obs in set of type %s, using first", name)
    return matches[0]


def _find_observation_value(obs_set: Dict, name: str) -> Union[str, float, None]:
    obj = _find_observation(obs_set, name)
    if obj:
        if obj.get("observation_string") and obj.get("observation_value"):
            logger.warning(
                "Both obs string (%s) and obs value (%s) are set",
                obj["observation_string"],
                obj["observation_value"],
            )
        return obj.get("observation_value") or obj.get("observation_string")
    return None


def _find_o2_therapy(obs_set: Dict) -> Dict:
    obj = _find_observation(obs_set, "o2_therapy_status")
    if obj is None:
        return {}
    metadata = obj.get("observation_metadata")
    return {
        "o2_therapy": obj["observation_value"],
        "o2_therapy_mask": metadata.get("mask") if metadata else None,
    }


def _set_obs_score(obs_set: Dict, score_val: int, name: str) -> None:
    obj = _find_observation(obs_set, name)
    if obj:
        obj["score_value"] = score_val
