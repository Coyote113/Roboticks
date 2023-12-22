'''
Cole, Emily, Cody, Thomas, 12/5/23
'''

#               imports

# micropy board imports
import utime as ut
import _thread as _t
# variables from the config file
import main_folder.config as config
# framework functions
import libr.framework as fw
# methods / classes
from libr.GPD import create_GPD
from libr.GPS import create_GPS
from libr.ACCELERATION_SENSOR import create_ACCELERATION_SENSOR
from libr.MOTOR_CONTROLLER import create_MOTOR_CONTROLLER
from libr.IN_PIN import create_IN_PIN
from libr.OUT_PIN import create_OUT_PIN
from libr.PID import create_PID

#               class / object def

gpd = create_GPD(config.file_name)
gps = create_GPS(config.pin_gps_serial)
accel = create_ACCELERATION_SENSOR(config.pin_accel_x, config.pin_accel_y, config.pin_accel_z)
motor = create_MOTOR_CONTROLLER(config.pin_m_i1, config.pin_m_i2, config.pin_m_i3, config.pin_m_i4)
pid_m1 = create_PID()
pid_m2 = create_PID()

# turns on when the robot is ready to path
# blinks when the robot is pathing
led_ready_to_path = create_OUT_PIN(config.pin_led_ready_to_path)
# turns on when the robot has a gps fix
led_has_gps_fix = create_OUT_PIN(config.pin_led_fix)
# 
led_pause_for_gps = create_OUT_PIN(config.pin_led_pause_for_gps)
#
led_main_called = create_OUT_PIN(config.pin_led_main_called)

robot_pathing_out_pin = create_OUT_PIN(config.pin_robot_is_pathing)

btn_start_path = create_IN_PIN(config.pin_btn_start, config.btn_start_high)
btn_store_gps_data = create_IN_PIN(config.pin_btn_store_gps_data, config.btn_store_high)


# create dictinary for handling normal polar to gps polar conversion
# this will later be passed to select framework functions
dictt = fw.get_dict_of_polar_degrees(fw.get_parallel_deg_format_tuple())

# this is a large dict data type so it is created here so it does not have to be re calculated in other functions


#               functions def

# allows to user to write data to the text file by pressing a button on the robot
# when the button btn_store_gps_data is pressed it saves the current gps lon lat data to an array
# which is then saved to the gpd txt file.
# when the robots path is then run it will path the new points added with the btn_store_gps_data button
def run_append_gps_to_gpd():
    #print('called gpd append')
    point_arr = [] # creates empty array
    pressed_bool = True # create bool to check if user has stopped pressing the button

    led_main_called.off() # leds / output status
    led_ready_to_path.off()
    led_has_gps_fix.on()
    #print('starting loop')
    while True:
        if btn_start_path.is_high(): # user presses start path button to exit this loop
            #print('write array')
            #print('a ' + str(point_arr))
            gpd.write_arr_to_txt(point_arr) # write data to txt file
            gpd.read_txt_to_arr() # updates arr with info from txt file
            break # break loop
        
        # when the button is pressed
        if btn_store_gps_data.is_high() and pressed_bool == False:
            #print('appending to array')
            pressed_bool = True 
            # stops overflow / only allows one run of if statement before closing until user releases button
            led_pause_for_gps.on() # tells user to wait
            ut.sleep(config.delay_gps_focus_time) # wait for gps to focus
            led_pause_for_gps.off()
            point_arr.append(gps.actual_location_tuple()) # append current point to arr
            #print('appended ' + str(gps.actual_location_tuple()))

        # revert pressed value when its released
        if btn_store_gps_data.is_low():
            #print('unpress')
            pressed_bool = False
        ut.sleep(config.delay_standard_long)
    led_has_gps_fix.off()

# the main pathing control for the robot
# it draws a line between it and the current desired point and uses the pid to get the robot closer, and farther
# along the line in the current loop.
# this loops until the error in the system is within range (given in the config file) at which point it checks
# for a new point. if you is found it repeats, other wise it breaks the current loop.
# it will also break the current loop if a user clicks a button
def run_robot_pathing():
    #gps.store_point() # stores its current location
    gpd.read_txt_to_arr() # converts the txt file to an array
    ktup = (config.pid_kp, config.pid_ki, config.pid_kd) # sets up the pids
    pid_m1.set_kpid(ktup)
    pid_m1.set_range(config.pid_range)
    pid_m2.set_kpid(ktup)
    pid_m2.set_range(config.pid_range)
    
    led_main_called.off()

    frame = 0 # a variable to count each frame of the loop
    while True:
        frame += 1

        if btn_start_path.is_high() or btn_store_gps_data.is_high(): 
            #print('\n\nending via button exit\n\n\n\n')
            break # if either button is pressed stop the robots pathing

        # pitch and roll check
        if accel.get_tilt_tuple_pitch_roll()[0] >= config.pitch_max:
            motor.stop()
            #print('\n\nover max pitch\n\n')
        if accel.get_tilt_tuple_pitch_roll()[1] >= config.roll_max:
            motor.stop()
            #print('\n\nover max roll\n\n')

        # gets current and desired posistions
        robot_position = gps.actual_location_tuple()
        robot_angle = gps.angle()
        desired_position = gpd.get_current_point_in_arr_float()

        # gets the error in the system based off the current and desired positions
        approx_error = fw.approx_error(robot_position, robot_angle, desired_position, dictt, config.pid_turn_multi)
        # sends error to pids
        m1_pid_out = pid_m1.calculate_by_error(approx_error[0])
        m2_pid_out = pid_m2.calculate_by_error(approx_error[1])
        # maps output to voltage and sends voltage to motor controller

        v1=fw.interval_mapping(m1_pid_out , 
                                config.pid_error_in_min, config.pid_error_in_max, 
                                config.pid_volt_out_min, config.pid_volt_out_max)- approx_error[2]
        v2=fw.interval_mapping(m2_pid_out, 
                                config.pid_error_in_min, config.pid_error_in_max, 
                                config.pid_volt_out_min, config.pid_volt_out_max) - approx_error[3]
        motor.move_ungrouped(v2, v1)
        
        '''terminal'''
        #print('distance ' + str(fw.distance(robot_position, desired_position)) + ' robotA ' + str(robot_angle))
        #print('pre pid ' + str(approx_error))
        #print('pid out ' + str((m1_pid_out, m2_pid_out)))
        #print('pre v ' + str(v1) + ' ' + str(v2))
        #print('point ' + str(gpd.get_idx()) + ' tm' + str(config.pid_turn_multi))
        #print('\n')

        if fw.distance(robot_position, desired_position) < config.pid_range: # if either error is within range
            #print('\n\nabout to jump')
            if gpd.at_end_of_gpd_arr(): # if the robot is at the final point
                #print('ending\n\n\n\n')
                break # break current loop
            else:
                gpd.jump_idx() # jump to the next point in the gpd arr
                #print('jumped\n\n\n\n')


        if frame % 10 == 0: # waits 10 frames to equal 0
            led_ready_to_path.toggle() # toggle or flash light
            ut.sleep(config.delay_standard_long)
        else:
            ut.sleep(config.delay_standard_long)
        # both parts of the if else have a delay

#               main / thread def

# main thread for working with the pid, motors, and gpd.
# this is the method that is taking in information and moving the robot
def run_main_control_thread():
    while True: # connect to gps signal before starting loop
        #print('fixing')
        led_has_gps_fix.toggle()
        if gps.lon != None and gps.lat() != None and gps.angle() != None:
            #print('fix')
            break # gps giving needed data, break loop
        ut.sleep(config.delay_gps_focus_time)

    led_has_gps_fix.on() # turn on led / ouput status to user
    led_ready_to_path.on()

    pressed_start_bool = False

    while True: # loop for checking for user input and calling the required functions
        #print('main loop frame')
        if btn_store_gps_data.is_high():
            run_append_gps_to_gpd()
            pressed_start_bool = True

        if btn_start_path.is_high() and pressed_start_bool == False:

            for x in range(config.delay_blink_amount): # flashes leds before moving
                led_ready_to_path.toggle()
                ut.sleep(config.delay_blink_time)

            robot_pathing_out_pin.on()
            #print('about to start path finding')
            run_robot_pathing() # starts robots path finding
            motor.stop()
            #print('end of path finding function')
            robot_pathing_out_pin.off()

        if btn_start_path.is_low():
            pressed_start_bool = False
            led_ready_to_path.on()
        ut.sleep(config.delay_standard_long)

# second thread for working with the gps
# this is the for controlling the method that will be finding the current gps data as it needs waits
# it could be done in one thread but splitting it makes it simpler
def run_gps_update_thread():
    while True:
        gps.update()
        ut.sleep(config.delay_standard_short)

# main code function starts the gps update thread and turns on the main controller
# when this function is called, everything turns on
def run():
    led_main_called.on()
    _t.start_new_thread(run_gps_update_thread, ())
    run_main_control_thread()