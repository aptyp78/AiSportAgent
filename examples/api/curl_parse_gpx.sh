#!/bin/bash
curl -s -X POST http://localhost:8000/v1/parse \
  -F "file=@tests/data/mini.gpx" | jq .
