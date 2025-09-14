import serial
import serial.tools.list_ports
import time

# Các gói hex cần gửi
packages = [
    bytes([0xFA, 0xAF, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xF0, 0x0F, 0x52]),  # FFF00F
    bytes([0xFA, 0xAF, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x2A, 0xD5, 0x52]),  # FF2AD5
    bytes([0xFA, 0xAF, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0x78, 0x87, 0x52]),  # FF7887
    bytes([0xFA, 0xAF, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF, 0xE8, 0x17, 0x52]),  # FFE817
]

# Cổng COM
com_port = "COM6"
baud_rate = 9600

# Kiểm tra COM6 có tồn tại
ports = [p.device for p in serial.tools.list_ports.comports()]
if com_port not in ports:
    print(f"Không tìm thấy {com_port}. Kiểm tra kết nối USB-Serial!")
    exit(1)

try:
    ser = serial.Serial(com_port, baudrate=baud_rate, timeout=0.1)
    print(f"Đã mở {com_port} thành công. Nhấn Ctrl+C để dừng.")

    i = 0
    while True:
        # --- Gửi gói ---
        pkg = packages[i % len(packages)]   # xoay vòng các gói
        ser.write(pkg)
        print(f"Gửi: {pkg.hex().upper()}")

        # --- Đọc phản hồi ---
        time.sleep(0.05)  # cho MCU xử lý
        response = ser.read(64)
        if response:
            print(f"Nhận: {response.hex().upper()}")

        i += 1
        time.sleep(1)  # gửi 1 gói mỗi giây (tùy chỉnh)

except KeyboardInterrupt:
    print("Dừng chương trình.")
    if ser.is_open:
        ser.close()
