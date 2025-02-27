from PyThreadKiller import PyThreadKiller   # PyThreadKiller uses the "threading" library and just adds a kill() function (https://github.com/kumarmuthu/PyThreadKiller)
import gui
import motors
import tkinter as tk
import time

def decode_inputs(distance_var, step_var, speed_var, wait_var):
    if distance_var.get():
        distance = int(distance_var.get())
    if step_var.get():
        step_size = int(step_var.get())
    if speed_var.get():
        speed = int(speed_var.get())
    if wait_var.get():
        wait = float(wait_var.get())
    return distance, step_size, speed, wait

def kill(plutoGui, root):
    if motorThread:
        motorThread.kill()
        plutoGui.log_message(f"Killed motors")
    if 'uart' in globals():
        motors.uart.close()
        plutoGui.log_message(f"Closed UART connection")

def drive_motors(plutoGui, distance_var, step_var, speed_var, wait_var):
    distance, step_size, speed, wait = decode_inputs(distance_var, step_var, speed_var, wait_var)
    global motorThread
    motorThread = PyThreadKiller(target=motors.drive_motors, args=(plutoGui, distance, step_size, speed, wait), daemon=True)
    
    motorThread.start()
    motorThread.join()
        
def collect_data(plutoGui, distance_var, step_var, speed_var, wait_var):
    distance, step_size, speed, wait = decode_inputs(distance_var, step_var, speed_var, wait_var)
    global motorThread
    motorThread = PyThreadKiller(target=motors.drive_motors, args=(plutoGui, distance, step_size, speed, wait), daemon=True)
    #global collectThread
    #collectThread = PyThreadKiller(target=radar.collect_data, args=(), daemon=True).start()       TODO: implement data collection code
    
    plutoGui.log_message(f"Driving motors:\n   Distance = {distance}\n   Step Size = {step_size}\n   Speed = {speed}")
    motorThread.start()
    plutoGui.log_message(f"Starting data collection")
    #collectThread.start()
    motorThread.join()
    plutoGui.log_message(f"Done driving motors")
    #collectThread.join()
    plutoGui.log_message(f"Done collecting data")
    

if __name__ == "__main__":
    root = tk.Tk(screenName=None, baseName=None, className='Tk', useTk=1)
    plutoGui = gui.GUI(root)
    