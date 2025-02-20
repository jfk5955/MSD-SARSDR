import tkinter as tk

import main
import motors

def start_gui():
    root = tk.Tk(screenName=None, baseName=None, className='Tk', useTk=1)
    
    distance_var=tk.StringVar()
    step_var=tk.StringVar()
    speed_var=tk.StringVar()
    wait_var=tk.StringVar()
    
    scale = 1.5
    fontNormal = ('calibre',int(scale*15),'normal')
    fontBold = ('calibre',int(scale*15),'bold')
    buttonHeight = int(scale*1)
    buttonWidth = int(scale*15)
    
    root.title('Pluto GUI')
    distance_l = tk.Label(root, text = 'Distance', font=fontBold)
    distance_e = tk.Entry(root, textvariable = distance_var, font=fontNormal)
    
    step_size_l = tk.Label(root, text = 'Step size', font=fontBold)
    step_size_e = tk.Entry(root, textvariable = step_var, font=fontNormal)
    
    speed_l = tk.Label(root, text = 'Speed', font=fontBold)
    speed_e = tk.Entry(root, textvariable = speed_var, font=fontNormal)
    
    wait_l = tk.Label(root, text = 'Wait time', font=fontBold)
    wait_e = tk.Entry(root, textvariable = wait_var, font=fontNormal)
    
    setup_b = tk.Button(root, text='Setup motors', font=fontNormal, height=buttonHeight, width=buttonWidth, 
                        command=motors.setup_motors)
                        
    drive_b = tk.Button(root, text='Drive motors', font=fontNormal, height=buttonHeight, width=buttonWidth, 
                        command=lambda: main.drive_motors(distance_var, step_var, speed_var, wait_var))
                        
    collect_b = tk.Button(root, text='Start data collection', font=fontNormal, height=buttonHeight, width=buttonWidth, 
                          command=lambda: main.collect_data(distance_var, step_var, speed_var, wait_var))
                          
    kill_b = tk.Button(root, text='Kill', font=fontNormal, height=buttonHeight, width=buttonWidth, bg='red', 
                       command=lambda: main.kill(root))
    
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
    wait_l.grid(row=i, column=0)
    wait_e.grid(row=i, column=1)
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