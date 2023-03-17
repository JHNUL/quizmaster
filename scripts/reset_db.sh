#!/bin/bash -xe

SCRIPT_DIR=$(dirname -- "$(readlink -f "${BASH_SOURCE}")")

psql -h localhost -p 5555 -U postgres < "$SCRIPT_DIR/schema.sql"
