from pathlib import Path

import connexion
from connexion import FlaskApp
from flask import Flask
from flask_batteries_included import augment_app
from flask_batteries_included.config import is_not_production_environment
from she_logging import logger

from dhos_rules_api import blueprint_api
from dhos_rules_api.config import init_config
from dhos_rules_api.helpers.cli import add_cli_command


def create_app(testing: bool = False) -> Flask:
    connexion_app: FlaskApp = connexion.App(
        __name__,
        specification_dir=Path(__file__).parent / "openapi",
        options={"swagger_ui": is_not_production_environment()},
    )
    connexion_app.add_api("openapi.yaml", strict_validation=True)
    app: Flask = augment_app(app=connexion_app.app, use_auth0=True, testing=testing)

    init_config(app)

    app.register_blueprint(blueprint_api.api_blueprint, url_prefix="/dhos")
    logger.info("Registered API blueprint")

    # Done!
    logger.info("App ready to serve requests")

    add_cli_command(app)

    return app
