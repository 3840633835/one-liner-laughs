#!/bin/sh
# Determinism check: running main.py twice into two fresh output dirs
# must produce byte-identical entry.txt files.
set -e
cd "$(dirname "$0")"
rm -rf /tmp/oll-det-a /tmp/oll-det-b
mkdir -p /tmp/oll-det-a /tmp/oll-det-b
MAKEFUN_OUTPUT_DIR=/tmp/oll-det-a python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/oll-det-b python3 main.py
cmp /tmp/oll-det-a/entry.txt /tmp/oll-det-b/entry.txt
cmp /tmp/oll-det-a/entry.txt entry.txt
echo "determinism PASS"
