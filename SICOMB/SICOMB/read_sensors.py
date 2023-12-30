import threading
import serial
import time

def send_hex_command(ser, command_hex):
    ser.write(bytearray.fromhex(command_hex))

def read_line(ser):
    isReading = False
    readData = []

    while True:
        rc = ser.read(1)

        if rc == b'\xAA':
            isReading = True
            currentReadlength = 0
            readData = []

        if isReading:
            readData.append(rc.hex().upper())

            if currentReadlength == 1:
                if rc != b'\x02':
                    isReading = False

            if rc == b'\xDD':
                return readData

            currentReadlength += 1


def get_uids():
    from SICOMB.settings import AUX
    
    command_hex = "AA 00 27 00 03 22 FF FF 4A DD"
    command_hex_2 = "AA 00 B6 00 02 03 E8 A3 DD"
    
    ser = AUX['serial_port_rfid']
    
    print("\nConexão com sensor RFID configurada com sucesso!\n")
    
    send_hex_command(ser, command_hex)
    send_hex_command(ser, command_hex_2)

    while True:
        try:
            line = read_line(ser)
            line = "".join(line[6:len(line) - 2])

            print(AUX["uids"])
            if line not in AUX["uids"]:
                AUX["uids"].append(line)
        except Exception as e:
            print("\nConexão com sensor RFID perdida!\n")
            print(e)
            
            while ser is None:
                try:
                    if ser is not None: ser.close()
                    ser = serial.Serial(AUX["PORT_RFID"], 115200)
                except Exception as e:
                    time.sleep(0.5)
                    print(e)
            print("\nConexão reestabelecida!\n")


def get_fingerprint():
    from SICOMB.settings import AUX
    
    print("\nConexão com sensor leitor de impressão digital configurada com sucesso!\n")
    
    ser = AUX['serial_port_fingerprint']
    
    while True:
        try:
            line = ser.readline().decode('utf-8')
            print(line)
            if not line:
                continue
            line = line.split("::")
        
            if len(line) > 1:
                AUX["message_fingerprint_sensor"] = line
        except Exception as e:
            print("\nConexão com sensor leitor de impressão digital perdida!\n")
            print(e)
            AUX["message_fingerprint_sensor"] = ['FINGERPRINT', 'ERROR', 'Conexão com sensor leitor de impressão digital perdida!']
            while ser is None:
                try:
                    if ser is not None: ser.close()
                    ser = serial.Serial(AUX["PORT_FINGERPRINT"], 115200)
                except Exception as e:
                    time.sleep(0.5)
                    print(e)
            print("\nConexão reestabelecida!\n")
    
from SICOMB.settings import AUX

if AUX["SENSOR_RFID"]:         
    THREAD_RFID = threading.Thread(target=get_uids)
    THREAD_RFID.start()

if AUX["SENSOR_FINGERPRINT"]:
    THREAD_FINGERPRINT = threading.Thread(target=get_fingerprint)
    THREAD_FINGERPRINT.start()