import serial


def send_light_request(index, color):
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    payload = str(index) + "," + color
    ser.write(str.encode(payload))
