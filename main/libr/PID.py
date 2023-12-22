'''
Cole Johnson 11/3/2023

a method / class for simple PID calculations
'''

import math as m

class create_PID:
    def __init__(self): # initialize, called on creation of the class object
        # sets all k constants, error values, and desired / range to 0 or None
        self.kp = None
        self.ki = None
        self.kd = None

        self.error = None
        self.preverror = 0
        self.totalerror = 0
        self.derivative = 0

        self.desired = None
        self.range = 0.01


    # function to get or set the constants
    def get_kp(self): # get and set kp
        return self.kp
    def set_kp(self, kp):
        self.kp = kp

    def get_ki(self): # get and set ki
        return self.ki
    def set_ki(self, ki):
        self.ki = ki

    def get_kd(self): # get and set kd
        return self.kd
    def set_kd(self, kd):
        self.kd = kd

    def get_kpid(self): # get and set p i and d using a tuple
        return (self.kp, self.ki, self.kd)
    def set_kpid(self, ktuple):
        self.kp = ktuple[0]
        self.ki = ktuple[1]
        self.kd = ktuple[2]


    def get_goal(self): # get and set the desired value
        return self.desired
    def set_goal(self, desired):
        self.desired = desired

    def get_range(self): # get and set the error range
        return self.range
    def set_range(self, range): 
        self.range = range


    def config_complete(self): # checks if any of the needed values are equal to None
        arr = [self.kp, self.ki, self.kd,  
               self.desired, self.range]
        for x in arr:
            if x == None:
                return False
        return True


    def calculate(self, current): # calc and return the PID based off the current value passed
        self.error = current - self.desired
        self.derivative = self.error - self.preverror
        self.totalerror += self.error
        self.preverror = self.error

        return (self.error * self.kp + self.totalerror * self.ki + self.derivative * self.kd)
    

    def error_in_range(self): # returns a bool on the condition that the error is within the error range
        if m.fabs(self.preverror) < self.range: # checks if the error is within the range
            return True
        else: return False

    def calculate_by_error(self, error):
        self.error = error
        self.derivative = self.error - self.preverror
        self.totalerror += self.error
        self.preverror = self.error

        return (self.error * self.kp + self.totalerror * self.ki + self.derivative * self.kd)
    
    # resets the error values in the pid
    def reset(self):
        self.preverror = 0
        self.derivative = 0
        self.totalerror = 0