# Radio RaCEBoards ESP32

Project based on *[RaCEBoards-ESP32](https://github.com/innopoltech/RaCEBoards-ESP32/tree/main)*

---

This project implements a receiving station for telemetry data using the Ra01S LoRa module and an ESP32-S3 microcontroller. The station receives telemetry data from experimental fly models, processes it, and displays it on a web interface with real-time updates.

![](interface.png)

## Features

- **LoRa Communication**: Uses the Ra01S LoRa module for receiving telemetry data.
- **Web Interface**: Displays telemetry data in real-time using a responsive web interface.
- **Data Visualization**: Includes charts for altitude and acceleration over time.
- **Map Integration**: Displays the location of the telemetry source on a map using Leaflet.
- **Channel Switching**: Allows switching between different radio channels (1 to 6).
- **Data Logging**: Logs received data and allows downloading it as a text file.

## Project Structure

```
├── main.py                # Main application script
├── config.py              # WiFi and pin settings
├── buzzer.py              # Buzzer control module
├── channel_switcher.py    # Button handler for channel switching
├── radio_module.py        # Ra01S driver module
├── web_interface.py       # HTTP server and endpoint logic
├── radio_receive.html     # Web UI template
└── lib/                   # Support libraries and drivers
   ├── adafruit_httpserver/ # Library for handling HTTP server functionality
   ├── adafruit_register/   # Library for low-level register manipulation
   ├── asyncio              # Library for asynchronous programming
   ├── BUZZER               # Module for controlling the buzzer
   ├── LLCC68               # Driver for the LLCC68 LoRa module
   ├── I2C_SPI_protocol_Base.py # Driver for I2C-based modules
   └── Ra01S                # Driver for the Ra01S LoRa module
```

## Requirements

- **Hardware**:
  - ESP32-S3 microcontroller
  - Ra01S LoRa module
  - Buzzer (optional)
  - Button for channel switching
- **Software**:
  - CircuitPython
  - Required libraries (e.g., `adafruit_httpserver`, `asyncio`, etc.)

## Setup

1. **Hardware Connections**:
   - Connect the Ra01S module to the ESP32-S3 using SPI pins.
   - Connect a button to the designated GPIO pin for channel switching.
   - Optionally, connect a buzzer to the specified GPIO pin.

2. **Install Dependencies**:
   - Copy the required libraries to the `lib/` folder on the ESP32-S3.

3. **Configure WiFi**:
   - Update the `ssid` and `password` variables in `main.py` with your WiFi credentials.

4. **Run the Project**:
   - Upload the project files to the ESP32.
   - Run `main.py` to start the receiving station.

## Usage

1. **Access the Web Interface**:
   - Connect to the same WiFi network as the ESP32-S3.
   - Open a browser and navigate to the ESP32-S3's IP address.

2. **View Telemetry Data**:
   - The web interface displays real-time telemetry data, including parameters like altitude, temperature, and acceleration.

3. **Switch Channels**:
   - Press the button to switch between radio channels (1 to 6).

4. **Download Logs**:
   - Use the "Download log" button on the web interface to save received data as a text file.

## Web Interface

The web interface includes the following sections:

- **Parameters**: Displays telemetry data such as altitude, temperature, and acceleration.
- **Charts**: Visualizes altitude and acceleration over time using Chart.js.
- **Map**: Shows the location of the telemetry source on a map using Leaflet.
- **Indicators**: Displays flags for start, apogee, and landing events.

## Radio Data Format

Received telemetry messages follow a colon-separated format:

```
id:time:temp:press:alt:ax:ay:az:lon:lat:start:deploy:land:other_user_data
```

- **id** — unique identifier.
- **time** — flight time in seconds (since start).
- **temp** — temperature, °C.
- **press** — atmospheric pressure, kPa.
- **alt** — altitude in meters (since start).
- **ax, ay, az** — acceleration projections on X, Y, Z axes in m/s².
- **lon, lat** — longitude and latitude in degrees.
- **start** — start flag (1 when launch detected).
- **deploy** — deployment flag (e.g., release of payload).
- **land** — landing flag (1 when landing detected).
- **other_user_data** — any additional data fields, separated by colons.

## Acknowledgments

- [Adafruit](https://www.adafruit.com/) for providing CircuitPython libraries.
- [Leaflet](https://leafletjs.com/) for map integration.
- [Chart.js](https://www.chartjs.org/) for data visualization.
- [Innopoltech](https://github.com/innopoltech) and [vano7209](https://github.com/vano7209) for providing the RaCEBoards electronic kit and libraries.
