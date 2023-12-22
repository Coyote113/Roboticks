'''
Cole Johnson 11/20/23

a method / class used for controlling acceleration sensors

the functions in the class can get you the pitch and roll of the acceleration sensor, and the acceleration of the
sensor in the x, y, z directions
'''

import machine
import math

class create_ACCELERATION_SENSOR:
    def __init__(self, pin_adc_x, pin_adc_y, pin_adc_z):
        # defines pins
        self.pin_adc_x = pin_adc_x
        self.pin_adc_y = pin_adc_y
        self.pin_adc_z = pin_adc_z
        # defines the adc inputs
        self.adc_x = machine.ADC(machine.Pin(self.pin_adc_x))
        self.adc_y = machine.ADC(machine.Pin(self.pin_adc_y))
        self.adc_z = machine.ADC(machine.Pin(self.pin_adc_z))

    # returns a tuple with the pitch and roll degrees
    def get_tilt_tuple_pitch_roll(self):
        x = read_acceleration(self.adc_x)
        y = read_acceleration(self.adc_y)
        z = read_acceleration(self.adc_z)
        # Calculate the tilt angles
        pitch, roll = calculate_tilt_angles(x, y, z)
        return (pitch, roll)

    # returns a tuple with the pitch and roll absolute value in degrees
    def get_tilt_tuple_pitch_roll_fabs(self):
        x = read_acceleration(self.adc_x)
        y = read_acceleration(self.adc_y)
        z = read_acceleration(self.adc_z)
        # Calculate the tilt angles
        pitch, roll = calculate_tilt_angles(x, y, z)
        pitch = math.fabs(pitch)
        roll = math.fabs(roll)
        return (pitch, roll)
    

    # returns a tuple with the x, y, z accelerations
    def get_accel_tuple_xyz(self):
        x = read_acceleration(self.adc_x)
        y = read_acceleration(self.adc_y)
        z = read_acceleration(self.adc_z)
        return (x, y, z)

# method function to read the adc to acceleration
def read_acceleration(adc):
    # Read the ADC value and convert it to voltage
    voltage = adc.read_u16() * 3.3 / 65535
    # Convert the voltage to acceleration (assuming 3.3V supply)
    acceleration = (voltage - 1.65) / 0.330
    return acceleration

# method function to get tilt from adc acceleration values
def calculate_tilt_angles(x, y, z):
    pitch = math.atan2(y, math.sqrt(x**2 + z**2))
    roll = math.atan2(x, math.sqrt(y**2 + z**2))
    # Convert the angles to degrees
    pitch = math.degrees(pitch)
    roll = math.degrees(roll)
    return pitch, roll