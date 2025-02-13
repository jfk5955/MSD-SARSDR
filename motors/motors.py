import serial
import time

def open_uart_connection(port, baudrate=250000, timeout=1):
    """Opens a UART connection over USB."""

    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        print(f"Successfully opened connection on {port}")
        time.sleep(2)   # Wait for connection to be fully established before sending more commands
        return ser
    except serial.SerialException as e:
        print(f"Error opening connection on {port}: {e}")
        return None

def setup_motors(step_size=80):
    setup = ("G91; relative positioning\r\n"
            "M302 S0; no cold extrusion check\r\n"
            "M211 S0; no endstop check\r\n"
            f"M92 X-{step_size} Y-{step_size} Z-{step_size} E{step_size}; Set step size & directions [steps/unit]\r\n"
            "M201 X2000 Y2000 Z2000 E3000; Set acceleration [units/s^2]\r\n"
            "M203 X300 Y300 Z300 E300; match motor feed limits [units/s]\r\n")
    ser.write(setup.encode())
    time.sleep(2)   # Wait for connection to be fully established before sending more commands
    
def move_motors(step_size=100, distance=1, wait_time=2, feed_rate=6000):
    jog = f"G0 X{step_size} Y{step_size} Z{step_size} E{step_size} F{feed_rate}\r\n"
    for i in range(distance):
        ser.write(jog.encode())
        time.sleep(wait_time)
    
    
if __name__ == "__main__":
    port = '/dev/ttyUSB1'
    ser = open_uart_connection(port)

    if ser:
        setup_motors()
        move_motors(100, 10, 2)
        ser.close()
