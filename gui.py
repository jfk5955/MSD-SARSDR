import tkinter as tk
from tkinter import scrolledtext
import main
import motors
import radar

class GUI:
    def __init__(self, root):        
        distance_var=tk.StringVar()
        step_count_var=tk.StringVar()
        speed_var=tk.StringVar()
        wait_var=tk.StringVar()
        port_var=tk.StringVar()
        comment_var=tk.StringVar()
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
        distance_label = tk.Label(root, text = 'Number of Steps', font=fontBold)
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

        comment_label = tk.Label(root, text = 'Test comment', font=fontBold)
        self.comment_entry = tk.Entry(root, textvariable = comment_var, font=fontNormal)
        self.comment_entry.insert(0, "")
        
        reverse_checkbox = tk.Checkbutton(root, text="Reverse", font=fontSmall, height=checkBoxHeight, width=checkBoxWidth, variable=reverse_var)
        
        setup_motors_button = tk.Button(root, text='Setup motors', font=fontNormal, height=buttonHeight, width=buttonWidth, command=lambda: motors.setup_motors(self, port_var))
        
        setup_radar_button = tk.Button(root, text='Setup radar', font=fontNormal, height=buttonHeight, width=buttonWidth, command=lambda: radar.setup_radar(self))
                            
        drive_button = tk.Button(root, text='Drive motors', font=fontNormal, height=buttonHeight, width=buttonWidth, command=lambda: main.drive_motors(self, distance_var, step_count_var, speed_var, wait_var, reverse_var, comment_var))
                            
        collect_button = tk.Button(root, text='Start collection', font=fontNormal, height=buttonHeight, width=buttonWidth, command=lambda: main.collect_data(self, distance_var, step_count_var, speed_var, wait_var, reverse_var, comment_var))
        
        collect_cont_button = tk.Button(root, text='Start continuous collection', font=fontNormal, height=buttonHeight, width=buttonWidth, command=lambda: main.collect_cont_data(self, distance_var, step_count_var, speed_var, wait_var, reverse_var, comment_var))
                            
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
        setup_motors_button.grid(row=i, column=0, columnspan=2)
        port_label.grid(row=i, column=2)
        port_entry.grid(row=i, column=3)
        i += 1
        setup_radar_button.grid(row=i, column=0, columnspan=2)
        comment_label.grid(row=i, column=2)
        self.comment_entry.grid(row=i, column=3)
        i += 1
        drive_button.grid(row=i, column=0, columnspan=2)
        reverse_checkbox.grid(row=i, column=1, columnspan=2, sticky="e")
        i += 1
        collect_button.grid(row=i, column=0, columnspan=2)
        i += 1
        collect_cont_button.grid(row=i, column=0, columnspan=2)
        i += 1
        kill_button.grid(row=i, column=0, columnspan=2)
        i += 1
        
        root.mainloop()
    '''
    FIXME (doesn't work): This function is meant to clear the text in the comment box once a data collection is complete
    so that multiple files don't end up getting the same comment.
    '''
    def clear_comment(self):
        self.comment_entry.config(state=tk.NORMAL)  
        self.comment_entry.insert(tk.END, "")
        self.comment_entry.config(state=tk.DISABLED)  

    '''
    FIXME (doesn't work): This function is meant create a progress bar style message in the log box
    '''
    def log_progress(self, message):
        """Appends a message to the log box."""
        self.log_t.config(state=tk.NORMAL)
        self.log_t.insert(tk.ANCHOR, message)
        self.log_t.config(state=tk.DISABLED)
        self.log_t.see(tk.END)

    def log_message(self, message):
        """Appends a message to the log box."""
        self.log_t.config(state=tk.NORMAL)  # Enable editing temporarily
        self.log_t.insert(tk.END, message + "\n")  # Insert new log entry
        self.log_t.config(state=tk.DISABLED)  # Disable editing again
        self.log_t.see(tk.END)  # Auto-scroll to the bottom
