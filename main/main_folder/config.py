'''
Cole Johnson 11/20/23

a method to store variables used in the main folder in one place.

do not change any variables below unless you know what you are doing.
'''

#           input pings

# gps serial
# this will affect what rx tx pins on the board will be used to get inputs from the gps sensor
pin_gps_serial = 1

# accel pins
# these are the pins comming in from the acceleration sensor
pin_accel_x = 26
pin_accel_y = 27
pin_accel_z = 28

#           output pins

# motor pins

# the motor controller has 4 pin, they go from i1 to i4 and are used to control the voltage
# send to each of the 2 motors. i1 and i2 control motor 1, and i3 and i4 control motor 2.
# i1
pin_m_i1 = 21
# i2
pin_m_i2 = 20
# i3
pin_m_i3 = 19
# i4
pin_m_i4 = 18

# led pins

# fix led
# flashes when the gps has a good signal / fix
pin_led_fix = 15
# active led
# lights up when the robot is ready to move and flashes when its moving
pin_led_ready_to_path = 14
# pause for gps led
# lights up when the user is trying to append data to the gpd via the button on the back.
# when it lights up the user should stop moving the robot to allow the gps to focus on its current position
pin_led_pause_for_gps = 13
# main called / on led
# led is turned on when the main_controller is properly called
# useful for debugging
pin_led_main_called = "LED"

# other pins

# outputs a high voltage (3.3v+) when the robot is path finding
# this should be used to detect when the tick collecting meausred should be run
pin_robot_is_pathing = 0

# button pins

# start button
# used to start the robots path finding, exit the robots pathfinding, or exit its gpd append mode
pin_btn_start = 10
btn_start_high = 0

# store gps data button
# used to enter append mode where data can be written to the txt file
pin_btn_store_gps_data = 11
btn_store_high = 0

#           constants
'''
Note that not all of these can be changed

if you are using the methods for a different project, sure, but these are what are needed for this probject.
constants marked with '^ can change ^' can be changed, those without shouldn't unless you know what you are doing.
'''

# motor max and min voltage inputs
v_in_min = 0
v_in_max = 5
# motor max and min duty outputs 
d_out_min = 0
d_out_max = 65535

# file name of the txt file containing the gps points for the gpd
file_name = "_path.txt"
'''^ can change but shouldn't unless the gpd data is under a different name ^'''

# pid contants
# k const used for tunning the pid
pid_kp = 1000
'''^ can change ^'''
pid_ki = 5.0
'''^ can change ^'''
pid_kd = 0.0001
'''^ can change ^'''
# the range that the error needs to be within to be considered complete
pid_range = 0.00013
'''^ can change ^'''
# the min and max pid output based off its returned value
# pid error used to tune the min max of the output
pid_error_in_min = -0.5
'''^ can change ^'''
pid_error_in_max = 0.5
'''^ can change ^'''
# -5 to 5 is what the motor controller can take
pid_volt_out_min = -5.0
pid_volt_out_max = 5.0
# the error in the system is the distance +- (turn * multi)
# this affects how much the turn error affects the overal error
pid_turn_multi = 0.005#0.000001
'''^ can change ^'''

# pitch roll max
pitch_max = 65
roll_max = 55

# delays
# delay to allow the gps to focus
delay_gps_focus_time = 0.500
# long delay, should be about double the short delay
delay_standard_long = 0.80
# short delay, used to update gps sensor
delay_standard_short = 0.40
# time that the led will blink before starting path finding
delay_blink_time = 0.200
# times the led will blink
delay_blink_amount = 25
# multiply delay_blink_time by delay_blink_amount
'''^ can change but make sure you know what you are doing before you do ^'''