import serial
import time

defaultDistance = 5
defaultStepSize = 100
defaultSpeed = 6000
defaultWait = 2
    
def getDefaultDistance():
    return defaultDistance
    
def getDefaultStepSize():
    return defaultStepSize
    
def getDefaultSpeed():
    return defaultSpeed
    
def getDefaultWait():
    return defaultWait

def setup_motors(plutoGui, step_size=80):
    # MACos usb port name
    #port='/dev/tty.usbserial-120'
    # Linux USB number depends on the order the USBs were plugged in
    port = '/dev/ttyUSB1'
    try:
        global uart
        uart = serial.Serial(port, 250000, timeout=1)
        plutoGui.log_message(f"Successfully opened connection on {port}")
        time.sleep(2)   # Wait for connection to be fully established before sending more commands
    except serial.SerialException as e:
        plutoGui.log_message(f"Error opening connection on {port}: {e}")
        return None
    if uart:
        setup = ("G91; relative positioning\r\n"
                "M302 S0; no cold extrusion check\r\n"
                "M211 S0; no endstop check\r\n"
                f"M92 X-{step_size} Y-{step_size} Z-{step_size} E{step_size}; Set step size & directions [steps/unit]\r\n"
                "M201 X2000 Y2000 Z2000 E3000; Set acceleration [units/s^2]\r\n"
                "M203 X300 Y300 Z300 E300; match motor feed limits [units/s]\r\n")
        uart.write(setup.encode())
        time.sleep(2)   # Wait for setup to complete before sending more commands
    
def drive_motors(plutoGui, distance, step_size, feed_rate, wait_time):
    jog = f"G0 X{step_size} Y{step_size} Z{step_size} E{step_size} F{feed_rate}\r\n"
    if 'uart' in globals():
        plutoGui.log_message(f"Driving motors:\n   Distance = {distance}\n   Step Size = {step_size}\n   Speed = {speed}")
        for i in range(distance):
            time.sleep(wait_time)
            uart.write(jog.encode())
        plutoGui.log_message(f"Done driving motors")
    else:
        plutoGui.log_message("UART is connection not open. Click 'Setup motors' and try again")

