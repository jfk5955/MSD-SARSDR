import tkinter as tk

import motors

def start_gui():
    root = tk.Tk(screenName=None, baseName=None, className='Tk', useTk=1)
    
    root.title('Test GUI')
    setup_b = tk.Button(root, text='Setup motors', width=25, command=motors.setup_motors)
    drive_b = tk.Button(root, text='Drive motors', width=25, command=motors.drive_motors)
    kill_b = tk.Button(root, text='Kill', width=25, command=root.destroy)
    setup_b.pack()
    drive_b.pack()
    kill_b.pack()
    
    root.mainloop()