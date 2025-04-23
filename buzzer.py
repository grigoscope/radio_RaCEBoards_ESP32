import time, pwmio, board

class Buzzer:
    """Class to control a buzzer."""
    def __init__(self, pin=board.IO4, freq=1000):
        # Initialize the PWM output for the buzzer with the specified pin and frequency
        self.pwm = pwmio.PWMOut(pin, duty_cycle=0, frequency=freq, variable_frequency=True)
    
    def beep(self, duration=0.5, duty=32000):
        # Activate the buzzer with the specified duty cycle and duration
        self.pwm.duty_cycle = duty
        time.sleep(duration)
        # Turn off the buzzer
        self.pwm.duty_cycle = 0
