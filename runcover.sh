#!/usr/bin/bash

.tox/py35/bin/coverage run --source=autoslug/ run_tests.py
coverage html
firefox htmlcov/index.html
