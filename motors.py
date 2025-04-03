import serial
import time

defaultDistance = 5
defaultStepSize = 50 # steps/mm
defaultStepCount = 100 # of mm
defaultSpeed = 6000
defaultWait = 2

uart = None
motorsSetUp = False

# MACos usb port name
#port='/dev/tty.usbserial-120'
# Linux USB number depends on the order the USBs were plugged in
defaultPort = '/dev/ttyUSB0'
    
def getDefaultDistance():
    return defaultDistance

def getDefaultStepCount():
    return defaultStepCount
    
def getDefaultSpeed():
    return defaultSpeed
    
def getDefaultWait():
    return defaultWait

def getDefaultPort():
    return defaultPort

def setup_motors(plutoGui, port_var):
    if port_var.get():
        port = port_var.get()
    else:
        port = getDefaultPort()
    
    try:
        global uart
        uart = serial.Serial(port, 250000, timeout=1)
        plutoGui.log_message(f"Successfully opened connection on {port}")
        time.sleep(2)   # Wait for connection to be fully established before sending more commands
    except serial.SerialException as e:
        plutoGui.log_message(f"Error opening connection on {port}: {e}")
        return None
    if uart.is_open:
        setup = ("G91; relative positioning\r\n"
                "M302 S0; no cold extrusion check\r\n"
                "M211 S0; no endstop check\r\n"
                f"M92 X{defaultStepSize} Y{defaultStepSize} Z{defaultStepSize} E-{defaultStepSize}; Set step size & directions [steps/unit]\r\n"
                "M201 X2000 Y2000 Z2000 E3000; Set acceleration [units/s^2]\r\n"
                "M203 X300 Y300 Z300 E300; match motor feed limits [units/s]\r\n")
        uart.write(setup.encode())
        time.sleep(2)   # Wait for setup to complete before sending more commands
        global motorsSetUp
        motorsSetUp = True
    
def drive_motors(plutoGui, distance, step_count, feed_rate, wait_time):
    jog = f"G0 X{step_count} Y{step_count} Z{step_count} E{step_count} F{feed_rate}\r\n"
    plutoGui.log_message(f"Driving motors:\n   Distance = {distance}\n   Step Size = {step_count}\n   Speed = {feed_rate}")
    for i in range(distance):
        uart.write(jog.encode())
        time.sleep(wait_time)
    plutoGui.log_message(f"Done driving motors")
        

