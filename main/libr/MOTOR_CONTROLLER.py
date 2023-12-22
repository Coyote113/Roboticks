'''
Cole Johnson 11/11/23

motor controller class

a method / class used to control the motor controller using the 4 i pins.

the functions in the class can move or turn the 2 motors in a group, move both ungrouped from each other, and stop
both motors.
'''

import machine
import libr.framework as fw
import math as m

class create_MOTOR_CONTROLLER:
    def __init__(self, pin_m1_in1, pin_m1_in2, pin_m2_in3, pin_m2_in4, frq = 50,
                 v_in_min = 0, v_in_max = 5, d_out_min = 0, d_out_max = 65535):
        # pass 4 i pins
        # pin 1 and 2 are motor 1 and pin 3 and 4 are motor 2
        self.pin_m1_in1 = pin_m1_in1
        self.pin_m1_in2 = pin_m1_in2
        self.pin_m2_in3 = pin_m2_in3
        self.pin_m2_in4 = pin_m2_in4
        # defines the outputs
        self.out_m1_f = machine.PWM(machine.Pin(self.pin_m1_in1)) # voltage to move forward, 0-5 v
        self.out_m1_r = machine.PWM(machine.Pin(self.pin_m1_in2)) # reverse voltage, 0-5v
        self.out_m2_f = machine.PWM(machine.Pin(self.pin_m2_in3))
        self.out_m2_r = machine.PWM(machine.Pin(self.pin_m2_in4))
        # sets freq
        self.out_m1_f.freq(frq)
        self.out_m1_r.freq(frq)
        self.out_m2_f.freq(frq)
        self.out_m2_r.freq(frq)
        # sets in and out max
        self.v_in_min = v_in_min # min and max input voltages
        self.v_in_max = v_in_max
        self.d_out_min = d_out_min # min and max output duty cycle values
        self.d_out_max = d_out_max


    def move(self, v): # function to move in 1 direction
        # gets the duty mapped from 0-5 volts to 0-65536 duty cycle
        mapped_duty = int(fw.interval_mapping(m.fabs(v), self.v_in_min, self.v_in_max, self.d_out_min, self.d_out_max))
        # checks the direction
        charge = fw.charge(v)

        if charge == 1: # forward movement
            self.out_m1_f.duty_u16(mapped_duty)
            self.out_m2_f.duty_u16(mapped_duty)
        if charge == -1: # reverse movement
            self.out_m1_r.duty_u16(mapped_duty)
            self.out_m2_r.duty_u16(mapped_duty)


    def turn(self, v): # function to turn in 1 direction
        # gets the duty mapped from 0-5 volts to 0-65536 duty cycle
        mapped_duty = int(fw.interval_mapping(m.fabs(v), self.v_in_min, self.v_in_max, self.d_out_min, self.d_out_max))
        # checks the direction
        charge = fw.charge(v)

        if charge == 1: # move the motors different directions
            self.out_m1_f.duty_u16(mapped_duty)
            self.out_m2_r.duty_u16(mapped_duty)
        if charge == -1: # reverse of above
            self.out_m1_r.duty_u16(mapped_duty)
            self.out_m2_f.duty_u16(mapped_duty)


    def move_ungrouped(self, v1, v2): # function to move both motors independently
        # gets the duty mapped from 0-5 volts to 0-u16 duty cycle for both volts
        mapped_duty_1 = int(fw.interval_mapping(m.fabs(v1), self.v_in_min, self.v_in_max, self.d_out_min, self.d_out_max))
        mapped_duty_2 = int(fw.interval_mapping(m.fabs(v2), self.v_in_min, self.v_in_max, self.d_out_min, self.d_out_max))
        # gets the direction of both volts
        charge1 = fw.charge(v1)
        charge2 = fw.charge(v2)

        #print('duty 1 ' + str(mapped_duty_1))
        #print('duty 2 ' + str(mapped_duty_2))

        if charge1 == 1: self.out_m1_f.duty_u16(mapped_duty_1) # move motor 1
        elif charge1 == -1: self.out_m1_r.duty_u16(mapped_duty_1)

        if charge2 == 1: self.out_m2_f.duty_u16(mapped_duty_2) # move motor 2
        elif charge2 == -1: self.out_m2_r.duty_u16(mapped_duty_2)


    def stop(self): # sets all u16 to 0 which stops all movement
        self.out_m1_f.duty_u16(0)
        self.out_m1_r.duty_u16(0)
        self.out_m2_f.duty_u16(0)
        self.out_m2_r.duty_u16(0)