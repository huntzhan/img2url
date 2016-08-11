#!/usr/bin/env bash
PROJECT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
for line in $(cat "${PROJECT_DIR}/requirements.txt" | grep -v ^#)
do
  pip install $line
done
