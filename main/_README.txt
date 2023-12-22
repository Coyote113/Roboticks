This is the main program for the fall 2023 robotics ENGR 151 team.

Code authors: Cole Johnson, 

Date: 11/20/23

If you want to change the path of the robot, use the file _path.txt, read the _manual.txt file for more information
about how to use the robot.



Our goal was to design the control system for a gps guided robot which could later be used to help
automate the collection of ticks.

This is a very complex code file, but we have done our best to document everything inside it.

Our main goal for this project was for it to be modular

This program has 1 py library in the lib folder

This program also has multiple methods in the libr folder created to simplify parts of the main_controller code.

For the team after us, we wanted it to be easy for you guys to add onto this project.

there is an out pin which will send a voltage of 3.3v+ when the robot is currently moving through its path.
when you add another pico, have that pico look for a current from our picos GPIO 0 pin (this can be changed in config)
as it will only send that high voltage signal when the robot is going along its path.