import utime as ut

def test_ACCEL():
    from libr.ACCELERATION_SENSOR import create_ACCELERATION_SENSOR
    # pass the x, y, and z ADC pins
    accel = create_ACCELERATION_SENSOR(26, 27, 28)
    while True:
        # gets a tuple containing the pitch and roll values
        accel_tup = accel.get_tilt_tuple_pitch_roll()
        print('pitch: ' + str(accel_tup[0]) + ' roll: ' + str(accel_tup[1]))
        ut.sleep(1)

def test_getting_system_error():
    import libr.framework as fw
    # robots current gps point
    robotPoint = (0,0)
    # robots current angle in gps polar / gps format
    robotAngle = 0
    # desired point to travel to as a gps point
    desiredPoint = (0,0)
    # amount of the turn error used when calculating the error, can be tuned
    turn_multi = .01
    # creates a dict object of gps vs normal polar theta values
    dictt = fw.get_dict_of_polar_degrees(fw.get_parallel_deg_format_tuple())
    # gets the error in the system
    error = fw.approx_error(robotPoint, robotAngle, desiredPoint, dictt, turn_multi)
    # returns a 4 part tuple with the first 2 being the distance error for motor 1 and 2
    # and the second 2 being the turn error for motor 1 and 2
    print('error in system: ' + str(error))

def test_in_pin():
    from libr.IN_PIN import create_IN_PIN
    # pass the pin that the input pin is to be connected to
    in_pin = create_IN_PIN(0)
    while True:
        # returns true when its in its high state
        print('is pressed: ' + str(in_pin.is_high()))
        ut.sleep(1)

def test_out_pin():
    from libr.OUT_PIN import create_OUT_PIN
    # pass the pin that the output pin is to be connected to
    out_pin = create_OUT_PIN(1)
    while True:
        # toggles the value of the output pin every second
        out_pin.toggle()
        ut.sleep(1)

def test_motor_controller():
    from libr.MOTOR_CONTROLLER import create_MOTOR_CONTROLLER
    # pass the motor controller pins in format (i1, i2, i3, i4)
    motor = create_MOTOR_CONTROLLER(0, 1, 2, 3)
    # moves the 2 motors in many ways for testing
    motor.move(5)
    ut.sleep(1)
    motor.move(-5)
    ut.sleep(1)
    motor.move(2.5)
    ut.sleep(1)
    motor.turn(5)
    ut.sleep(1)
    motor.move(-5)
    ut.sleep(1)
    motor.move_ungrouped(5, 0)
    ut.sleep(1)
    motor.move_ungrouped(0, 5)
    ut.sleep(1)
    motor.move_ungrouped(1, 3)
    ut.sleep(1)
    motor.stop()

def test_GPD():
    from libr.GPD import create_GPD
    # the file name for the path file (txt file)
    path_file_name = "_path.txt"
    gpd = create_GPD(path_file_name, True)
    # prints the array of points within the text file
    print('full gpd array ' + str(gpd.get_full_gpd_arr()))

def test_GPS():
    from libr.GPS import create_GPS
    gps = create_GPS(1)
    while True: # connects to sats
        if gps.lon != None and gps.lat() != None and gps.angle() != None:
            break # gps has fix
        ut.sleep(1)
    while True: # gps can now output needed data
        # prints the current gps point read by the gps sensor
        print('gps point: ' + str(gps.actual_location_tuple()))
        ut.sleep(1)