import serial
import serial.tools.list_ports

com_port = "COM6"
baud_rate = 9600  # chỉnh theo MCU

# Kiểm tra COM6 có tồn tại
ports = [p.device for p in serial.tools.list_ports.comports()]
if com_port not in ports:
    print(f"Không tìm thấy {com_port}. Kiểm tra kết nối USB-Serial!")
    exit(1)
else:
    print(f"{com_port} có tồn tại. Bắt đầu đọc dữ liệu...")

try:
    ser = serial.Serial(com_port, baudrate=baud_rate, timeout=0.1)  # timeout ngắn để đọc liên tục
    print(f"Đã mở {com_port} thành công. Nhấn Ctrl+C để dừng.")

    while True:
        data = ser.read(64)  # đọc tối đa 64 byte
        if data:
            # In dữ liệu nhận được dưới dạng hex, in hoa
            print(data.hex().upper())

except serial.SerialException as e:
    print(f"Lỗi mở cổng {com_port}: {e}")

except KeyboardInterrupt:
    print("Đã dừng đọc dữ liệu.")
    if ser.is_open:
        ser.close()
