import serial
import time

def setup_motors(step_size=80):
    # MACos usb port name
    #port='/dev/tty.usbserial-120'
    # Linux USB number depends on the order the USBs were plugged in
    port = '/dev/ttyUSB1'
    try:
        global uart
        uart = serial.Serial(port, 250000, timeout=1)
        print(f"Successfully opened connection on {port}")
        time.sleep(2)   # Wait for connection to be fully established before sending more commands
    except serial.SerialException as e:
        print(f"Error opening connection on {port}: {e}")
        return None
    if uart:
        setup = ("G91; relative positioning\r\n"
                "M302 S0; no cold extrusion check\r\n"
                "M211 S0; no endstop check\r\n"
                f"M92 X-{step_size} Y-{step_size} Z-{step_size} E{step_size}; Set step size & directions [steps/unit]\r\n"
                "M201 X2000 Y2000 Z2000 E3000; Set acceleration [units/s^2]\r\n"
                "M203 X300 Y300 Z300 E300; match motor feed limits [units/s]\r\n")
        uart.write(setup.encode())
        time.sleep(2)   # Wait for connection to be fully established before sending more commands
    
def drive_motors(distance=5, step_size=100, feed_rate=6000, wait_time=2):
    print(f"Driving motors:\n   Distance = {distance}\n   Step Size = {step_size}\n   Speed = {feed_rate}")
    jog = f"G0 X{step_size} Y{step_size} Z{step_size} E{step_size} F{feed_rate}\r\n"
    for i in range(distance):
        time.sleep(wait_time)
        uart.write(jog.encode())
    print("Done driving motors")
        
if __name__ == "__main__":
    setup_motors()
    drive_motors()
        
