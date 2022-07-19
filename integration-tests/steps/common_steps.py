from behave import given
from behave.runner import Context
from clients import wiremock_client
from helpers.jwt import get_system_token
from she_logging import logger


@given("I have a valid system JWT")
def get_system_jwt(context: Context) -> None:
    if not hasattr(context, "system_jwt"):
        context.system_jwt = get_system_token()
        logger.debug("system jwt: %s", context.system_jwt)


@given("the Trustomer API is running")
def setup_mock_trustomer_api(context: Context) -> None:
    wiremock_client.setup_mock_get_trustomer_config()
