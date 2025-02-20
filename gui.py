import tkinter as tk

import main
import motors

def start_gui():
    root = tk.Tk(screenName=None, baseName=None, className='Tk', useTk=1)
    
    distance_var=tk.StringVar()
    step_var=tk.StringVar()
    speed_var=tk.StringVar()
    
    root.title('Test GUI')
    distance_l = tk.Label(root, text = 'Distance', font=('calibre',10, 'bold'))
    distance_e = tk.Entry(root, textvariable = distance_var, font=('calibre',10,'normal'))
    
    step_size_l = tk.Label(root, text = 'Step size', font=('calibre',10, 'bold'))
    step_size_e = tk.Entry(root, textvariable = step_var, font=('calibre',10,'normal'))
    
    speed_l = tk.Label(root, text = 'Speed', font=('calibre',10, 'bold'))
    speed_e = tk.Entry(root, textvariable = speed_var, font=('calibre',10,'normal'))
    
    setup_b = tk.Button(root, text='Setup motors', width=25, command=motors.setup_motors)
    drive_b = tk.Button(root, text='Drive motors', width=25, command=lambda: main.drive_motors(distance_var, step_var, speed_var))
    collect_b = tk.Button(root, text='Start data collection', width=25, command=lambda: main.collect_data(distance_var, step_var, speed_var))
    kill_b = tk.Button(root, text='Kill', width=25, command=root.destroy)
    
    i = 0
    distance_l.grid(row=i, column=0)
    distance_e.grid(row=i, column=1)
    i += 1
    step_size_l.grid(row=i, column=0)
    step_size_e.grid(row=i, column=1)
    i += 1
    speed_l.grid(row=i, column=0)
    speed_e.grid(row=i, column=1)
    i += 1
    setup_b.grid(row=i, column=0, columnspan=2)
    i += 1
    drive_b.grid(row=i, column=0, columnspan=2)
    i += 1
    collect_b.grid(row=i, column=0, columnspan=2)
    i += 1
    kill_b.grid(row=i, column=0, columnspan=2)
    i += 1
    
    root.mainloop()