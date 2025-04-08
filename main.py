from PyThreadKiller import PyThreadKiller   # PyThreadKiller uses the "threading" library and just adds a kill() function (https://github.com/kumarmuthu/PyThreadKiller)
import tkinter as tk
import time

import gui
import motors
import radar

motorThread = None
collectThread = None

def decode_inputs(distance_var, step_count_var, speed_var, wait_var, reverse_var):
    if distance_var.get():
        distance = int(distance_var.get())
    else:
        distance = motors.getDefaultDistance()
    if step_count_var.get():
        step_count = int(step_count_var.get())
    else:
        step_count = motors.getDefaultStepCount()
    if speed_var.get():
        speed = int(speed_var.get())
    else:
        speed = motors.getDefaultSpeed()
    if wait_var.get():
        wait = float(wait_var.get())
    else:
        wait = motors.getDefaultWait()
    
    if reverse_var.get():
        if bool(reverse_var.get()):
            step_count = -step_count

    return distance, step_count, speed, wait

def kill(plutoGui, root):
    if motorThread:
        motorThread.kill()
        plutoGui.log_message(f"Killed motors")
    if collectThread:
        collectThread.kill()
        plutoGui.log_message(f"Killed data collection")
    if motors.motorsSetUp:
        motors.uart.close()
        plutoGui.log_message(f"Closed UART connection")
        motors.motorsSetUp = False

def drive_motors(plutoGui, distance_var, step_count_var, speed_var, wait_var, reverse_var):
    distance, step_count, speed, wait = decode_inputs(distance_var, step_count_var, speed_var, wait_var, reverse_var)
    if motors.motorsSetUp:
        global motorThread
        motorThread = PyThreadKiller(target=motors.drive_motors, args=(plutoGui, distance, step_count, speed, wait), daemon=True)
        motorThread.start()
    else:
        plutoGui.log_message("Motors are not set up. Click 'Setup motors' and try again")
 
def collect_data(plutoGui, distance_var, step_count_var, speed_var, wait_var, reverse_var):
    distance, step_count, speed, wait = decode_inputs(distance_var, step_count_var, speed_var, wait_var, reverse_var)
    
    if motors.motorsSetUp:
        global collectThread
        collectThread = PyThreadKiller(target=radar.collect_data, args=(plutoGui, distance, step_count, speed, wait), daemon=True).start()       #TODO: implement data collection code
        collectThread.start()
    else:
        plutoGui.log_message("Motors are not set up. Click 'Setup motors' and try again")

if __name__ == "__main__":
    root = tk.Tk(screenName=None, baseName=None, className='Tk', useTk=1)
    plutoGui = gui.GUI(root)
    