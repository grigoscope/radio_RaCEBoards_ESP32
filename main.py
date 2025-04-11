import time
import board
import busio
import digitalio
import pwmio
import ipaddress

from lib import Ra01S

import wifi
import socketpool
import json
from adafruit_httpserver import Server, Request, Response, Websocket, GET
from asyncio import gather, run, sleep as async_sleep

# Buzzer frequency
frequency_buzzer = 1000

# Buzzer pin setup
buzzer_pin = board.IO4
buzzer = pwmio.PWMOut(
    pin=buzzer_pin, duty_cycle=0, frequency=frequency_buzzer, variable_frequency=True
)

# Radio channel (1 to 6)
CHANNEL = 1

# Load HTML template for the web interface
with open("radio_recieve.html") as f:
    HTML_TEMPLATE = f.read()

# Setup Radio
SDCard_cs_pin = board.IO15
SDCard_cs = digitalio.DigitalInOut(SDCard_cs_pin)
SDCard_cs.direction = digitalio.Direction.OUTPUT
SDCard_cs.value = True

# SPI module setup
spi0_speed = 2000000
spi0_module = busio.SPI(clock=board.IO12, MOSI=board.IO11, MISO=board.IO13)

# Radio module pins
Ra01S_cs_pin = board.IO7
Ra01S_nRst_pin = board.IO6
Ra01S_nInt_pin = board.IO5

# Initialize Ra01S radio module
Ra01S = Ra01S.Ra01S_SPI(
    spi0_module, Ra01S_cs_pin, Ra01S_nRst_pin, Ra01S_nInt_pin, spi0_speed
)
Ra01S.on()
Ra01S.SetMaxPower()
Ra01S.SetChannel(CHANNEL)

# Initial delays for GNSS and magnetometer setup
time.sleep(1)
time.sleep(1)

# Button setup
button = digitalio.DigitalInOut(board.IO9)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP

# WiFi credentials
ssid = "WiFi-name"
password = "1234567890"

# Server configuration
HOST = ""
PORT = 5000

# Connect to WiFi
wifi.radio.connect(ssid, password)
pool = socketpool.SocketPool(wifi.radio)
print("Self IP", wifi.radio.ipv4_address, "Self PORT", PORT)

HOST = str(wifi.radio.ipv4_address)
server_ipv4 = ipaddress.ip_address(pool.getaddrinfo(HOST, PORT)[0][4][0])
s = pool.socket(pool.AF_INET, pool.SOCK_DGRAM)
s.settimeout(None)
s.bind((HOST, PORT))

buf = bytearray(100)
print(f"Created UDP Server socket {server_ipv4}:{PORT}")

buzzer.duty_cycle = 32000
time.sleep(0.5)
buzzer.duty_cycle = 0

# HTTP server setup
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, debug=True, address_="/client")

websocket: Websocket = None


@server.route("/client", GET)
def client(request: Request):
    """Serve the HTML template to the client."""
    return Response(request, HTML_TEMPLATE, content_type="text/html; charset=utf-8")


@server.route("/connect-websocket", GET)
def connect_client(request: Request):
    """Handle WebSocket connection."""
    global websocket  # pylint: disable=global-statement

    if websocket is not None:
        websocket.close()  # Close any existing connection

    websocket = Websocket(request, buffer_size=16384 * 2)
    return websocket


server.start(str(wifi.radio.ipv4_address))


async def handle_http_requests():
    """Handle incoming HTTP requests."""
    while True:
        server.poll()
        await async_sleep(0)


async def send_websocket_messages():
    """Send messages over WebSocket."""
    rec_string = ""
    global CHANNEL

    while True:
        if websocket is not None:
            # Handle button press to change channel
            if button.value == 0:
                CHANNEL += 1
                if CHANNEL == 7:
                    CHANNEL = 1
                print(f"Channel: {CHANNEL}")
                Ra01S.SetChannel(CHANNEL)
                time.sleep(1)

            # Handle incoming radio messages
            if Ra01S.AvailablePacket():
                rec_string = Ra01S.ReciveS()
                print(f"Received message: {rec_string}")
                seq_ = rec_string.split(":")
                try:
                    if rec_string != "wait":
                        seq_ = [
                            float(x) if i > 0 else x for i, x in enumerate(seq_)
                        ]  # Convert numeric parts to float
                        data_dict = {
                            "ch": f"{CHANNEL}",
                            "id_": seq_[0],
                            "t_fly": round(seq_[1], 2),
                            "temp": round(seq_[2], 2),
                            "press": round(seq_[3], 2),
                            "alt": round(seq_[4], 2),
                            "ax": round(seq_[5], 2),
                            "ay": round(seq_[6], 2),
                            "az": round(seq_[7], 2),
                            "lon": round(seq_[8], 2),
                            "lat": round(seq_[9], 2),
                            "flag_start": round(seq_[10], 2),
                            "flag_apoge": round(seq_[11], 2),
                            "flag_land": round(seq_[12], 2),
                            "user_data": list(map(lambda x: round(x, 2), seq_[13:])),
                        }

                        # Convert to JSON
                        data = json.dumps(data_dict)

                        # Send via WebSocket
                        websocket.send_message(data, fail_silently=True)
                except Exception as e:
                    print(f"Error processing message: {e}")
        await async_sleep(0.01)


async def main():
    """Main asynchronous function."""
    await gather(
        handle_http_requests(),
        send_websocket_messages(),
    )


run(main())