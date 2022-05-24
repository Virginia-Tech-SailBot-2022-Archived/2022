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
            self.sergps.flushInput()

        strs = line.split(",")

        if strs[6] == '0':
            return 0

        coord = {"LAT": strs[2], "LONG": strs[4]}
        return coord
"""
    def getLIDAR(self):
        self.serlidar.write(struct.pack('>BBBB', 0x5A, 0x04, 0x04, 0x62))
        while True:
            counta = self.serlidar.inWaiting()
            if counta >= 9:
                break

        arr = self.serlidar.read(9).hex()
        print(self.serlidar.read(9).hex())
        dist = arr[2] + arr[3] * 256
        self.serlidar.flushInput()
        return dist
"""
    def getWindData(self):
        """ Returns Wind Direction (with respect to Boat) and Wind Speed (Knots)"""
    def getHeading(self):
        """ Returns Current Heading with respect to North """

    def
        
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
        self.serardu.write('')

    def moveRudder(self, degree):
        """
        Moving Rudder motor
        :param degree: rudder motor degree: between 0 and 180
        """
        self.serardu.write('')

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

