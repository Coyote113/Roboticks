'''
Cole Johnson 11/29/23

framework function used in the libr and main_f folder methods.

these are functions that are needed throughtout the program so they are stored in one place.
'''

import math

# interval mapping function
# returns the passed x to a mapped value based off in_min in_max and graph mapped to out_min out_max
def interval_mapping(x, in_min, in_max, out_min, out_max):
    if x < in_min: return out_min # x is below in_min
    elif x > in_max: return out_max # x is above in_max
    else: # x is between in_min and in_max
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


# returns the charge of the passed value
# returns 1 if its positive and -1 if its negative
def charge(x):
    if x > 0: return 1
    elif x < 0: return -1
    else: return 0


# gets the number of degrees between 2 degrees on a degree unit circle
# takes in the two points as degrees from 0, and returns a degree arc
# this can cross between 360 and 0
def degree_arc_calc(current, target): # the matthew calculation
    E1=target-current
    E2=-1*(current-(target-360)) 
    E3=target-(current-360) 
    Efinal = 0
    if (math.fabs(E1) < math.fabs(E2) and math.fabs(E1) < math.fabs(E3)):
      Efinal = E1
    if (math.fabs(E2) < math.fabs(E1) and math.fabs(E2) < math.fabs(E3)):
      Efinal = E2 
    if (math.fabs(E3) < math.fabs(E1) and math.fabs(E3) < math.fabs(E2)):
      Efinal = E3
    return Efinal


# gets the distance between 2 points using pythag theorem
# takes 2 points as tupples and returns a float
def distance(location_start, location_go):
    # gets distance with pythag theorem
    d = math.sqrt((location_go[0]-location_start[0])**2 + (location_go[1]-location_start[1])**2)
    return d


# gets the angle between two points
# cannot do transformations between the different polar types
def get_raw_angle(origin, point, round_to_dec = 1):
    dx = point[0] - origin[0] # gets the distance between the 2 points in x and y directions
    dy = point[1] - origin[1]
    angle_rad = math.atan2(dy, dx)
    angle_deg = math.degrees(angle_rad)
    if angle_deg < 0: # if the output should be in quad 3 or 4 and not 1 or 2
        angle_deg += 360
    angle_deg = round(angle_deg, round_to_dec) # rounds the value to an amount
    return angle_deg


# creates a tuple containing 2 parallel arrays
# the arrays are maps of how the different polar coordinate types relate to each other'
def get_parallel_deg_format_tuple():
    deg_normal = []
    deg_gps = []
    for x in range(0, 360, 1):
        deg_normal.append(x)
    for x in range(90, -1, -1):
        deg_gps.append(x)
    for x in range(359, 90, -1):
        deg_gps.append(x)
    return (deg_normal, deg_gps)

# creates a dict of the polar coordinate differences
# the dict is then used to get angles from normal to gps format to some resolution
def get_dict_of_polar_degrees(normal_gps_tuple):
    #get_dict_of_normal_to_gps_polor was prev name
    dictt = {}
    deg_normal = normal_gps_tuple[0]
    deg_gps = normal_gps_tuple[1]
    for x in range(len(deg_normal)): 
        ''' changed from np.arange to range'''
        dictt[str(deg_gps[x])] = deg_normal[x]
    return dictt


# converts and angle using the dict and returns it
# used to convert angles from normal polar coordinates to gps polar format
# returns a decimal float
def angle_from_dict(angle, dictt, round_to_dec = 0):
    if angle == 360:
        angle = 0
    if round_to_dec == 0:
        return dictt[str((int(angle)))]
    return dictt[str(angle)]


# checks if an angle is greater than a base / reference angle
# this can cross over 0/360
# returns true if it is and false if not
# note that this is with gps polar format, degrees start at 0 and go clockwise
def is_angle_greater_than_base(base, angle):
    x = degree_arc_calc(base, angle)
    x = charge(x)
    if x == 1:
        return True
    return False
# attempt swap true and false
#        return True
#    return False


# gets an approximation for the error in the system
# approx_error is distance +- (degrees off * multiplier)
# returns a tuple as there is different error for each of the 2 motors depending on the turn angle
# tuple format (m1 error, m2 error)
def approx_error(robot_pos, robot_angle, desired_pos, degree_dict, turn_multi = 1.0):

    m1e = distance(robot_pos, desired_pos) # error for motor 1 and 2 is at base the distance between the points
    m2e = distance(robot_pos, desired_pos)

    # gets the line angle in gps polar format
    line_angle = angle_from_dict(get_raw_angle(robot_pos, desired_pos, 1), degree_dict)
    arc = math.fabs(degree_arc_calc(line_angle, robot_angle) * turn_multi)
    #print('arc ' + str(arc) + ' angle ' + str(degree_arc_calc(line_angle, robot_angle)))
    arc1 = 0
    arc2 = 0
    if line_angle == robot_angle:
        #print("zero")
        pass
    elif is_angle_greater_than_base(line_angle, robot_angle): # line_angle > robot_angle
        #print("greater arc")
        arc1 = -1*arc
        arc2 = arc
    else: # line_angle < robot_angle
        #print("less arc")
        arc1 = arc
        arc2 = -1*arc
    print('arc1 ' + str(arc1) + ' arc2 ' + str(arc2))
    return (m1e, m2e, arc1,arc2)