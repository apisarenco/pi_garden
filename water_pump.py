import time

from gpiozero import OutputDevice

class Pump:
    def __init__(self, pin):
        self.pump = OutputDevice(pin)

    def __edit__(self):
        self.pump.close()
    
    def self_test(self):
        for i in range(0, 10):
            self.pump.on()
            time.sleep(0.1)
            self.pump.off()
            time.sleep(0.1)

    def on(self):
        self.pump.on()

    def off(self):
        self.pump.off()
