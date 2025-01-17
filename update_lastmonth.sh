#!/usr/bin/env bash

dtstamp=$(date +%Y%m%d_%H%M%S)
. ~/.virtualenvs/legistar/bin/activate

git pull
./legistar_last_month.py
git add -A
git commit -m "$dtstamp"
git push

deactivate