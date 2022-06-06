import struct
import serial


ser = serial.Serial('COM15', 115200)
#ser2: serial

#ser2 = serial.Serial('COM8', 4800)

def getGPSData():
    #sensors = Sensors('COM14')
    #print(sensors.getGPS())

    while True:
        str = ser2.readline().decode('utf-8')
        if str.startswith("$GPGGA"):
            strs = str.split(",")
            if(strs[2] == ''):
                print("0")
            else:
                print(strs[2], strs[4])

        ser2.flushInput()






def getTFminiData():
    #ser.write(struct.pack('>BBBB', 0x5A, 0x04, 0x04, 0x62))
    """
    while True:
        counta = ser.inWaiting()
        if counta >= 9:
            break

    recv = ser.read(9)
    #print(ser.read(9).hex())
    print(int(recv[2]) + int(recv[3]) * 256)
    ser.flushInput()
"""
    while True:
        count = ser.inWaiting()
        if count > 8:
            recv = ser.read(9)
            ser.flushInput()
            if recv[0] == 0x59 and recv[1] == 0x59:  # 0x59 is 'Y'

                #print(recv.hex())
                low = int(recv[2])
                high = int(recv[3])

                distance = low + high * 256
                print(distance)





if __name__ == '__main__':
    getTFminiData()
"""
    try:
        if ser.is_open == False:
            ser.open()
        #getGPSData()
        getTFminiData()

    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()
            """
