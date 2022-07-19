from typing import Any

import pytest
import requests
from flask_batteries_included.helpers.error_handler import (
    EntityNotFoundException,
    ServiceUnavailableException,
)

from dhos_rules_api.blueprint_api import controller
from dhos_rules_api.helpers import obs_set_utils


@pytest.mark.usefixtures("app")
class TestController:
    def test_score_observation_set_error(
        self, requests_mock: Any, mocker: Any, observation_set_request: Any
    ) -> None:
        requests_mock.post("http://dhos-rules-engine/news2", status_code=404)
        mocker.patch.object(
            obs_set_utils,
            "ews_from_observation_set_dict",
            return_value={"some": "request"},
        )
        with pytest.raises(ServiceUnavailableException):
            controller.score_observation_set(observation_set=observation_set_request)

    def test_execute_news2_rules_no_rules_engine(
        self, requests_mock: Any, mocker: Any, observation_set_request: Any
    ) -> None:
        requests_mock.post(
            "http://dhos-rules-engine/news2", exc=requests.exceptions.ConnectionError
        )
        mocker.patch.object(
            obs_set_utils,
            "ews_from_observation_set_dict",
            return_value={"some": "request"},
        )
        with pytest.raises(ServiceUnavailableException):
            controller.score_observation_set(observation_set=observation_set_request)

    def test_score_observation_set_success(
        self,
        requests_mock: Any,
        mocker: Any,
        observation_set_request: Any,
        observation_set_response: Any,
    ) -> None:
        requests_mock.post("http://dhos-rules-engine/news2", json={"some": "response"})
        mocker.patch.object(
            obs_set_utils,
            "ews_from_observation_set_dict",
            return_value={"some": "request"},
        )
        mocker.patch.object(
            obs_set_utils,
            "build_obs_set_response",
            return_value=observation_set_response,
        )
        actual = controller.score_observation_set(observation_set_request)
        assert actual == observation_set_response

    def test_score_meows_observation_set_success(
        self,
        requests_mock: Any,
        mocker: Any,
        meows_observation_set_request: Any,
        meows_observation_set_response: Any,
    ) -> None:
        requests_mock.post("http://dhos-rules-engine/meows", json={"some": "response"})
        mocker.patch.object(
            obs_set_utils,
            "ews_from_observation_set_dict",
            return_value={"some": "request"},
        )
        mocker.patch.object(
            obs_set_utils,
            "build_obs_set_response",
            return_value=meows_observation_set_response,
        )
        actual = controller.score_observation_set(meows_observation_set_request)
        assert actual == meows_observation_set_response

    def test_score_blood_glucose_reading_error(
        self, requests_mock: Any, mock_trustomer_config: Any
    ) -> None:
        requests_mock.post("http://dhos-rules-engine/bg_reading", status_code=404)
        bg_reading = {
            "blood_glucose_value": 22,
            "prandial_tag_id": "PRANDIAL-TAG-BEFORE-BREAKFAST",
        }
        with pytest.raises(ServiceUnavailableException):
            controller.score_blood_glucose_reading(bg_reading=bg_reading)

    def test_execute_blood_glucose_rules_no_rules_engine(
        self, requests_mock: Any, mock_trustomer_config: Any
    ) -> None:
        requests_mock.post(
            "http://dhos-rules-engine/bg_reading",
            exc=requests.exceptions.ConnectionError,
        )
        bg_reading = {
            "blood_glucose_value": 22,
            "prandial_tag_id": "PRANDIAL-TAG-BEFORE-BREAKFAST",
        }
        with pytest.raises(ServiceUnavailableException):
            controller.score_blood_glucose_reading(bg_reading=bg_reading)

    def test_score_blood_glucose_reading_success(
        self, requests_mock: Any, mock_trustomer_config: Any
    ) -> None:
        returned = {"banding_id": "score", "extra_ignored": 42}
        expected = {"banding_id": "score", "extra_ignored": 42}
        requests_mock.post("http://dhos-rules-engine/bg_reading", json=returned)
        bg_reading = {
            "blood_glucose_value": 22,
            "prandial_tag_id": "PRANDIAL-TAG-BEFORE-BREAKFAST",
            "uuid": "hello world",
        }
        actual = controller.score_blood_glucose_reading(bg_reading)
        assert actual == expected

    def test_score_blood_glucose_reading_v2_error(self, requests_mock: Any) -> None:
        requests_mock.post("http://dhos-rules-engine/bg_reading", status_code=404)
        bg_reading = {
            "blood_glucose_value": 22,
            "prandial_tag_id": "PRANDIAL-TAG-BEFORE-BREAKFAST",
            "thresholds_mmoll": {"OTHER": {"high": 7.0, "low": 4.0}},
        }
        with pytest.raises(ServiceUnavailableException):
            controller.score_blood_glucose_reading_v2(bg_reading=bg_reading)

    def test_execute_blood_glucose_v2_rules_no_rules_engine(
        self, requests_mock: Any
    ) -> None:
        requests_mock.post(
            "http://dhos-rules-engine/bg_reading",
            exc=requests.exceptions.ConnectionError,
        )
        bg_reading = {
            "blood_glucose_value": 22,
            "prandial_tag_id": "PRANDIAL-TAG-BEFORE-BREAKFAST",
            "thresholds_mmoll": {"OTHER": {"high": 7.0, "low": 4.0}},
        }
        with pytest.raises(ServiceUnavailableException):
            controller.score_blood_glucose_reading_v2(bg_reading=bg_reading)

    def test_score_blood_glucose_reading_v2_success(
        self, requests_mock: Any, mock_trustomer_config: Any
    ) -> None:
        returned = {"banding_id": "score", "extra_ignored": 42}
        expected = {"banding_id": "score", "extra_ignored": 42}
        requests_mock.post("http://dhos-rules-engine/bg_reading", json=returned)
        bg_reading = {
            "blood_glucose_value": 22,
            "prandial_tag_id": "PRANDIAL-TAG-BEFORE-BREAKFAST",
            "thresholds_mmoll": {"OTHER": {"high": 7.0, "low": 4.0}},
            "uuid": "hello world",
        }
        actual = controller.score_blood_glucose_reading_v2(bg_reading)
        assert actual == expected

    def test_retrieve_rules_success(self, requests_mock: Any) -> None:
        filename = "rule.bundle.js"
        expected = b"""
            function calculateRule(input) {
                console.log("This is the input!", input);
            }
            
            module.exports = calculateRule;
        """
        requests_mock.get(
            f"http://dhos-rules-engine/rule_definition/{filename}", content=expected
        )
        actual = controller.retrieve_rule_definition(filename=filename)
        assert actual.data == expected

    def test_retrieve_rules_no_rules_engine(self, requests_mock: Any) -> None:
        filename = "something.bundle.js"
        requests_mock.get(
            f"http://dhos-rules-engine/rule_definition/{filename}",
            exc=requests.exceptions.ConnectionError,
        )
        with pytest.raises(ServiceUnavailableException):
            controller.retrieve_rule_definition(filename=filename)

    def test_retrieve_rules_rule_not_found(self, requests_mock: Any) -> None:
        filename = "notreal.bundle.js"
        requests_mock.get(
            f"http://dhos-rules-engine/rule_definition/{filename}", status_code=404
        )
        with pytest.raises(EntityNotFoundException):
            controller.retrieve_rule_definition(filename=filename)

    def test_retrieve_rules_rule_unexpected(self, requests_mock: Any) -> None:
        filename = "something.bundle.js"
        requests_mock.get(
            f"http://dhos-rules-engine/rule_definition/{filename}", status_code=400
        )
        with pytest.raises(ServiceUnavailableException):
            controller.retrieve_rule_definition(filename=filename)
