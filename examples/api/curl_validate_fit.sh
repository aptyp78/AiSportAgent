#!/bin/bash
curl -s -X POST http://localhost:8000/v1/validate \
  -F "file=@tests/data/good.fit" | jq .
