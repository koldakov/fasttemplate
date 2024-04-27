#!/usr/bin/env bash

<%text>if [ -z "${PORT}" ]
then
  PORT=8080
fi</%text>

poetry run hypercorn -b :$PORT -k uvloop ${project["src_rel_path"]}.main:app
