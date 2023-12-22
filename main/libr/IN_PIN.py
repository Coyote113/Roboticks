'''
Cole Johnson 11/20/23

a method / class for handling the boards in pins.

can only handle 1 bit inputs

useful for buttons or switches or any high to low input.
'''

import machine

class create_IN_PIN():
    def __init__(self, pin, v_high = 1):
        self.pin = pin # pin number
        self.ini = machine.Pin(self.pin, machine.Pin.IN) # actual pin object
        self.v_high = v_high # the high voltage number, 1 by defualt but with a pull up circuit it would be 0
        
    # gets the current value of the in pin object
    def value(self):
        return self.ini.value()

    # checks if the in pin object is detecting its high voltage and returns True if so
    def is_high(self):
        if self.ini.value() == self.v_high:
            return True
        else: return False

    # checks if the in pin object is not detecting its hight voltage and returns False if so
    def is_low(self):
        if self.ini.value() != self.v_high:
            return True
        else: return False

    # gets the pin objects pin number
    def get_pin_num(self):
        return self.pin
    
    # gets the raw in pins object
    def get_in_pin_obj_raw(self):
        return self.ini