import threading

import gui
import motors

def decode_inputs(distance_var, step_var, speed_var):
    if distance_var.get():
        distance = int(distance_var.get())
    else:
        distance = 5
    if step_var.get():
        step_size = int(step_var.get())
    else:
        step_size = 1
    if speed_var.get():
        speed = int(speed_var.get())
    else:
        speed = 6000
    return distance, step_size, speed


def drive_motors(distance_var, step_var, speed_var):
    distance, step_size, speed = decode_inputs(distance_var, step_var, speed_var)
    print(f"Driving motors:\n   Distance = {distance}\n   Step Size = {step_size}\n   Speed = {speed}")
    motors.drive_motors(distance, step_size, speed)
        
def collect_data(distance_var, step_var, speed_var):
    distance, step_size, speed = decode_inputs(distance_var, step_var, speed_var)
    threading.Thread(target=motors.drive_motors, args=(distance, step_size, speed), daemon=True).start()
    #threading.Thread(target=radar.collect_data, args=(), daemon=True).start()       TODO: implement data collection code
    

if __name__ == "__main__":
    gui.start_gui()
    