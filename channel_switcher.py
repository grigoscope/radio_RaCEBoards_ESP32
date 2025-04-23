from lib.Ra01S import Ra01S_SPI
import time, digitalio, board

class ChannelSwitcher:
    """Handles channel switching using a button."""
    def __init__(self, button_pin: board.Pin, radio: Ra01S_SPI):
        # Initialize the button with the specified pin
        self.button   = digitalio.DigitalInOut(button_pin)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull      = digitalio.Pull.UP
        
        # Initialize the radio and set the default channel
        self.radio    = radio
        self.channel  = 1

    def update(self):
        # Check if the button is pressed
        if not self.button.value:
            # Increment the channel and wrap around after 6
            self.channel = (self.channel % 6) + 1
            
            # Set the new channel on the radio
            self.radio.SetChannel(self.channel)
            
            # Print the current channel
            print(f"Channel switched to {self.channel}")
            
            # Add a delay to debounce the button
            time.sleep(1)
        
        # Return the current channel
        return self.channel
