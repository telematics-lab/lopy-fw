## Overview

Welcome to the Telematics Lab's LoRaWAN repository. This repository provides a comprehensive set of resources and examples for configuring and deploying a LoRaWAN network using LoPy/FiPy boards. The repository is organized into several folders, each serving a specific purpose in the network setup and data collection process.

## Repository Structure

### 1. gateway
This folder contains the necessary code and configurations to set up a single-channel LoRa gateway using a LoPy or FiPy board.

**Contents:**
- `main.py`: Main script to configure and run the LoRa gateway.
- `config.py`: Configuration file for setting up gateway parameters such as frequency, spreading factor, and server details.

### 2. node1
This folder provides example code for a LoRa node that sends light strength and pressure data. The data is retrieved using a PySense shield connected to a LoPy or FiPy board.

**Contents:**
- `main.py`: Script to read light strength and pressure data from the PySense shield and send it via LoRa.
- `config.py`: Configuration file for node parameters.

### 3. node2
This folder includes example code for a LoRa node that sends temperature and humidity data. The data is retrieved using a PySense shield connected to a LoPy or FiPy board.

**Contents:**
- `main.py`: Script to read temperature and humidity data from the PySense shield and send it via LoRa.
- `config.py`: Configuration file for node parameters.

### 4. node3
This folder contains example code for a LoRa node that sends GPS coordinates. The coordinates are retrieved using a PyTrack shield connected to a LoPy or FiPy board.

**Contents:**
- `main.py`: Script to read GPS coordinates from the PyTrack shield and send it via LoRa.
- `config.py`: Configuration file for node parameters.

### 5. decoder
This folder includes JavaScript examples of decoding functions to be used in The Things Network (TTN) for decoding the payload received from the LoRa nodes.

### 6. Colab MQTT Examples
This folder contains iPython Notebook examples that demonstrate how to retrieve data from The Things Network (TTN) using MQTT.

## Getting Started

### Prerequisites
- LoPy/FiPy board(s)
- PySense or PyTrack shield(s)
- The Things Network Console account
- Python environment for running iPython Notebooks

### Setting Up the Gateway/Nodes
1. Clone this repository to your local machine.
2. Open the board file system.
3. Copy gateway or nodes files inside.

## Contributing

We welcome contributions from the community. If you have any suggestions, bug reports, or feature requests, please create an issue or submit a pull request.