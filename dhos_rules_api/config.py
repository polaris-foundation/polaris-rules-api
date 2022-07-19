from environs import Env
from flask import Flask


class Configuration:
    env = Env()
    DHOS_RULES_ENGINE_URL: str = env.str(
        "DHOS_RULES_ENGINE_URL", "http://localhost:3000"
    )
    CUSTOMER_CODE: str = env.str("CUSTOMER_CODE")
    DHOS_TRUSTOMER_API_HOST: str = env.str("DHOS_TRUSTOMER_API_HOST")
    POLARIS_API_KEY: str = env.str("POLARIS_API_KEY")
    TRUSTOMER_CONFIG_CACHE_TTL_SEC: int = env.int(
        "TRUSTOMER_CONFIG_CACHE_TTL_SEC", 60 * 60  # Cache for 1 hour by default.
    )


def init_config(app: Flask) -> None:
    app.config.from_object(Configuration)
