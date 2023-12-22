'''
Cole Johnson 11/11/23

gps class

a method / class used to read data from the gps sensor
'''
from machine import UART

import lib.adafruit_gps as adafruit_gps

class create_GPS:
    def __init__(self, serial, baud = 9600):
        self.serial = serial # sets the rx and tx using the serial
        self.baud = baud

        self.uart = UART(self.serial, baudrate=self.baud) # creates a uart object
        self.gps = adafruit_gps.GPS(self.uart) # creates a gps object from the uart
        self.gps.send_command('PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # sends command to get position and direction data

        self.stored_point = (None, None)


    # gets both the longitude and the latitude and returns it as a tuple
    def actual_location_tuple(self):
        return (self.gps.latitude, self.gps.longitude)

    # gets the longitude of the sensor
    def lon(self):
        return self.gps.longitude

    # gets the latitude of the sensor
    def lat(self):
        return self.gps.latitude

    # gets the number of sats the gps is connected to
    def satellites(self):
        return self.gps.satellites

    # gets about the angle of the gps sensor
    def angle(self):
        return self.gps.track_angle_deg

    # gets about the  speed of the gps sensor
    def speed(self):
        return self.gps.speed_knots


    # stores a point to the gps class    
    def store_point(self):
        self.stored_point = (self.gps.longitude, self.gps.latitude)

    # gets the stored point from the gps class
    def get_stored_point(self):
        return self.stored_point


    # sends an update to the sensor
    # returns a bool regarding if there is new information
    def update(self):
        return self.gps.update()
    

    # gets raw uart or gps objects
    def get_uart(self):
        return self.uart
    def get_gps(self):
        return self.gps