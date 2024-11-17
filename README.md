# Smart Hotel

## Directory Structure

```
smart-hotel/
│
├── hotel_system/
│   │
│   ├── room_system/
│   │   │
│   │   ├── data_logger/ 
│   │   │
│   │   ├── device_controller/
│   │   │
│   │   ├── device_simulator/
│   │   │
│   │   ├── occupancy_detection_service/
│   │   │
│   │   ├── sensor_agent/
│   │   │
│   │   ├── sensor_simulator/
│
├── central_backend/
│   │
│   ├── central_debezium_resources
│   │   ├── create_postgres_sink_connector.sh
│
├── development-compose/
│   │
│   ├── configs/
│   │   ├── device-config.json
│   │   ├── sensor-to-device.json
│   │
│   ├── template/
│   │   ├── docker-compose-room-template.yml
│   │
│   ├── generate-room-compose-file.sh
│
├── run-development.sh
│
├── stop-all-compose.sh
```

#### Explanation
- __hotel_system__: Directory for hotel-level files (e.g., future HVAC-related modules).
    - __room_system__: Directory for room-level files.
        - __data_logger__: Django project subscribes to sensor events and logs them to a local database.
        - __device_controller__: Django project subscribes to the device control topic and triggers changes on a specific device.
        - __device_simulator__: IoT device simulator.
        - __occupancy_detection_service__: Django project subscribes to presence state changes and publishes device control commands if needed.
        - __sensor_agent__: Agent schedules and fetches updates from IoT sensors.
        - __sensor_simulator__: IoT sensor simulator.
- __central_backend__: Directory for cloud backend _(WIP - not implemented yet).
    - __central_debezium_resources__: Directory for storing resources for Debezium to connect to the cloud database.
        - create_postgres_sink_connectors.sh: Shell script (.sh) to register a sink connector to the cloud database.
- __development-compose__: Directory for storing the docker-compose.yml generation script and the generated file.
    - __configs__: Directory for storing configuration files that need manual updates and will be mounted to the Docker container.
        - device-config.json: Mapping file mounted to the device controller, which uses it to determine the URL for updating the device with a specific ID.
        - sensor-to-device.json: Mapping file mounted to the Occupancy Detector module, allowing it to adjust the temperature on the correct device when the sensor with a specific ID detects no occupancy.
    - __template/docker-compose-room-template.yml__: Docker Compose template used to generate docker-compose.[HOTEL_NO]-[FLOOR_NO]-[ROOM_NO].yml files.
    - __generate-room-compose-file.sh__: Shell script (.sh) used to generate docker-compose.[HOTEL_NO]-[FLOOR_NO]-[ROOM_NO].yml files. It will prompt for the required parameters and automatically generate the file.
- __run-development.sh__: Shell script (.sh) used to run all docker-compose files in the __development-compose/__ directory simultaneously.
- __stop-all-compose.sh__: Shell script (.sh) used to stop all running containers in docker-compose and remove associated volumes (which contain persistent data).

## Setting up for development environment

> **Note:** Pending changes to the CSV file. The shell script will generate all required files from the CSV.


1. Navigate to the development-compose directory.

```bash
cd development-compose
```

2. Generate a docker-compose file for each room.

```bash
generate-room-compose-file.sh
```

You will be prompted to ...
```bash
Enter Hotel Number: salonpasresort                   
Enter Floor Number: 3                   
Enter Room Number: 3001                    
Enter PostgreSQL User: xxxx                  
Enter PostgreSQL Password: xxxx             
Enter PostgreSQL Expose Port (54XX): 5432
Enter EMQX Expose Port (18XX): 1833
Enter LifeBeing Sensor Expose Port (8XXX): 8001
Enter LifeBeing Sensor Device ID (EX: LB-R101-1): LB-salonpasresort-3001
Enter IAQ Sensor Expose Port (80XX): 8002
Enter IAQ Sensor Device ID (EX: IQA-R101-1): IAQ-salonplasresort-3001
Enter IAQ Device Expose Port (80XX): 8003
```

3. Update the configs/device-config.json file with ` "[IAQ SENSOR DEVICE ID]": "http://[ROOM_NO]-iaqdevice:8000/api"`.
```json
{
    "IAQ-salonplasresort-3001": "http://3001-iaqdevice:8000/api"
}
```

4. Update the configs/sensor-to-device.json file with ` "[LIFEBEING SENSOR DEVICE ID]": "[IAQ SENSOR DEVICE ID]"`.
```json
{
    "LB-salonplasresort-3001": "IAQ-salonplasresort-3001"
}
```

5. Repeat steps 2-4 until all rooms are created.

6. Navigate back to the root directory.
```bash
cd ..
```

7. Start Docker Compose.
```bash
run-development.sh
```
