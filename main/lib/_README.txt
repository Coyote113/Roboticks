Cole Johnson 11/15/23

the adafruit_gps.py lib / method was not made by me. you may have to pip install it if you are having trouble 
(pip install adafruit_gps), but overall everything should be contained within its file.

when you open it there will be errors, disregard those as they will not impact anything and the interpreter
can understand it even when the IDE you have might not.

in general do not mess with the file adafruit_gps.py as it would only cause problems.

Note that GPGGA and GPRMC was changed to GNGGA and GNRMC