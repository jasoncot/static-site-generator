#!/bin/bash

python3 src/main.py
bash -c "cd public && python3 -m http.server 8888"