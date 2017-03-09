#!/bin/bash
body='{
"request": {
  "branch":"master"
}}'

curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Travis-API-Version: 3" \
  -H "Authorization: token YOUR_TOKEN" \
  -d "$body" \
  https://api.travis-ci.org/repo/musescore%2Ftx2s3/requests
