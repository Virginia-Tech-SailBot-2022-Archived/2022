import math
import time

import serial
import RPi.GPIO as GPIO

lidarpin = 17
picampin = 22
webcampin = 27


class Sensors:
    """
    Reading inputs from GPS, Lidar, and Airmar

    :var serairmar serial object for airmar usb
    :var sergps serial object for gps usb
    :var serlidar serial object for lidar usb
    """

    def __init__(self, airmarport, gpsport, lidarport):
        """
        Constructor, Initiates Serial Connections
        :param airmarport: airmar USB port, ex. /dev/ttyUSB0
        :param gpsport: gps USB port, ex. /dev/ttyUSB1
        :param lidarport: lidar USB port, ex. /dev/ttyUSB2
        """

        self.serlidar = serial.Serial('COM15', 115200)
        self.serairmar = serial.Serial('COM14', 4800)
        self.sergps = serial.Serial(gpsport, 4800)

    def getGPS(self):
        """
        Getter method for GPS
        :return: current GPS coordinate, 0 if GPS unavailable
        """
        line: str
        while True:
            line = self.sergps.readline().decode('utf-8')
            if line.startswith("$GPGGA"):
                break

        strs = line.split(",")

        if strs[6] == '0':
            return 0

        latdeg = int(strs[2][0:2])
        latmin = float(strs[2][2:])

        longdeg = int(strs[4][0:2])
        longmin = float(strs[4][2:])

        coord = {"LAT": latdeg * 60 + latmin, "LONG": longdeg * 60 + longmin}
        return coord

    def getWindData(self):
        """ Returns Wind Direction (with respect to Boat) """
        line: str
        while True:
            line = self.serairmar.readline().decode('utf-8')
            if line.startswith("$WIMWV"):
                strs = line.split(",")

                if strs[2] == "R":
                    return float(strs[1])

    def getHeading(self):
        """ Returns Current Heading with respect to North """
        line: str
        while True:
            line = self.serairmar.readline().decode('utf-8')
            if line.startswith("$HCHDT"):
                strs = line.split(",")

                if strs[2] == "T":
                    return float(strs[1])


class Motors:
    """
    Arduino Motor Controls
    :var serardu serial object for arduino connection
    """

    def __init__(self, arduCOM):
        """
        Constructor
        :param arduCOM: arduino USB port, ex. /dev/ttyUSB3
        """
        self.serardu = serial.Serial(arduCOM, 9600)

    def moveMast(self, degree):
        """
        Moving Mast motor
        :param degree: mast motor degree: between 0 and 180

        """
        str = "M" + str(degree)
        self.serardu.write(str)

    def moveRudder(self, degree):
        """
        Moving Rudder motor
        :param degree: rudder motor degree: between 0 and 180
        """
        str = "R" + str(degree)
        self.serardu.write(str)


class Servos:
    def __init__(self):
        self.pwmlidar = GPIO.PWM(lidarpin, 300)
        self.pwmwebcam = GPIO.PWM(webcampin, 50)
        self.pwmpicam = GPIO.PWM(picampin, 50)

    def lidarrotation(self):
        """
        lidar: 500us (0) to 2500us (270)
        :param lidarpin:
        :return:
        """
        self.pwmlidar.start()
        self.pwmduration = 500

def calc_bearing(pointA, pointB) ->float:
    deg2rad = math.pi / 180
    latA = pointA[0] * deg2rad
    latB = pointB[0] * deg2rad
    lonA = pointA[1] * deg2rad
    lonB = pointB[1] * deg2rad

    delta_ratio = math.log(math.tan(latB/ 2 + math.pi / 4) / math.tan(latA/ 2 + math.pi / 4))
    delta_lon = abs(lonA - lonB)

    delta_lon %= math.pi
    bearing = math.atan2(delta_lon, delta_ratio)/deg2rad
    return bearing


servo = Servos()
motor = Motors()
sensor = Sensors()

print('printing information to the terminal:')
x = input('Center mast')
motor.moveMast(90)
x = input('move mast to fully counterclockwise')
motor.moveMast(0)
y = print('move mast to fully clockwise')
motor.moveMast(180)
z = input('Center Rudders')
motor.moveRudder(90)
x = input('move rudders to fully counterclockwise')
motor.moveRudder(0)
y = input('move rudders to fully clockwise')
motor.moveRudder(180)

print('rudders and mast test over')
start = time.time()

print('what tf is a bearing')

while time.time()-start < 60:
    print('where is the boat?',sensor.getGPS())
    print('what is the wind right now?',sensor.getWindData())
    print('where are we headed', sensor.getHeading())
    time.sleep(5)
