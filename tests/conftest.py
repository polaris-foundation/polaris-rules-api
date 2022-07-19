from typing import Any, Dict, Generator
from unittest import mock

import pytest
from flask import Flask

from dhos_rules_api.blueprint_api import trustomer


@pytest.fixture()
def app() -> Flask:
    """Fixture that creates app for testing"""
    import dhos_rules_api.app

    return dhos_rules_api.app.create_app(testing=True)


@pytest.fixture
def app_context(app: Flask) -> Generator[None, None, None]:
    with app.app_context():
        yield


@pytest.fixture
def trustomer_config() -> Dict:
    """Trustomer configuration"""
    return {
        "gdm_config": {
            "blood_glucose_units": "mmol/L",
            "blood_glucose_thresholds_mmoll": {
                "BEFORE-BREAKFAST": {"high": 5.3, "low": 4.0},
                "OTHER": {"high": 7.8, "low": 4.0},
                "BEFORE-LUNCH": {"high": 6.0, "low": 4.0},
                "BEFORE-DINNER": {"high": 6.0, "low": 4.0},
            },
            "graph_thresholds_mmoll": {"high": 7.8, "low": 4.0},
        },
        "send_config": {
            "news2": {
                "zero_severity_interval_hours": 12,
                "low_severity_interval_hours": 4,
                "low_medium_severity_interval_hours": 1,
                "medium_severity_interval_hours": 1,
                "high_severity_interval_hours": 0,
                "escalation_policy": {
                    "routine_monitoring": "<p>Continue routine NEWS monitoring</p>",
                    "low_monitoring": "<p>Inform registered nurse, who must assess the patient</p><p>Registered nurse decides whether increased frequency of monitoring and/or escalation of care is required</p>",
                    "low_medium_monitoring": "<p>Registered nurse to inform medical team caring for the patient, who will review and decide whether escalation of care is necessary</p>",
                    "medium_monitoring": "<p>Registered nurse to immediately inform the medical team caring for the patient</p><p>Registered nurse to request urgent assessment by a clinician or team with core competencies in the care of acutely ill patients</p><p>Provide clinical care in an environment with monitoring facilities</p>",
                    "high_monitoring": "<p>Registered nurse to immediately inform the medical team caring for the patient – this should be at least at specialist registrar level</p><p>Emergency assessment by a team with critical care competencies, including practitioner(s) with advanced airway management skills</p><p>Consider transfer of care to a level 2 or 3 clinical care facility, ie higher-dependency unit or ICU</p><p>Clinical care in an environment with monitoring facilities</p>",
                },
            },
            "meows": {
                "zero_severity_interval_hours": 12,
                "low_severity_interval_hours": 12,
                "low_medium_severity_interval_hours": 6,
                "medium_severity_interval_hours": 0.5,
                "high_severity_interval_hours": 0.5,
                "escalation_policy": {
                    "routine_monitoring": "<p>Continue routine MEOWS monitoring</p>",
                    "low_monitoring": "<p>Inform registered nurse, who must assess the patient</p><p>Registered nurse decides whether increased frequency of monitoring and/or escalation of care is required</p>",
                    "low_medium_monitoring": "<p>Registered nurse to inform medical team caring for the patient, who will review and decide whether escalation of care is necessary</p>",
                    "medium_monitoring": "<p>Registered nurse to immediately inform the medical team caring for the patient</p><p>Registered nurse to request urgent assessment by a clinician or team with core competencies in the care of acutely ill patients</p><p>Provide clinical care in an environment with monitoring facilities</p>",
                    "high_monitoring": "<p>Registered nurse to immediately inform the medical team caring for the patient – this should be at least at specialist registrar level</p><p>Emergency assessment by a team with critical care competencies, including practitioner(s) with advanced airway management skills</p><p>Consider transfer of care to a level 2 or 3 clinical care facility, ie higher-dependency unit or ICU</p><p>Clinical care in an environment with monitoring facilities</p>",
                },
            },
        },
    }


@pytest.fixture
def mock_trustomer_config(mocker: Any, trustomer_config: Any) -> mock.Mock:
    """Mock trustomer config get"""
    return mocker.patch.object(
        trustomer, "get_trustomer_config", return_value=trustomer_config
    )


@pytest.fixture
def observation_set_request() -> Dict:
    """An observation set request, corresponding to observation_set_response"""

    # Test observations include examples with observation_metadata omitted, present but None, and present with
    # additional field that should be ignored.
    return {
        "score_system": "news2",
        "record_time": "2017-09-23T08:31:19.123+00:00",
        "observations": [
            {
                "observation_type": "heart_rate",
                "patient_refused": False,
                "observation_value": 160,
                "observation_unit": "bpm",
                "measured_time": "2017-09-23T08:29:19.123+00:00",
            },
            {
                "observation_type": "o2_therapy_status",
                "patient_refused": False,
                "observation_value": 2,
                "observation_metadata": {
                    "created": "2017-09-23T08:29:19.123+00:00",
                    "mask": "Venturi",
                    "mask_percent": 75,
                },
                "observation_unit": "lpm",
                "measured_time": "2017-09-23T08:29:19.123+00:00",
            },
            {
                "observation_type": "spo2",
                "patient_refused": False,
                "observation_value": 55,
                "observation_unit": "%",
                "measured_time": "2017-09-23T08:29:19.123+00:00",
                "observation_metadata": None,
            },
        ],
        "encounter_id": "e22f5175-6283-408d-9ba4-ea3b3a5354b8",
    }


@pytest.fixture
def observation_set_response() -> Dict:
    """An observation set response, corresponding to observation_set_request"""
    return {
        "score_system": "news2",
        "score_value": 0,
        "score_severity": "low",
        "score_value_display": "0",
        "record_time": "2017-09-23T08:31:19.123+00:00",
        "observations": [
            {
                "observation_type": "heart_rate",
                "patient_refused": False,
                "observation_value": 160,
                "observation_unit": "bpm",
                "measured_time": "2017-09-23T08:29:19.123+00:00",
            },
            {
                "observation_type": "o2_therapy_status",
                "patient_refused": False,
                "score_value": 3,
                "observation_value": 2,
                "observation_metadata": {"mask": "Venturi", "mask_percent": 75},
                "observation_unit": "lpm",
                "measured_time": "2017-09-23T08:29:19.123+00:00",
            },
            {
                "observation_type": "spo2",
                "patient_refused": False,
                "score_value": 3,
                "observation_value": 55,
                "observation_unit": "%",
                "measured_time": "2017-09-23T08:29:19.123+00:00",
                "observation_metadata": None,
            },
        ],
        "encounter_id": "e22f5175-6283-408d-9ba4-ea3b3a5354b8",
        "obx_reference_range": "0-4",
        "obx_abnormal_flags": "N",
    }


@pytest.fixture
def meows_observation_set_request() -> Dict:
    """An observation set request, corresponding to observation_set_response"""
    return {
        "uuid": "2c4f1d24-2952-4d4e-b1d1-3637e33cc161",
        "created": "2017-09-23T08:29:19.123+00:00",
        "modified": "2017-09-23T08:29:19.123+00:00",
        "score_system": "meows",
        "record_time": "2017-09-23T08:31:19.123+00:00",
        "observations": [
            {
                "observation_type": "heart_rate",
                "patient_refused": False,
                "observation_value": 60,
                "observation_unit": "bpm",
                "measured_time": "2017-09-23T08:29:19.123+00:00",
            }
        ],
        "encounter_id": "e22f5175-6283-408d-9ba4-ea3b3a5354b8",
    }


@pytest.fixture
def meows_observation_set_response() -> Dict:
    """An observation set response, corresponding to observation_set_request"""
    return {
        "uuid": "2c4f1d24-2952-4d4e-b1d1-3637e33cc161",
        "created": "2017-09-23T08:29:19.123+00:00",
        "modified": "2017-09-23T08:29:19.123+00:00",
        "score_system": "meows",
        "score_value": 0,
        "score_severity": "low",
        "score_value_display": "0",
        "record_time": "2017-09-23T08:31:19.123+00:00",
        "observations": [
            {
                "observation_type": "heart_rate",
                "patient_refused": False,
                "observation_value": 60,
                "observation_unit": "bpm",
                "measured_time": "2017-09-23T08:29:19.123+00:00",
            }
        ],
        "encounter_id": "e22f5175-6283-408d-9ba4-ea3b3a5354b8",
        "obx_reference_range": "0",
        "obx_abnormal_flags": "N",
    }
