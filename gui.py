import tkinter as tk
from tkinter import scrolledtext
import main
import motors

class GUI:
    def __init__(self, root):        
        distance_var=tk.StringVar()
        step_count_var=tk.StringVar()
        speed_var=tk.StringVar()
        wait_var=tk.StringVar()
        port_var=tk.StringVar()
        reverse_var = tk.IntVar()
        
        scale = 1.5
        fontSmall = ('calibre',int(scale*10),'normal')
        fontNormal = ('calibre',int(scale*15),'normal')
        fontBold = ('calibre',int(scale*15),'bold')
        buttonHeight = int(scale*1)
        buttonWidth = int(scale*15)
        checkBoxHeight = int(scale*1)
        checkBoxWidth = int(scale*15)
        textBoxHeight = int(scale*10)
        textBoxWidth = int(scale*40)
        
        root.title('Pluto GUI')
        distance_label = tk.Label(root, text = 'Distance', font=fontBold)
        distance_entry = tk.Entry(root, textvariable = distance_var, font=fontNormal)
        distance_entry.insert(0, motors.getDefaultDistance())
        
        step_count_label = tk.Label(root, text = '# of mm/step', font=fontBold)
        step_count_entry = tk.Entry(root, textvariable = step_count_var, font=fontNormal)
        step_count_entry.insert(0, motors.getDefaultStepCount())
        
        speed_label = tk.Label(root, text = 'Speed', font=fontBold)
        speed_entry = tk.Entry(root, textvariable = speed_var, font=fontNormal)
        speed_entry.insert(0, motors.getDefaultSpeed())
        
        wait_label = tk.Label(root, text = 'Wait time', font=fontBold)
        wait_entry = tk.Entry(root, textvariable = wait_var, font=fontNormal)
        wait_entry.insert(0, motors.getDefaultWait())
        
        port_label = tk.Label(root, text = 'Port path', font=fontBold)
        port_entry = tk.Entry(root, textvariable = port_var, font=fontNormal)
        port_entry.insert(0, motors.getDefaultPort())
        
        reverse_checkbox = tk.Checkbutton(root, text="Reverse", font=fontSmall, height=checkBoxHeight, width=checkBoxWidth, variable=reverse_var)
        
        setup_button = tk.Button(root, text='Setup motors', font=fontNormal, height=buttonHeight, width=buttonWidth, command=lambda: motors.setup_motors(self, port_var))
                            
        drive_button = tk.Button(root, text='Drive motors', font=fontNormal, height=buttonHeight, width=buttonWidth, command=lambda: main.drive_motors(self, distance_var, step_count_var, speed_var, wait_var, reverse_var))
                            
        collect_button = tk.Button(root, text='Start data collection', font=fontNormal, height=buttonHeight, width=buttonWidth, command=lambda: main.collect_data(self, distance_var, step_count_var, speed_var, wait_var, reverse_var))
                            
        kill_button = tk.Button(root, text='Kill', font=fontNormal, height=buttonHeight, width=buttonWidth, bg='red', command=lambda: main.kill(self, root))
                        
        self.log_t = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=textBoxHeight, width=textBoxWidth, state=tk.DISABLED)
        
        i = 0
        distance_label.grid(row=i, column=0)
        distance_entry.grid(row=i, column=1)
        self.log_t.grid(row=i, column=2, rowspan=4, columnspan=2)
        i += 1
        step_count_label.grid(row=i, column=0)
        step_count_entry.grid(row=i, column=1)
        i += 1
        speed_label.grid(row=i, column=0)
        speed_entry.grid(row=i, column=1)
        i += 1
        wait_label.grid(row=i, column=0)
        wait_entry.grid(row=i, column=1)
        i += 1
        setup_button.grid(row=i, column=0, columnspan=2)
        port_label.grid(row=i, column=2)
        port_entry.grid(row=i, column=3)
        i += 1
        drive_button.grid(row=i, column=0, columnspan=2)
        reverse_checkbox.grid(row=i, column=1, columnspan=2, sticky="e")
        i += 1
        collect_button.grid(row=i, column=0, columnspan=2)
        i += 1
        kill_button.grid(row=i, column=0, columnspan=2)
        i += 1
        
        root.mainloop()
    
    def log_message(self, message="This is a log message!"):
        """Appends a message to the log box."""
        self.log_t.config(state=tk.NORMAL)  # Enable editing temporarily
        self.log_t.insert(tk.END, message + "\n")  # Insert new log entry
        self.log_t.config(state=tk.DISABLED)  # Disable editing again
        self.log_t.see(tk.END)  # Auto-scroll to the bottom
