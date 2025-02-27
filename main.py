from PyThreadKiller import PyThreadKiller   # PyThreadKiller uses the "threading" library and just adds a kill() function (https://github.com/kumarmuthu/PyThreadKiller)
import tkinter as tk
import time

import gui
import motors
import collection

motorThread = None
collectThread = None

def decode_inputs(distance_var, step_var, speed_var, wait_var):
    if distance_var.get():
        distance = int(distance_var.get())
    else:
        distance = motors.getDefaultDistance()
    if step_var.get():
        step_size = int(step_var.get())
    else:
        step_size = motors.getDefaultStepSize()
    if speed_var.get():
        speed = int(speed_var.get())
    else:
        speed = motors.getDefaultSpeed()
    if wait_var.get():
        wait = float(wait_var.get())
    else:
        wait = motors.getDefaultWait()
    return distance, step_size, speed, wait

def kill(plutoGui, root):
    if motorThread:
        motorThread.kill()
        plutoGui.log_message(f"Killed motors")
    if collectThread:
        collectThread.kill()
        plutoGui.log_message(f"Killed data collection")
    try:
        if motors.uart.is_open:
            motors.uart.close()
            plutoGui.log_message(f"Closed UART connection")
    except Exception as e:
        plutoGui.log_message(f"Tried closing UART connection but failed: {e}")

def drive_motors(plutoGui, distance_var, step_var, speed_var, wait_var):
    distance, step_size, speed, wait = decode_inputs(distance_var, step_var, speed_var, wait_var)
    global motorThread
    
    motorThread = PyThreadKiller(target=motors.drive_motors, args=(plutoGui, distance, step_size, speed, wait), daemon=True)
    
    motorThread.start()
        
def collect_data(plutoGui, distance_var, step_var, speed_var, wait_var):
    distance, step_size, speed, wait = decode_inputs(distance_var, step_var, speed_var, wait_var)
    global motorThread
    global collectThread
    
    motorThread = PyThreadKiller(target=motors.drive_motors, args=(plutoGui, distance, step_size, speed, wait), daemon=True)
    collectThread = PyThreadKiller(target=collection.collect_data, args=(plutoGui), daemon=True).start()       #TODO: implement data collection code
    
    motorThread.start()
    collectThread.start()
    

if __name__ == "__main__":
    root = tk.Tk(screenName=None, baseName=None, className='Tk', useTk=1)
    plutoGui = gui.GUI(root)
    