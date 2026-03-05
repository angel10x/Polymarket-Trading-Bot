#!/usr/bin/env bash
# run-local.sh is a script that runs the market maker locally.
export $(xargs <config.env)
./bin/run
