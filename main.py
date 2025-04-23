import time, json
from asyncio import gather, run, sleep as async_sleep
from config import *
from buzzer import Buzzer
from channel_switcher import ChannelSwitcher
from radio_module import RadioModule
from web_interface import WebInterface

class TelemetryApp:
    def __init__(self):
        # Initialize the buzzer with its pin and frequency
        self.buzzer    = Buzzer(BUZZER_PIN, BUZZER_FREQ)
        
        # Initialize the radio module with speed and starting channel
        self.radio     = RadioModule(LORA_SPEED, START_CHANNEL)
        
        # Initialize the channel switcher with button pin and radio instance
        self.switcher  = ChannelSwitcher(BUTTON_PIN, self.radio.radio)
        
        # Load the HTML content for the web interface
        html = open(HTML_PATH).read()
        
        # Initialize and start the web interface
        self.web       = WebInterface(SSID, PASSWORD, html, PORT)
        self.web.start()

    async def _http(self):
        # Handle HTTP requests in a loop
        while True:
            self.web.poll()
            await async_sleep(0)

    async def _telemetry(self):
        # Handle telemetry data in a loop
        while True:
            self.switcher.update()  # Update the channel switcher state
            
            # Check if a packet is available from the radio
            if self.radio.radio.AvailablePacket():
                raw = self.radio.radio.ReciveS()  # Receive the raw data
                print(f"Received message from {self.switcher.channel} channel: {raw}")
                
                # Parse the raw data and send it to the web interface
                data = self._parse(raw)
                self.web.send(data)
            
            await async_sleep(0.01)

    def _parse(self, msg: str) -> dict:
        try:
            # Parse the incoming telemetry message into a structured dictionary
            parts = msg.split(":")
            vals  = [float(x) if i > 0 else x for i, x in enumerate(parts)]
            return {
                "ch": str(self.switcher.channel),  # Current channel
                "id_": vals[0],                   # Identifier
                "t_fly": round(vals[1], 2),       # Flight time
                "temp": round(vals[2], 2),        # Temperature
                "press": round(vals[3], 2),       # Pressure
                "alt": round(vals[4], 2),         # Altitude
                "ax": round(vals[5], 2),          # Acceleration in X-axis
                "ay": round(vals[6], 2),          # Acceleration in Y-axis
                "az": round(vals[7], 2),          # Acceleration in Z-axis
                "lon": round(vals[8], 2),         # Longitude
                "lat": round(vals[9], 2),         # Latitude
                "flag_start": round(vals[10], 2), # Start flag
                "flag_apoge": round(vals[11], 2), # Apogee flag
                "flag_land": round(vals[12], 2),  # Landing flag
                "user_data": [round(x, 2) for x in vals[13:]]  # Additional user data
            }
        except (ValueError, IndexError) as e:
            print(f"Error parsing message: {msg}. Error: {e}")
            return {
                "ch": str(self.switcher.channel),
                "error": "Invalid data format"
            }

    def run(self):
        # Beep the buzzer to indicate the application is starting
        self.buzzer.beep()
        
        # Run the HTTP and telemetry tasks concurrently
        run(gather(self._http(), self._telemetry()))

if __name__ == "__main__":
    # Start the telemetry application
    TelemetryApp().run()
