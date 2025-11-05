.DEFAULT_GOAL       := help
TARGET_MAX_CHAR_NUM := 20

GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
WHITE  := $(shell tput -Txterm setaf 7)
RESET  := $(shell tput -Txterm sgr0)

.PHONY: help lint style static test test_rest test_websocket

## Show help
help:
	@awk '/^[a-zA-Z\-_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = substr($$1, 0, index($$1, ":")-1); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)

## Check code style
style:
	poetry run black $(if $(CI),--check,) massive test_* examples

## Check static types
static:
	poetry run mypy massive test_* examples

## Check code style and static types
lint: style static

## Update the REST API spec
rest-spec:
	poetry run python .massive/rest.py

## Update the WebSocket API spec
ws-spec:
	curl https://api.massive.com/specs/websocket.json > .massive/websocket.json

test_rest:
	poetry run python -m unittest discover -s test_rest

test_websocket:
	poetry run python -m unittest discover -s test_websocket

## Run the unit tests
test: test_rest test_websocket
