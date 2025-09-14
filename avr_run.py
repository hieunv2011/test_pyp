# avr_sim.py
import binascii

def send_data_CPU(data_h, data_l):
    data = [0] * 10
    data[0] = 0xFA
    data[1] = 0xAF
    data[2] = (data_h >> 24) & 0xFF
    data[3] = (data_h >> 16) & 0xFF
    data[4] = (data_h >> 8) & 0xFF
    data[5] = data_h & 0xFF
    data[6] = (data_l >> 24) & 0xFF
    data[7] = (data_l >> 16) & 0xFF
    data[8] = (data_l >> 8) & 0xFF
    data[9] = data_l & 0xFF
    checksum = sum(data) % 121
    data.append(checksum)
    return data

def handle_button(button_id: int):
    data_h = 0x00004004
    button_map = {
        1: 0x00004C4D,
        2: 0x00004E4F,
        3: 0x00004849,
        4: 0x00004142,
        5: 0x00004344,
        6: 0x00004546,
        7: 0x00004A4B,
        8: 0x00004747,
        9: 0x00004B4C,
    }
    data_l = button_map.get(button_id, 0x00000000)
    return send_data_CPU(data_h, data_l)

def handle_remote(hex_input: str):
    data_l = int(hex_input, 16)
    data_h = 0
    return send_data_CPU(data_h, data_l)

def format_packet(packet):
    hex_str = ''.join(f"{b:02X}" for b in packet)
    py_bytes = "bytes([%s])" % ', '.join(f"0x{b:02X}" for b in packet)
    return hex_str, py_bytes

if __name__ == "__main__":
    print("💡 AVR Simulator - nhập 'button <id>' hoặc trực tiếp hex (VD: FFF00F). Ctrl+C để thoát.")

    try:
        while True:
            user_in = input("\n👉 Nhập lệnh: ").strip()
            if not user_in:
                continue

            parts = user_in.split()

            try:
                if parts[0].lower() == "button" and len(parts) == 2:
                    btn_id = int(parts[1])
                    packet = handle_button(btn_id)

                else:
                    # coi toàn bộ input là hex remote
                    packet = handle_remote(parts[0])

                h, p = format_packet(packet)
                print(f"📤 Gói gửi đi (hex): {h}")
                print(f"📤 Gói gửi đi (Python bytes): {p}")

            except Exception as e:
                print(f"⚠️ Lỗi: {e}")

    except KeyboardInterrupt:
        print("\n👋 Kết thúc chương trình.")
