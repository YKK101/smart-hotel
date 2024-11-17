#!/bin/sh

url="$1"

echo "Waiting for $url to be available..."

while ! curl -s "$url" >/dev/null; do
  echo "Still waiting for $url..."
  sleep 10
done

echo "$url is available!"
