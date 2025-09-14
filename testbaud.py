import serial
import time

# Cổng nối với MCU
COM_PORT = "COM6"

# Các baudrate phổ biến cần thử
baudrates = [9600, 19200, 38400, 57600, 115200]

def test_baudrate(com, baud):
    try:
        with serial.Serial(com, baudrate=baud, timeout=0.5) as ser:
            data = ser.read(20)  # đọc 20 byte
            if data:
                print(f"[{baud}] Received:", data.hex().upper())
                # kiểm tra header gói MCU
                if data[0:2] == b'\xFA\xAF':
                    print(f"[{baud}] Likely correct baudrate!")
                    return True
            return False
    except serial.SerialException as e:
        print(f"[{baud}] Error: {e}")
        return False

for br in baudrates:
    test_baudrate(COM_PORT, br)
    time.sleep(0.5)
