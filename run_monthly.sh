#!/bin/bash

# $1 path to work directory

cd "$1"

pipenv run python ParseSessions.py