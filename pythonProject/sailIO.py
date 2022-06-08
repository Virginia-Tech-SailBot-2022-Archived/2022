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



        coord = {"LAT": latdeg*60 + latmin, "LONG": longdeg*60 + longmin}
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
                
                
    def getTrueWindData(self):
        """ Returns Wind Direction and Speed with respect to True North """
        line: str
        while True:
            line = self.serairmar.readline().decode('utf-8')
            if line.startswith("$WIMWD"):
                strs = line.split(",")
                if(strs[2] == "T"):
                    return {"Angle": float(strs[1]), "Speed": float(strs[5])}



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

