#!/bin/bash

# Prompt user for input variables
read -p "Enter Hotel Number: " HOTEL_NO
read -p "Enter Floor Number: " FLOOR_NO
read -p "Enter Room Number: " ROOM_NO
read -p "Enter PostgreSQL User: " PG_USER
read -sp "Enter PostgreSQL Password: " PG_PASSWORD; echo
read -p "Enter PostgreSQL Expose Port (54XX): " PG_EXPOSE_PORT
read -p "Enter EMQX Expose Port (18XX): " EMQX_EXPOSE_PORT
read -p "Enter LifeBeing Sensor Expose Port (8XXX): " LIFEBEING_SENSOR_EXPOSE_PORT
read -p "Enter LifeBeing Sensor Device ID (EX: LB-R101-1): " LIFEBEING_SENSOR_DEVICE_ID
read -p "Enter IAQ Sensor Expose Port (80XX): " IAQ_SENSOR_EXPOSE_PORT
read -p "Enter IAQ Sensor Device ID (EX: IQA-R101-1): " IAQ_SENSOR_DEVICE_ID
read -p "Enter IAQ Device Expose Port (80XX): " IAQ_DEVICE_EXPOSE_PORT

# Auto-generate UUIDs for secrets
LIFEBEING_SENSOR_SECRET=$(uuidgen)
IAQ_SENSOR_SECRET=$(uuidgen)
IAQ_DEVICE_SECRET=$(uuidgen)
LIFEBEING_AGENT_SECRET=$(uuidgen)
IAQ_AGENT_SECRET=$(uuidgen)
DATALOGGER_SECRET=$(uuidgen)
DEVICE_CONTROLLER_SECRET=$(uuidgen)
OCCUPENCY_DETECTOR_SECRET=$(uuidgen)

# Template file
TEMPLATE_FILE="./template/docker-compose-room-template.yml"

# Output directory and file
OUTPUT_FILE="docker-compose.${HOTEL_NO}-${FLOOR_NO}-${ROOM_NO}.yml"

# Check if template file exists
if [[ ! -f $TEMPLATE_FILE ]]; then
  echo "Error: Template file '$TEMPLATE_FILE' not found!"
  exit 1
fi

# Replace placeholders in the template and generate the output file
sed -e "s/\[VARIABLE_ROOM_NO\]/$ROOM_NO/g" \
    -e "s/\[VARIABLE_PG_USER\]/$PG_USER/g" \
    -e "s/\[VARIABLE_PG_PASSWORD\]/$PG_PASSWORD/g" \
    -e "s/\[VARIABLE_PG_EXPOSE_PORT\]/$PG_EXPOSE_PORT/g" \
    -e "s/\[VARIABLE_EMQX_EXPOSE_PORT\]/$EMQX_EXPOSE_PORT/g" \
    -e "s/\[VARIABLE_LIFEBEING_SENSOR_EXPOSE_PORT\]/$LIFEBEING_SENSOR_EXPOSE_PORT/g" \
    -e "s/\[VARIABLE_LIFEBEING_SENSOR_SECRET\]/$LIFEBEING_SENSOR_SECRET/g" \
    -e "s/\[VARIABLE_LIFEBEING_SENSOR_DEVICE_ID\]/$LIFEBEING_SENSOR_DEVICE_ID/g" \
    -e "s/\[VARIABLE_IAQ_SENSOR_EXPOSE_PORT\]/$IAQ_SENSOR_EXPOSE_PORT/g" \
    -e "s/\[VARIABLE_IAQ_SENSOR_SECRET\]/$IAQ_SENSOR_SECRET/g" \
    -e "s/\[VARIABLE_IAQ_SENSOR_DEVICE_ID\]/$IAQ_SENSOR_DEVICE_ID/g" \
    -e "s/\[VARIABLE_IAQ_DEVICE_EXPOSE_PORT\]/$IAQ_DEVICE_EXPOSE_PORT/g" \
    -e "s/\[VARIABLE_IAQ_DEVICE_SECRET\]/$IAQ_DEVICE_SECRET/g" \
    -e "s/\[VARIABLE_LIFEBEING_AGENT_SECRET\]/$LIFEBEING_AGENT_SECRET/g" \
    -e "s/\[VARIABLE_HOTEL_NO\]/$HOTEL_NO/g" \
    -e "s/\[VARIABLE_FLOOR_NO\]/$FLOOR_NO/g" \
    -e "s/\[VARIABLE_IAQ_AGENT_SECRET\]/$IAQ_AGENT_SECRET/g" \
    -e "s/\[VARIABLE_DATALOGGER_SECRET\]/$DATALOGGER_SECRET/g" \
    -e "s/\[VARIABLE_DEVICE_CONTROLLER_SECRET\]/$DEVICE_CONTROLLER_SECRET/g" \
    -e "s/\[VARIABLE_OCCUPENCY_DETECTOR_SECRET\]/$OCCUPENCY_DETECTOR_SECRET/g" \
    $TEMPLATE_FILE > $OUTPUT_FILE

echo "Docker Compose file generated at '$OUTPUT_FILE'."
