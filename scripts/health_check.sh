#!/usr/bin/env bash

set -o pipefail

URLS=(
  '/v1/results'
  '/v1/matches'
  '/v1/news'
  '/v1/rankings'
  '/v1/stats'
)

for url in ${URLS[@]}; do
  full_url=("http://hltv-api.herokuapp.com"$url)
  res=$(curl -fsSI "$full_url" | grep "HTTP/1.1")
  res=${res%$'\r'}  # remove a trailing carriage return if present on the end of the line
  if [ "$res" != "HTTP/1.1 200 OK" ]; then
    exit 1
  fi
done

exit 0

