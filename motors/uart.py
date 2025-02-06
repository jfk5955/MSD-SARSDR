import serial
import time

def open_uart_connection(port, baudrate=250000, timeout=1):
    """Opens a UART connection over USB."""

    try:
        ser = serial.Serial(port, baudrate, timeout=timeout)
        print(f"Successfully opened connection on {port}")
        return ser
    except serial.SerialException as e:
        print(f"Error opening connection on {port}: {e}")
        return None

if __name__ == "__main__":
    # Replace '/dev/ttyUSB0' with the appropriate port for your system
    port = '/dev/cu.usbserial-1120' 
    ser = open_uart_connection(port)

    time.sleep(2)
    
    if ser:
        # Setup
        setup = ("G91; relative positioning\r\n"
                "M302 S0; no cold extrusion check\r\n"
                "M211 S0; no endstop check\r\n"
                "M92 X-80 Y-80 Z-80 E80; Set step size & directions [steps/unit]\r\n"
                "M201 X2000 Y2000 Z2000 E3000; Set acceleration [units/s^2]\r\n"
                "M203 X300 Y300 Z300 E300; match motor feed limits [units/s]\r\n"
                "G0 F6000; Set default G0 feedrate [units/min]\r\n")
        print(ser.write(setup.encode()))
        
        time.sleep(2)
        
        # Jog
        jog = "G0 X100 Y100 Z100 E100\r\n"
        print(ser.write(jog.encode()))

        # Close the connection
        ser.close()