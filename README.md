<!-- Title - A concise title for the service that fits the pattern identified and in use across all services. -->
# Polaris Rules API

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

<!-- Description - Fewer than 500 words that describe what a service delivers, providing an informative, descriptive, and comprehensive overview of the value a service brings to the table. -->
The Rules API is part of the Polaris platform (formerly DHOS). This service is for calculating outputs from inputs given certain internal rules.

**This service wraps the Polaris Rules Engine.**

## Maintainers
The Polaris platform was created by Sensyne Health Ltd., and has now been made open-source. As a result, some of the
instructions, setup and configuration will no longer be relevant to third party contributors. For example, some of
the libraries used may not be publicly available, or docker images may not be accessible externally. In addition, 
CICD pipelines may no longer function.

For now, Sensyne Health Ltd. and its employees are the maintainers of this repository.

## Setup
These setup instructions assume you are using out-of-the-box installations of:
- `pre-commit` (https://pre-commit.com/)
- `pyenv` (https://github.com/pyenv/pyenv)
- `poetry` (https://python-poetry.org/)

You can run the following commands locally:
```bash
make install  # Creates a virtual environment using pyenv and installs the dependencies using poetry
make lint  # Runs linting/quality tools including black, isort and mypy
make test  # Runs unit tests
```

You can also run the service locally using the script `run_local.sh`, or in dockerized form by running:
```bash
docker build . -t <tag>
docker run <tag>
```

## Documentation
<!-- Include links to any external documentation including relevant ADR documents.
     Insert API endpoints using markdown-swagger tags (and ensure the `make openapi` target keeps them up to date).
     -->
This service originally formed part of the dhos-services-api but was split to its own services as part of [ADR016](https://sensynehealth.atlassian.net/wiki/spaces/SENS/pages/207519760/ADR016+Locations+service)
<!-- markdown-swagger -->
 Endpoint                               | Method | Auth? | Description                                                                                   
 -------------------------------------- | ------ | ----- | ----------------------------------------------------------------------------------------------
 `/running`                             | GET    | No    | Verifies that the service is running. Used for monitoring in kubernetes.                      
 `/version`                             | GET    | No    | Get the version number, circleci build number, and git hash.                                  
 `/dhos/v1/score_observation_set`       | POST   | Yes   | Input is an observation set to be score, result is the same observation set with scores added.
 `/dhos/v1/score_blood_glucose_reading` | POST   | Yes   |                                                                                               
 `/dhos/v2/score_blood_glucose_reading` | POST   | Yes   |                                                                                               
 `/dhos/v1/rule_definition/{filename}`  | GET    | No    | Returns a compressed javascript module that contains a scoring engine.                        
<!-- /markdown-swagger -->

## Requirements
<!-- An outline of what other services, tooling, and libraries needed to make a service operate, providing a
  complete list of EVERYTHING required to work properly. -->
  At a minimum you require a system with Python 3.9. Tox 3.20 is required to run the unit tests, docker with docker-compose are required to run integration tests. See [Development environment setup](https://sensynehealth.atlassian.net/wiki/spaces/SPEN/pages/3193270/Development%2Benvironment%2Bsetup) for a more detailed list of tools that should be installed.
  
## Deployment
<!-- Setup - A step by step outline from start to finish of what is needed to setup and operate a service, providing as
  much detail as you possibly for any new user to be able to get up and running with a service. -->
  
  All development is done on a branch tagged with the relevant ticket identifier.
  Code may not be merged into develop unless it passes all CircleCI tests.
  :partly_sunny: After merging to develop tests will run again and if successful the code is built in a docker container and uploaded to our Azure container registry. It is then deployed to test environments controlled by Kubernetes.

## Testing
<!-- Testing - Providing details and instructions for mocking, monitoring, and testing a service, including any services or
  tools used, as well as links or reports that are part of active testing for a service. -->

### Unit tests
:microscope: Either use `make` or run `tox` directly.

<!-- markdown-make Makefile tox.ini -->
`tox` : Running `make test` or tox with no arguments runs `tox -e lint,default`

`make clean` : Remove tox and pyenv virtual environments.

`tox -e debug` : Runs last failed unit tests only with debugger invoked on failure. Additional py.test command line arguments may given preceded by `--`, e.g. `tox -e debug -- -k sometestname -vv`

`make default` (or `tox -e default`) : Installs all dependencies, verifies that lint tools would not change the code, runs security check programs then runs unit tests with coverage. Running `tox -e py39` does the same but without starting a database container.

`tox -e flask` : Runs flask within the tox environment. Pass arguments after `--`. e.g. `tox -e flask -- --help` for a list of commands. Use this to create database migrations.

`make help` : Show this help.

`make lint` (or `tox -e lint`) : Run `black`, `isort`, and `mypy` to clean up source files.

`make openapi` (or `tox -e openapi`) : Recreate API specification (openapi.yaml) from Flask blueprint

`make pyenv` : Create pyenv and install required packages (optional).

`make readme` (or `tox -e readme`) : Updates the README file with database diagram and commands. (Requires graphviz `dot` is installed)

`make test` : Test using `tox`

`make update` (or `tox -e update`) : Updates the `poetry.lock` file from `pyproject.toml`

<!-- /markdown-make -->

## Integration tests
:nut_and_bolt: Integration tests are located in the `integration-tests` sub-directory. After changing into this directory you can run the following commands:

<!-- markdown-make integration-tests/Makefile -->
<!-- /markdown-make -->

## Issue tracker
:bug: Bugs related to this microservice should be raised on Jira as [PLAT-###](https://sensynehealth.atlassian.net/issues/?jql=project%20%3D%20PLAT%20AND%20component%20%3D%20Locations) tickets with the component set to Locations.

## Configuration
<!-- Configuration - An outline of all configuration and environmental variables that can be adjusted or customized as part
  of service operations, including as much detail on default values, or options that would produce different known
  results for a service. -->
  * `LOG_LEVEL=ERROR|WARN|INFO|DEBUG` sets the log level
  * `LOG_FORMAT=colour|plain|json` configure logging format. JSON is used for the running system but the others may be more useful during development.

## Early Warning Score calculations

The Rules API provides endpoints for scoring sets of vital sign observations, returning an early warning score by using scoring systems such as NEWS2.

`POST /dhos/v1/execute_observation_set_news2_rules`

Body:
```
{
  "time": "2018-01-01T00:00:00.000Z",
  "heart_rate": 60,
  ...
}
``` 

Response:
```
{
  "heart_rate_score": 0,
  "overall_score": 0,
  "overall_severity": "low",
  ...
}
``` 

## Blood glucose reading banding

The Rules API provides endpoints for banding blood glucose readings.

`POST /dhos/v1/blood_glucose_rules`

Body:
```
{
  "blood_glucose_value": 6.5,
  "prandial_tag_id": "PRANDIAL-TAG-BEFORE-BREAKFAST",
  ...
}
``` 

Response:
```
{
  "banding_id": "BG-READING-BANDING-NORMAL"
}
``` 
