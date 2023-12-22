'''
Cole Johnson 11/20/23

a method / class for handling the boards out pins.

can only handle 1 bit outputs.

useful for leds or on off circuits.
'''

import machine

class create_OUT_PIN():
    def __init__(self, pin, v_high = 1):
        self.pin = pin # pin number
        self.out = machine.Pin(self.pin, machine.Pin.OUT) # actual pin object
        self.high = v_high # the high output
        self.low = 0 # the low output
        if v_high == 0:
            self.low = 1

    # sets the value of the out pin object
    def value(self, v):
        self.out.value(v)

    # toggles the value of the out pin object
    def toggle(self):
        self.out.toggle()

    # sets the value of the out pin object to its high value
    def on(self):
        self.out.value(self.high)

    # sets the value of the out pin object to its low value
    def off(self):
        self.out.value(self.low)

    # checks if the out pin object is sending its high output
    def is_on(self):
        if self.out.value() == self.high:
            return True
        else: return False

    # checks if the out pin object it sending its low output
    def is_off(self):
        if self.out.value() != self.high:
            return True
        else: return False

    # gets the pin objects pin number
    def get_pin_num(self):
        return self.pin
    
    # gets the raw out pins object
    def get_out_pin_obj_raw(self):
        return self.out