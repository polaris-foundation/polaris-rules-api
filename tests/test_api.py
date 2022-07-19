from typing import Any, Dict, Optional

import flask
import pytest


@pytest.fixture
def mock_bearer_validation(mocker: Any) -> Any:
    from jose import jwt

    mocked = mocker.patch.object(jwt, "get_unverified_claims")
    mocked.return_value = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": 1_516_239_022,
        "iss": "http://localhost/",
    }
    return mocked


class TestApi:
    @pytest.mark.parametrize(
        "extra_fields",
        [
            None,
            {
                "uuid": "2c4f1d24-2952-4d4e-b1d1-3637e33cc161",
                "created": "2017-09-23T08:29:19.123+00:00",
                "modified": "2017-09-23T08:29:19.123+00:00",
            },
        ],
    )
    def test_score_observation_set_success(
        self,
        mocker: Any,
        client: Any,
        observation_set_request: Any,
        mock_bearer_validation: Any,
        extra_fields: Optional[Dict],
    ) -> None:
        if extra_fields:
            observation_set_request.update(extra_fields)
        expected = {"key": "value"}
        mock_controller = mocker.patch("dhos_rules_api.blueprint_api.controller")
        mock_controller.score_observation_set.return_value = expected
        response = client.post(
            f"/dhos/v1/score_observation_set",
            json=observation_set_request,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.get_json() == expected
        assert mock_bearer_validation.called_once_with("TOKEN")

    @pytest.mark.parametrize("body", [{"wrong": "schema"}, "some_string", None])
    def test_score_observation_set_invalid(
        self, client: Any, mock_bearer_validation: Any, body: Any
    ) -> None:
        response = client.post(
            f"/dhos/v1/score_observation_set",
            json=body,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_score_observation_set_unknown_score_system(
        self, client: Any, mock_bearer_validation: Any, observation_set_request: Any
    ) -> None:
        observation_set_request["score_system"] = "something_else"
        response = client.post(
            f"/dhos/v1/score_observation_set",
            json=observation_set_request,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_score_blood_glucose_reading_success(
        self, mocker: Any, mock_bearer_validation: Any, client: Any
    ) -> None:
        expected = {"key": "value"}
        mock_controller = mocker.patch("dhos_rules_api.blueprint_api.controller")
        mock_controller.score_blood_glucose_reading.return_value = expected
        response = client.post(
            f"/dhos/v1/score_blood_glucose_reading",
            json={
                "blood_glucose_value": 22,
                "prandial_tag_id": "PRANDIAL-TAG-BEFORE-BREAKFAST",
            },
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.get_json() == expected

    @pytest.mark.parametrize("body", [{"wrong": "schema"}, "some_string", None])
    def test_score_blood_glucose_reading_invalid(
        self, client: Any, mock_bearer_validation: Any, body: Any
    ) -> None:
        response = client.post(
            f"/dhos/v1/score_blood_glucose_reading",
            json=body,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    @pytest.mark.parametrize(
        "body,expected",
        [
            # ({"wrong": "schema"}, 400),
            (None, 200)
        ],
    )
    def test_retrieve_rule_definition(
        self, client: Any, requests_mock: Any, body: Any, expected: int
    ) -> None:
        filename = "some.rules.js"
        requests_mock.get(
            f"http://dhos-rules-engine/rule_definition/{filename}",
            text="""
            function calculateRule(input) {
                console.log("This is the input!", input);
            }
            
            module.exports = calculateRule;
        """,
        )

        response = client.get(
            flask.url_for("api.retrieve_rule_definition", filename=filename), json=body
        )
        assert response.status_code == expected

    def test_score_blood_glucose_reading_v2_success(
        self, mocker: Any, mock_bearer_validation: Any, client: Any
    ) -> None:
        expected = {"key": "value"}
        mock_controller = mocker.patch("dhos_rules_api.blueprint_api.controller")
        mock_controller.score_blood_glucose_reading_v2.return_value = expected
        response = client.post(
            f"/dhos/v2/score_blood_glucose_reading",
            json={
                "blood_glucose_value": 22,
                "prandial_tag_id": "PRANDIAL-TAG-BEFORE-BREAKFAST",
                "thresholds_mmoll": {"OTHER": {"high": 7.0, "low": 4.0}},
            },
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.get_json() == expected

    @pytest.mark.parametrize(
        "body",
        [
            {"wrong": "schema"},
            "some_string",
            None,
            {
                "blood_glucose_value": 22,
                "prandial_tag_id": "PRANDIAL-TAG-BEFORE-BREAKFAST",
            },
        ],
    )
    def test_score_blood_glucose_reading_v2_invalid(
        self, client: Any, mock_bearer_validation: Any, body: Any
    ) -> None:
        response = client.post(
            f"/dhos/v2/score_blood_glucose_reading",
            json=body,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400
