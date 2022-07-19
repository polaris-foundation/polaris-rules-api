import json

from flask_batteries_included.helpers.apispec import openapi_schema
from marshmallow import EXCLUDE, INCLUDE, Schema, fields

from dhos_rules_api.models.api_spec import dhos_rules_api_spec


# Marking the Object schema itself as nullable in the openapi spec seems to be necessary to get
# 'observation_metadata: null' past validation.
@openapi_schema(dhos_rules_api_spec, {"nullable": True})
class ObservationMetadata(Schema):
    class Meta:
        title = "Metadata associated with certain observations"
        unknown = EXCLUDE
        ordered = True

    gcs_eyes = fields.Integer(required=False, allow_none=True)
    gcs_eyes_description = fields.String(required=False, allow_none=True)
    gcs_verbal = fields.Integer(required=False, allow_none=True)
    gcs_verbal_description = fields.String(required=False, allow_none=True)
    gcs_motor = fields.Integer(required=False, allow_none=True)
    gcs_motor_description = fields.String(required=False, allow_none=True)
    mask = fields.String(required=False, allow_none=True)
    mask_percent = fields.Integer(required=False, allow_none=True)
    patient_position = fields.String(required=False, allow_none=True)


@openapi_schema(dhos_rules_api_spec)
class Observation(Schema):
    class Meta:
        title = "Unscored Observation"
        unknown = EXCLUDE
        ordered = True

    observation_type = fields.String(required=True)
    patient_refused = fields.Boolean(required=False, allow_none=True)
    observation_value = fields.Number(required=False, allow_none=True)
    observation_string = fields.String(required=False, allow_none=True)
    observation_unit = fields.String(required=False, allow_none=True)
    measured_time = fields.String(required=True)
    observation_metadata = fields.Nested(
        ObservationMetadata, required=False, many=False, allow_none=True
    )


@openapi_schema(dhos_rules_api_spec)
class ObservationResponse(Observation):
    class Meta:
        title = "Scored Observation"
        unknown = EXCLUDE
        ordered = True

    score_value = fields.Integer(required=True)


OBSERVATIONSET_EXAMPLE = {
    "score_system": "news2",
    "score_string": "T",
    "score_value": 12,
    "score_severity": "bad",
    "record_time": "2017-09-23T08:31:19.123+00:00",
    "spo2_scale": 2,
    "observations": [
        {
            "observation_type": "temperature",
            "patient_refused": False,
            "score_value": 5,
            "observation_value": 28.4,
            "observation_string": "",
            "observation_unit": "celsius",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "diastolic_blood_pressure",
            "patient_refused": False,
            "score_value": 8,
            "observation_value": 245,
            "observation_string": "",
            "observation_unit": "mmHg",
            "observation_metadata": {"patient_position": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "systolic_blood_pressure",
            "patient_refused": False,
            "score_value": 7,
            "observation_value": 281,
            "observation_string": "",
            "observation_unit": "mmHg",
            "observation_metadata": {"patient_position": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "heart_rate",
            "patient_refused": False,
            "score_value": 3,
            "observation_value": 160,
            "observation_string": "",
            "observation_unit": "bpm",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "respiratory_rate",
            "patient_refused": False,
            "score_value": 3,
            "observation_value": 55,
            "observation_string": "",
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
            "observation_type": "consciousness_acvpu",
            "patient_refused": False,
            "score_value": 4,
            "observation_string": "Alert",
            "observation_metadata": {"patient_position": "sitting"},
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "nurse_concern",
            "patient_refused": False,
            "score_value": 4,
            "observation_string": "Infection",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "spo2",
            "patient_refused": False,
            "score_value": 3,
            "observation_value": 55,
            "observation_unit": "%",
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
        {
            "observation_type": "consciousness_gcs",
            "patient_refused": False,
            "score_value": 4,
            "observation_metadata": {
                "gcs_eyes": 4,
                "gcs_eyes_description": "Spontaenous",
                "gcs_verbal": 2,
                "gcs_verbal_description": "Oriented",
                "gcs_motor": 3,
                "gcs_motor_description": "Commands",
            },
            "measured_time": "2017-09-23T08:29:19.123+00:00",
        },
    ],
    "encounter_id": "e22f5175-6283-408d-9ba4-ea3b3a5354b8",
    "is_partial": False,
    "monitoring_instruction": "low_medium_monitoring",
    "empty_set": False,
    "ranking": "0101010,2017-09-23T08:29:19.123+00:00",
    "obx_reference_range": "0-4",
    "obx_abnormal_flag": "EXTHIGH",
}


class UnscoredObservationSetSchema(Schema):
    class Meta:
        title = "Unscored Observation Set"
        unknown = INCLUDE
        ordered = True

    record_time = fields.String(required=True)
    spo2_scale = fields.Integer(required=False, allow_none=True)
    observations = fields.List(fields.Nested(Observation), required=True)
    score_system = fields.String(required=True)


# OpenAPI request example is created by parsing the response with the score fields excluded. Note that the loaded
# schema is a recursive OrderedDict, so we use the json library to simplify it to a dict, which apispec can understand.
unscored_example = UnscoredObservationSetSchema().load(
    OBSERVATIONSET_EXAMPLE, unknown=EXCLUDE
)
openapi_schema(
    dhos_rules_api_spec,
    {"example": json.loads(json.dumps(unscored_example))},
)(UnscoredObservationSetSchema)


@openapi_schema(dhos_rules_api_spec, {"example": OBSERVATIONSET_EXAMPLE})
class ScoredObservationSetSchema(UnscoredObservationSetSchema):
    class Meta:
        title = "Scored Observation Set"
        unknown = INCLUDE
        ordered = True

    is_partial = fields.Boolean(required=True)
    empty_set = fields.Boolean(required=True, allow_none=True)
    time_next_obs_set_due = fields.String(required=True)
    monitoring_instruction = fields.String(required=True)
    score_string = fields.String(required=True)
    score_value = fields.Integer(required=True)
    score_severity = fields.String(required=True)
    observations = fields.List(fields.Nested(ObservationResponse), required=True)
    ranking = fields.String(required=True)
    obx_reference_range = fields.String(required=True)
    obx_abnormal_flags = fields.String(required=True, description="N, HIGH, EXTHIGH")
