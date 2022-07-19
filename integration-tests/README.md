# dhos-rules-api Integration Tests
This folder contains service-level integration tests for the Rules API.

## Running the tests
```
# run tests
$ make test-local
```

## Test development
For test development purposes you can keep the service running and keep re-running only the tests:
```
# in one terminal screen, or add `-d` flag if you don't want the process running in foreground
$ docker-compose up --force-recreate

# in another terminal screen you can now run the tests
$ DHOS_RULES_BASE_URL="http://localhost:5000" \
  HS_ISSUER="http://localhost/" \
  HS_KEY=secret \
  PROXY_URL="http://localhost" \
  SYSTEM_JWT_SCOPE="read:gdm_rule read:send_rule"  \
  behave --no-capture --logging-level DEBUG

# inspect test logs
$ docker logs dhos-rules-integration-tests

# Don't forget to clean up when done!
$ docker-compose down
```
