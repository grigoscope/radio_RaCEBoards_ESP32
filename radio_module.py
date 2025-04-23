import busio, digitalio, board
from lib import Ra01S

class RadioModule:
    """Wraps LoRa Ra01S module operations."""
    def __init__(self, speed: int = 2_000_000, channel: int = 1):
        # SPI module setup
        spi = busio.SPI(
            clock=board.IO12,  # SPI clock pin
            MOSI=board.IO11,   # SPI MOSI (Master Out Slave In) pin
            MISO=board.IO13    # SPI MISO (Master In Slave Out) pin
        )
        # Use Pin objects directly, not DigitalInOut
        cs_pin = board.IO7    # Chip Select pin
        rst_pin = board.IO6   # Reset pin
        int_pin = board.IO5   # Interrupt pin
        # Initialize radio
        self.radio = Ra01S.Ra01S_SPI(
            spi, cs_pin, rst_pin, int_pin, speed
        )
        self.radio.on()  # Turn on the radio module
        self.radio.SetMaxPower()  # Set the radio to maximum power
        self.channel = channel  # Set the communication channel
        self.radio.SetChannel(self.channel)  # Apply the channel setting to the radio
