#!/bin/bash
dropdb orchestrator-core
createdb orchestrator-core
psql -d orchestrator-core < db.psql
