from sailIO import Sensors


#ser = serial.Serial('COM15', 115200)
#ser2: serial

#ser2 = serial.Serial('COM14', 4800)


def getGPSData():
    sensors = Sensors('COM14')
    print(sensors.getGPS())
    """
    while True:
        str = ser2.readline().decode('utf-8')
        if str.startswith("$GPGGA"):
            strs = str.split(",")
            print(strs)
        ser2.flushInput()
"""
"""
def getTFminiData():
    ser.write(struct.pack('>BBBB', 0x5A, 0x04, 0x04, 0x62))

    while True:
        counta = ser.inWaiting()
        if counta >= 9:
            break

    print(ser.read(9).hex())
    ser.flushInput()

    while True:
        count = ser.inWaiting()
        if count > 8:
            recv = ser.read(9)
            ser.flushInput()
            if recv[0] == 0x59 and recv[1] == 0x59:  # 0x59 is 'Y'

                print(recv.hex())
                low = int(recv[2])
                high = int(recv[3])

                distance = low + high * 256
                print(distance)


            """


if __name__ == '__main__':
    getGPSData()
    """
    try:
        if ser2.is_open == False:
            ser2.open()
        getGPSData()
        #getTFminiData()
    except KeyboardInterrupt:   # Ctrl+C
        if ser2 != None:
            ser2.close()
            """