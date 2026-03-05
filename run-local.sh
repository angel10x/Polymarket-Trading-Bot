#!/usr/bin/env bash

export $(xargs <config.env)
./bin/run
