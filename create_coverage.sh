#!/bin/bash


set -x

export PATH=$PWD/test/bin:/usr/bin/:$PATH
nosetests --with-timer --with-coverage --cover-erase --cover-html --cover-html-dir=coverage \
--cover-package=scheduler \
test/test_submission.py \
test/test_ecflow.py \
|| exit 1


