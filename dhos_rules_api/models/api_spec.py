from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_batteries_included.helpers.apispec import (
    FlaskBatteriesPlugin,
    initialise_apispec,
    openapi_schema,
)
from marshmallow import Schema, fields

dhos_rules_api_spec: APISpec = APISpec(
    version="1.0.0",
    openapi_version="3.0.3",
    title="DHOS Rules API",
    info={
        "description": "The DHOS Rules API is responsible for scoring observation sets and blood glucose readings using defined rules."
    },
    plugins=[FlaskPlugin(), MarshmallowPlugin(), FlaskBatteriesPlugin()],
)

initialise_apispec(dhos_rules_api_spec)


@openapi_schema(dhos_rules_api_spec)
class RuleDefinitionParameter(Schema):
    class Meta:
        ordered = True

    filename = fields.String(required=True, description="Filename to retrieve")
