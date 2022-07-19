import pytest

from dhos_rules_api.helpers import obs_set_utils


@pytest.mark.usefixtures("app", "mock_trustomer_config")
class TestObsSetUtils:
    def test_from_news2_observation_set_dict(self) -> None:
        expected = RULES_ENGINE_INPUT
        actual = obs_set_utils.ews_from_observation_set_dict(OBS_SET_REQUEST)
        assert expected == actual

    def test_build_obs_set_response(self) -> None:
        expected = OBS_SET_RESPONSE
        actual = obs_set_utils.build_obs_set_response(
            OBS_SET_REQUEST, RULES_ENGINE_OUTPUT
        )
        assert expected == actual

    def test_build_obs_set_with_no_obs_response(self) -> None:
        expected = EMPTY_OBS_SET_RESPONSE
        actual = obs_set_utils.build_obs_set_response(
            EMPTY_OBS_SET_REQUEST, EMPTY_RULES_ENGINE_OUTPUT
        )
        assert expected == actual


OBS_SET_REQUEST = {
    "score_system": "news2",
    "record_time": "2017-09-23T08:31:19.123+00:00",
    "spo2_scale": 2,
    "observations": [
        {
            "observation_type": "temperature",
            "patient_refused": False,
            "observation_value": 28.4,
            "observation_string": "",
            "observation_unit": "celsius",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "diastolic_blood_pressure",
            "patient_refused": False,
            "observation_value": 245,
            "observation_string": "",
            "observation_unit": "mmHg",
            "observation_metadata": {"patient_postion": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "systolic_blood_pressure",
            "patient_refused": False,
            "observation_value": 281,
            "observation_string": "",
            "observation_unit": "mmHg",
            "observation_metadata": {"patient_postion": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "heart_rate",
            "patient_refused": False,
            "observation_value": 160,
            "observation_string": "",
            "observation_unit": "bpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "respiratory_rate",
            "patient_refused": False,
            "observation_value": 55,
            "observation_string": "",
            "observation_unit": "bpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "o2_therapy_status",
            "patient_refused": False,
            "observation_value": 2,
            "observation_metadata": {"mask": "Venturi", "mask_percent": 75},
            "observation_unit": "lpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "consciousness_acvpu",
            "patient_refused": False,
            "observation_string": "Alert",
            "observation_metadata": {"patient_postion": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "nurse_concern",
            "patient_refused": False,
            "observation_string": "Infection",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "spo2",
            "patient_refused": False,
            "observation_value": 55,
            "observation_unit": "%",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "consciousness_gcs",
            "patient_refused": False,
            "observation_metadata": {
                "gcs_eyes": 4,
                "gcs_verbal": 2,
                "gcs_motor": 3,
                "gcs_eyes_description": "Spontaneous",
                "gcs_verbal_description": "Oriented",
                "gcs_motor_description": "Commands",
            },
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
    ],
    "encounter_id": "e22f5175-6283-408d-9ba4-ea3b3a5354b8",
}


RULES_ENGINE_INPUT = {
    "respiratory_rate": 55,
    "heart_rate": 160,
    "oxygen_saturation": 55,
    "spo2_scale": 2,
    "o2_therapy": 2,
    "o2_therapy_mask": "Venturi",
    "systolic_blood_pressure": 281,
    "consciousness_acvpu": "Alert",
    "temperature": 28.4,
    "time": "2017-09-23T08:31:19.123+00:00",
    "nurse_concern": "Infection",
    "config": {
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
}


RULES_ENGINE_OUTPUT = {
    "respiratory_rate_score": 0,
    "heart_rate_score": 1,
    "oxygen_saturation_score": 0,
    "o2_therapy_score": 3,
    "blood_pressure_score": 1,
    "consciousness_score": 2,
    "temperature_score": 3,
    "overall_score": 12,
    "overall_severity": "high",
    "overall_score_display": "12",
    "partial_set": False,
    "ranking": "0101010,2017-09-23T08:29:19.123+00:00",
    "time_next_obs_set_due": "2017-09-23T08:29:19.123+00:00",
    "monitoring_instruction": "low_medium_monitoring",
    "obx_reference_range": "0-4",
    "obx_abnormal_flags": "EXTHIGH",
}


OBS_SET_RESPONSE = {
    "score_system": "news2",
    "score_value": 12,
    "score_severity": "high",
    "score_string": "12",
    "is_partial": False,
    "record_time": "2017-09-23T08:31:19.123+00:00",
    "spo2_scale": 2,
    "ranking": "0101010,2017-09-23T08:29:19.123+00:00",
    "empty_set": None,
    "time_next_obs_set_due": "2017-09-23T08:29:19.123+00:00",
    "monitoring_instruction": "low_medium_monitoring",
    "observations": [
        {
            "observation_type": "temperature",
            "patient_refused": False,
            "observation_value": 28.4,
            "observation_string": "",
            "score_value": 3,
            "observation_unit": "celsius",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "diastolic_blood_pressure",
            "patient_refused": False,
            "observation_value": 245,
            "observation_string": "",
            "observation_unit": "mmHg",
            "observation_metadata": {"patient_postion": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "systolic_blood_pressure",
            "patient_refused": False,
            "observation_value": 281,
            "observation_string": "",
            "score_value": 1,
            "observation_unit": "mmHg",
            "observation_metadata": {"patient_postion": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "heart_rate",
            "patient_refused": False,
            "observation_value": 160,
            "observation_string": "",
            "score_value": 1,
            "observation_unit": "bpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "respiratory_rate",
            "patient_refused": False,
            "observation_value": 55,
            "observation_string": "",
            "score_value": 0,
            "observation_unit": "bpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "o2_therapy_status",
            "patient_refused": False,
            "observation_value": 2,
            "score_value": 3,
            "observation_metadata": {"mask": "Venturi", "mask_percent": 75},
            "observation_unit": "lpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "consciousness_acvpu",
            "patient_refused": False,
            "observation_string": "Alert",
            "score_value": 2,
            "observation_metadata": {"patient_postion": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "nurse_concern",
            "patient_refused": False,
            "observation_string": "Infection",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "spo2",
            "patient_refused": False,
            "observation_value": 55,
            "score_value": 0,
            "observation_unit": "%",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "consciousness_gcs",
            "patient_refused": False,
            "observation_metadata": {
                "gcs_eyes": 4,
                "gcs_verbal": 2,
                "gcs_motor": 3,
                "gcs_eyes_description": "Spontaneous",
                "gcs_verbal_description": "Oriented",
                "gcs_motor_description": "Commands",
            },
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
    ],
    "encounter_id": "e22f5175-6283-408d-9ba4-ea3b3a5354b8",
    "obx_reference_range": "0-4",
    "obx_abnormal_flags": "EXTHIGH",
}


EMPTY_OBS_SET_REQUEST = {
    "uuid": "2c4f1d24-2952-4d4e-b1d1-3637e33cc161",
    "uri": "http://uri.org",
    "created": "2017-09-23T08:29:19.123+00:00",
    "modified": "2017-09-23T08:29:19.123+00:00",
    "score_system": "news2",
    "record_time": "2017-09-23T08:31:19.123+00:00",
    "spo2_scale": 2,
    "ranking": "0101010,2017-09-23T08:29:19.123+00:00",
    "empty_set": True,
    "observations": [
        {
            "observation_type": "temperature",
            "patient_refused": True,
            "observation_value": None,
            "observation_string": "",
            "observation_unit": "celsius",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "diastolic_blood_pressure",
            "patient_refused": True,
            "observation_value": None,
            "observation_string": "",
            "observation_unit": "mmHg",
            "observation_metadata": {"patient_postion": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "systolic_blood_pressure",
            "patient_refused": True,
            "observation_value": None,
            "observation_string": "",
            "observation_unit": "mmHg",
            "observation_metadata": {"patient_postion": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "heart_rate",
            "patient_refused": True,
            "observation_value": None,
            "observation_string": "",
            "observation_unit": "bpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "respiratory_rate",
            "patient_refused": True,
            "observation_value": None,
            "observation_string": "",
            "observation_unit": "bpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "o2_therapy_status",
            "patient_refused": True,
            "observation_value": None,
            "observation_metadata": {"mask": "Venturi", "mask_percent": 75},
            "observation_unit": "lpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "spo2",
            "patient_refused": True,
            "observation_value": None,
            "observation_unit": "%",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "consciousness_gcs",
            "patient_refused": True,
            "observation_metadata": None,
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
    ],
    "encounter_id": "e22f5175-6283-408d-9ba4-ea3b3a5354b8",
}

EMPTY_RULES_ENGINE_OUTPUT = {
    "respiratory_rate_score": None,
    "heart_rate_score": None,
    "oxygen_saturation_score": None,
    "o2_therapy_score": None,
    "blood_pressure_score": None,
    "consciousness_score": None,
    "temperature_score": None,
    "overall_score": None,
    "overall_severity": "medium",
    "overall_score_display": None,
    "partial_set": True,
    "empty_set": True,
    "ranking": "0101010,2017-09-23T08:29:19.123+00:00",
    "time_next_obs_set_due": "2017-09-23T08:29:19.123+00:00",
    "monitoring_instruction": "low_medium_monitoring",
    "obx_reference_range": "0-4",
    "obx_abnormal_flags": "N",
}

EMPTY_OBS_SET_RESPONSE = {
    "uuid": "2c4f1d24-2952-4d4e-b1d1-3637e33cc161",
    "uri": "http://uri.org",
    "created": "2017-09-23T08:29:19.123+00:00",
    "modified": "2017-09-23T08:29:19.123+00:00",
    "score_system": "news2",
    "score_value": None,
    "score_severity": "medium",
    "score_string": None,
    "is_partial": True,
    "record_time": "2017-09-23T08:31:19.123+00:00",
    "spo2_scale": 2,
    "ranking": "0101010,2017-09-23T08:29:19.123+00:00",
    "empty_set": True,
    "time_next_obs_set_due": "2017-09-23T08:29:19.123+00:00",
    "monitoring_instruction": "low_medium_monitoring",
    "observations": [
        {
            "observation_type": "temperature",
            "patient_refused": True,
            "observation_value": None,
            "observation_string": "",
            "score_value": None,
            "observation_unit": "celsius",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "diastolic_blood_pressure",
            "patient_refused": True,
            "observation_value": None,
            "observation_string": "",
            "observation_unit": "mmHg",
            "observation_metadata": {"patient_postion": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "systolic_blood_pressure",
            "patient_refused": True,
            "observation_value": None,
            "observation_string": "",
            "score_value": None,
            "observation_unit": "mmHg",
            "observation_metadata": {"patient_postion": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "heart_rate",
            "patient_refused": True,
            "observation_value": None,
            "observation_string": "",
            "score_value": None,
            "observation_unit": "bpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "respiratory_rate",
            "patient_refused": True,
            "observation_value": None,
            "observation_string": "",
            "score_value": None,
            "observation_unit": "bpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "o2_therapy_status",
            "patient_refused": True,
            "observation_value": None,
            "score_value": None,
            "observation_metadata": {"mask": "Venturi", "mask_percent": 75},
            "observation_unit": "lpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "spo2",
            "patient_refused": True,
            "observation_value": None,
            "score_value": None,
            "observation_unit": "%",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "consciousness_gcs",
            "patient_refused": True,
            "observation_metadata": None,
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
    ],
    "encounter_id": "e22f5175-6283-408d-9ba4-ea3b3a5354b8",
    "obx_reference_range": "0-4",
    "obx_abnormal_flags": "N",
}
