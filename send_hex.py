# import serial
# import time

# # -----------------------------
# # Cấu hình cổng COM
# # -----------------------------
# COM_SEND = "COM7"   # Python gửi trực tiếp sang RealTerm mở COM8
# BAUD = 9600
# TIMEOUT = 1

# # Gói dữ liệu cần gửi (11 byte)
# packages = [
#     bytes([0xFA, 0xAF, 0x00, 0x00, 0x40, 0x04, 0x00, 0x00, 0x4C, 0x4D, 0x29])
# ]

# # -----------------------------
# # Gửi dữ liệu mỗi 5 giây
# # -----------------------------
# try:
#     ser_send = serial.Serial(COM_SEND, baudrate=BAUD, timeout=TIMEOUT)
#     print(f"[SEND] Opened {COM_SEND} for sending")

#     while True:
#         for pkg in packages:
#             ser_send.write(pkg)
#             print(f"[SEND] Sent: {pkg.hex().upper()}")
#         time.sleep(5)  # gửi lại sau 5 giây

# except serial.SerialException as e:
#     print(f"[SEND] Error: {e}")

import serial
import time

# -----------------------------
# Cấu hình cổng COM
# -----------------------------
COM_SEND = "COM6"   # Cổng thiết bị đang mở
BAUD = 38400
TIMEOUT = 1

# -----------------------------
# Danh sách gói dữ liệu (data_h, data_l)
# -----------------------------
commands = [
    (0x00004004, 0x00004C4D),  # RG
    (0x00004004, 0x0000D0D1),  # QT
    (0x00004004, 0x00000A0B),  # HL
    (0x00004004, 0x00008A8B),  # TN
    (0x00004004, 0x0000F0F1),  # CL
    (0x00004004, 0x00000405),  # TS
    (0x00004004, 0x00008485),  # GS
    (0x00004004, 0x0000BCBD),  # BD
    (0x00004004, 0x0000A0A1)   # IN
]

def build_packet(data_h, data_l):
    """Tạo gói 11 byte + checksum giống MCU"""
    data = [
        0xFA,
        0xAF,
        (data_h >> 24) & 0xFF,
        (data_h >> 16) & 0xFF,
        (data_h >> 8) & 0xFF,
        data_h & 0xFF,
        (data_l >> 24) & 0xFF,
        (data_l >> 16) & 0xFF,
        (data_l >> 8) & 0xFF,
        data_l & 0xFF
    ]
    checksum = sum(data) % 121
    data.append(checksum)
    return bytes(data)

# -----------------------------
# Gửi dữ liệu liên tục, mỗi lệnh delay 1 giây
# -----------------------------
try:
    ser = serial.Serial(COM_SEND, baudrate=BAUD, timeout=TIMEOUT)
    print(f"[SEND] Opened {COM_SEND} for sending")

    while True:
        for h, l in commands:
            packet = build_packet(h, l)
            ser.write(packet)
            print(f"[SEND] Sent: {packet.hex().upper()}")
            time.sleep(2)  # delay 1 giây giữa các lệnh
        print("[SEND] All commands sent, repeating...")

except serial.SerialException as e:
    print(f"[SEND] Error: {e}")
 