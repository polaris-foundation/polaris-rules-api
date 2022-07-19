from flask_batteries_included.helpers.apispec import openapi_schema
from marshmallow import Schema, fields

from dhos_rules_api.models.api_spec import dhos_rules_api_spec


@openapi_schema(dhos_rules_api_spec)
class BloodGlucoseBandingRequest(Schema):
    class Meta:
        title = "Blood Glucose Reading"
        ordered = True

    blood_glucose_value = fields.Number(
        required=True, example=22, description="Value of the blood glucose reading"
    )
    prandial_tag_id = fields.String(
        required=True,
        example="PRANDIAL-TAG-BEFORE-BREAKFAST",
        description="Prandial tag for this reading",
    )


@openapi_schema(dhos_rules_api_spec)
class HighLow(Schema):
    class Meta:
        title = "High and low thresholds"
        ordered = True

    high = fields.Number(required=True)
    low = fields.Number(required=True)


@openapi_schema(dhos_rules_api_spec)
class BloodGlucoseThresholds(Schema):
    class Meta:
        title = "Blood Glucose Thresholds"
        ordered = True

    other = fields.Nested(
        HighLow, required=True, data_key="OTHER", example={"high": 7.8, "low": 4.0}
    )
    before_breakfast = fields.Nested(
        HighLow, data_key="BEFORE-BREAKFAST", example={"high": 7.8, "low": 4.0}
    )
    after_breakfast = fields.Nested(
        HighLow, data_key="AFTER-BREAKFAST", example={"high": 7.8, "low": 4.0}
    )
    before_lunch = fields.Nested(
        HighLow, data_key="BEFORE-LUNCH", example={"high": 7.8, "low": 4.0}
    )
    after_lunch = fields.Nested(
        HighLow, data_key="AFTER-LUNCH", example={"high": 7.8, "low": 4.0}
    )
    before_dinner = fields.Nested(
        HighLow, data_key="BEFORE-DINNER", example={"high": 7.8, "low": 4.0}
    )
    after_dinner = fields.Nested(
        HighLow, data_key="AFTER-DINNER", example={"high": 7.8, "low": 4.0}
    )


@openapi_schema(dhos_rules_api_spec)
class BloodGlucoseBandingRequestV2(BloodGlucoseBandingRequest):
    class Meta:
        title = "Blood Glucose Reading V2"
        ordered = True

    thresholds_mmoll = fields.Nested(
        BloodGlucoseThresholds,
        required=True,
        description="Blood Glucose Banding Thresholds",
    )


@openapi_schema(dhos_rules_api_spec)
class BloodGlucoseBanding(Schema):
    class Meta:
        title = "Blood Glucose Banding"
        ordered = True

    banding_id = fields.String(
        example="BG-READING-BANDING-NORMAL", description="Banding the reading fits into"
    )
