import threading

import gui
import motors

def kill(root):
    if 'uart' in globals():
        motors.uart.close()
    root.destroy()

def decode_inputs(distance_var, step_var, speed_var, wait_var):
    if distance_var.get():
        distance = int(distance_var.get())
    else:
        distance = 5
    if step_var.get():
        step_size = int(step_var.get())
    else:
        step_size = 100
    if speed_var.get():
        speed = int(speed_var.get())
    else:
        speed = 6000
    if wait_var.get():
        wait = float(wait_var.get())
    else:
        wait = 2
    return distance, step_size, speed, wait


def drive_motors(distance_var, step_var, speed_var, wait_var):
    distance, step_size, speed, wait = decode_inputs(distance_var, step_var, speed_var, wait_var)
    threading.Thread(target=motors.drive_motors, args=(distance, step_size, speed, wait), daemon=True).start()
        
def collect_data(distance_var, step_var, speed_var, wait_var):
    distance, step_size, speed, wait = decode_inputs(distance_var, step_var, speed_var, wait_var)
    threading.Thread(target=motors.drive_motors, args=(distance, step_size, speed, wait), daemon=True).start()
    #threading.Thread(target=radar.collect_data, args=(), daemon=True).start()       TODO: implement data collection code
    

if __name__ == "__main__":
    gui.start_gui()
    