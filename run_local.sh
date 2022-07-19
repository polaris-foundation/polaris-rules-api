#!/bin/bash

SERVER_PORT=${1-5000}
export SERVER_PORT=${SERVER_PORT}
export AUTH0_DOMAIN=https://login-sandbox.sensynehealth.com/
export AUTH0_AUDIENCE=https://dev.sensynehealth.com/
export AUTH0_METADATA=https://gdm.sensynehealth.com/metadata
export AUTH0_JWKS_URL=https://login-sandbox.sensynehealth.com/.well-known/jwks.json
export ENVIRONMENT=DEVELOPMENT
export PROXY_URL=http://localhost
export HS_KEY=secret
export FLASK_APP=dhos_rules_api/autoapp.py
export IGNORE_JWT_VALIDATION=True
export LOG_LEVEL=DEBUG
export LOG_FORMAT=${LOG_FORMAT:-COLOUR}
export REDIS_INSTALLED=False
export DHOS_TRUSTOMER_API_HOST=http://dhos-trustomer
export CUSTOMER_CODE=dev
export POLARIS_API_KEY=secret

flask ${*-run}
