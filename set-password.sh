#!/bin/sh
. env/bin/activate
FLASK_APP=aliasmanager.py flask set-password "$@"
