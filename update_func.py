# Author: Garrett Brindle
# Created: 04/08/25
# Last Edit: 04/08/25

# Using a portion of the update function from the standard test program
# Call update() when you want to take image
# Call load() when you are done imaging and what to create .mat file
# CURRENTLY DRAFT - do not worry about uninstantiated variables
# Meant for use inside larger program

import numpy as np
from scipy.io import savemat

# Initialize update counter to store data
update_cnt = 0

# Create global array to share with load and update
# 80 x 300 array with complex type
rows, cols = 80, 300
store = np.zeros((rows, cols), dtype=complex)

def load():
    """
    Uses scipy library
    Saves 2D array to .mat file
    """
    mdic = {"data_mat": store, "label": "Data_04_10_25"}
    # Save to a .mat file
    savemat("data_mat.mat", mdic)
    print("Matrix saved to 'data_mat.mat'")

def update():
    """
    Tells SDR to capture data
    Removes non-linear portion of received signal
    Preforms preliminary data storage in 2D array
	"""
    my_phaser._gpios.gpio_burst = 0
    my_phaser._gpios.gpio_burst = 1
    my_phaser._gpios.gpio_burst = 0
    data = my_sdr.rx()
    chan1 = data[0]
    chan2 = data[1]
    sum_data = chan1 + chan2

    # select just the linear portion of the last chirp
    rx_bursts = np.zeros((num_chirps, good_ramp_samples), dtype=complex)
    for burst in range(num_chirps):
        start_index = start_offset_samples + burst * num_samples_frame
        stop_index = start_index + good_ramp_samples
        rx_bursts[burst] = sum_data[start_index:stop_index]
        burst_data = np.ones(fft_size, dtype=complex) * 1e-10
        # win_funct = np.blackman(len(rx_bursts[burst]))
        win_funct = np.ones(len(rx_bursts[burst]))
        burst_data[start_offset_samples:(start_offset_samples + good_ramp_samples)] = rx_bursts[burst] * win_funct
    
    # Save the linear portion to array for later save
    store[update_cnt, :] = burst_data
    update_cnt += 1
