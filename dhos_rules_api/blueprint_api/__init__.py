from typing import Dict

from flask import Blueprint, Response, jsonify
from flask_batteries_included.helpers.security import protected_route
from flask_batteries_included.helpers.security.endpoint_security import scopes_present
from marshmallow import INCLUDE, ValidationError
from she_logging import logger

from dhos_rules_api.blueprint_api import controller
from dhos_rules_api.models.blood_glucose import (
    BloodGlucoseBandingRequest,
    BloodGlucoseBandingRequestV2,
)
from dhos_rules_api.models.observation_set import UnscoredObservationSetSchema

api_blueprint: Blueprint = Blueprint("api", __name__)


@api_blueprint.route("/v1/score_observation_set", methods=["POST"])
@protected_route(scopes_present(required_scopes="read:send_rule"))
def score_observation_set(observation_set: Dict[str, object]) -> Response:
    """Score a set of observations using news 2
    ---
    post:
      summary: Compute scores for an observation set
      description: >-
        Input is an observation set to be score, result is the same
        observation set with scores added.
      tags:
        - send-scores
      requestBody:
        description: >-
            JSON body of observations contained in the current set.
            Note: Additional fields may be present and will be returned in the result
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UnscoredObservationSetSchema'
              x-body-name: observation_set
      responses:
        '200':
          description: "JSON body of observations contained in the current set"
          content:
            application/json:
              schema: ScoredObservationSetSchema
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    logger.debug("Received request to score obs set")
    try:
        observation_set = UnscoredObservationSetSchema().load(observation_set)
    except ValidationError as err:
        logger.error("Error parsing observation set: %s", err.messages)
        raise ValueError("Error validating request body")

    return jsonify(controller.score_observation_set(observation_set=observation_set))


@api_blueprint.route("/v1/score_blood_glucose_reading", methods=["POST"])
@protected_route(scopes_present(required_scopes="read:gdm_rule"))
def score_blood_glucose_reading(bg_reading: Dict[str, object]) -> Response:
    """
    ---
    post:
      summary: Compute banding id from Blood Glucose and Prandial Tag
      tags:
        - gdm-scores
      requestBody:
        description: "JSON body of current blood glucose reading"
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BloodGlucoseBandingRequest'
              x-body-name: bg_reading
      responses:
        '200':
          description: "Blood glucose reading banded"
          content:
            application/json:
              schema: BloodGlucoseBanding
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    try:
        bg_reading = BloodGlucoseBandingRequest(unknown=INCLUDE).load(bg_reading)
    except ValidationError as err:
        logger.error("Error parsing blood glucose reading: %s", err.messages)
        raise ValueError("Error validating request body")

    logger.debug("Received request to score BG reading")
    response = controller.score_blood_glucose_reading(bg_reading=bg_reading)
    return jsonify(response)


@api_blueprint.route("/v2/score_blood_glucose_reading", methods=["POST"])
@protected_route(scopes_present(required_scopes="read:gdm_rule"))
def score_blood_glucose_reading_v2(bg_reading: Dict[str, object]) -> Response:
    """
    ---
    post:
      summary: Compute banding id from Blood Glucose and Prandial Tag
      tags:
        - gdm-scores
      requestBody:
        description: "Score blood glucose reading request"
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/BloodGlucoseBandingRequestV2'
              x-body-name: bg_reading
      responses:
        '200':
          description: "Blood glucose reading banded"
          content:
            application/json:
              schema: BloodGlucoseBanding
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    try:
        bg_reading = BloodGlucoseBandingRequestV2(unknown=INCLUDE).load(bg_reading)
    except ValidationError as err:
        logger.error("Error parsing blood glucose reading: %s", err.messages)
        raise ValueError("Error validating request body")

    logger.debug("Received request to score BG reading")
    response = controller.score_blood_glucose_reading_v2(bg_reading=bg_reading)
    return jsonify(response)


# In future this could stream back the response
# But our current rules files are too small to need it
# And it may be a design/code smell if they do become that big
#
# This endpoint is deliberately left unprotected, as it only serves back code and open source licences
@api_blueprint.route("/v1/rule_definition/<string:filename>")
def retrieve_rule_definition(filename: str) -> Response:
    """
    ---
    get:
      summary: "Retrieve rules Javascript to run scoring in the browser"
      description: >-
          Returns a compressed javascript module that contains a scoring engine.
      tags:
        - rules
      parameters:
        - in: path
          name: filename
          required: true
          schema: RuleDefinitionParameter
      responses:
        '200':
          description: "Returns a javascript scoring engine"
          content:
            application/json:
              schema:
                type: string
                example: "... some compressed javascript ..."
        default:
          description: >-
            Error, e.g. 404 Not Found
          content:
            application/json:
              schema: Error
    """
    logger.debug("Received request to stream rule definition")
    return controller.retrieve_rule_definition(filename=filename)
