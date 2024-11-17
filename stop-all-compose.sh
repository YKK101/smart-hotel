#!/bin/bash

# Navigate to the directory containing all docker-compose files
cd development-compose

# Find all docker-compose.yml files recursively inside the docker-compose directory
compose_files=$(find . -type f -name "docker-compose.yml" -o -name "docker-compose.*.yml")

# Check if any docker-compose.yml files were found
if [ -z "$compose_files" ]; then
  echo "No docker-compose.yml files found."
  exit 1
fi

# Prepare the arguments for the docker-compose command
compose_args=""
for file in $compose_files; do
  compose_args="$compose_args -f $file"
done

# Run docker-compose up with all the found docker-compose.yml files
docker-compose $compose_args down -v
