Cole Johnson 11/20/23

the main folder has 2 main file inside it.

the first is the config file. this file holds all of the variables used in the other main file in order
to have all of them in one place so that they can be easily changed.

the other file is the main_controller. this is the actual main file and the most complex file in the progam.
DO NOT mess with the program unless you know what you are doing as you could cause issues if you change anything.

the main_controller has 3 functions inside it. the main thread function handles the actual movement of the robot.
it runs the current gps values against the desired gpd values in a pid and gets a voltage value that it then
sends to the motor controller to move the robot.

the second function, seco thread, uses the gps sensor and method to get the robots current data.

the third function is the run function, which simply starts both of the other 2 function.