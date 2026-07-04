# Game Server Scanner

A multi-threaded Python script designed to scan IP ranges and specific ports for running game servers using the A2S protocol. The script matches server metadata against targeted keywords to locate specific game servers efficiently.

## Features

* Multi-threaded architecture utilizing ThreadPoolExecutor for high performance.
* Support for complete subnet scanning via CIDR notation notation.
* Automated server query handling via the A2S protocol.
* Configurable target name matching, timeouts, and worker limits.

## Prerequisites

Before running the scanner, ensure you have Python 3.x installed along with the required libraries.

Install the necessary dependencies using pip:

```bash
pip install python-a2s
```

## Configuration

Open the script file to customize your scan parameters:

* **TARGET_SERVER_NAMES**: A list of string keywords used to filter server names (e.g., `['CS2']`). The search is case-insensitive.
* **TIMEOUT**: The maximum time in seconds to wait for a response from each individual port.
* **MAX_WORKERS**: The number of concurrent threads to spawn for scanning.
* **ip_range**: The target subnet block specified in CIDR format (e.g., `192.168.1.0/24`).
* **ports**: A list of UDP destination ports known for hosting the targeted game servers.

## Usage

Execute the script directly from your terminal or command prompt:

```bash
python main.py
```

## How It Works

1. **Network Parsing**: The script converts the provided CIDR block into a list of individual host IP addresses.
2. **Task Distribution**: A matrix of every combination of IP address and port is generated and fed into the thread pool.
3. **A2S Queries**: Each thread attempts to establish communication with the target endpoint using the Source Engine A2S_INFO protocol query.
4. **Filtering and Reporting**: If a server responds, its name is inspected against your keywords. Matching instances are instantly logged to the console output.

## License

This project is open-source and available under the MIT License.
