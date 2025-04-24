# Author: Garrett Brindle
# Created: 04/08/25
# Last Edit: 04/08/25

# Using a portion of the update function from the standard test program
# Call update() when you want to take image
# Call load() when you are done imaging and what to create .mat file
# CURRENTLY DRAFT - do not worry about uninstantiated variables
# Meant for use inside larger program

from datetime import datetime
import numpy as np
from scipy.io import savemat

import radar

def load(store, comment):
    """
    Uses scipy library
    Saves 2D array to .mat file
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    mdic = {"data_mat": store, "label": timestamp, "comment": comment,
            "fast_time_dim": 1,
            "sample_rate_Hz": radar.my_sdr.sample_rate,
            "ramp_bandwidth_Hz": radar.my_sdr.bw,
            "ramp_time_s": radar.my_sdr.ramp_time / 1e6,
            "num_chirps": radar.my_sdr.num_chirps,
            "rx_gain_dB": radar.my_sdr.rx_hardwaregain_chan0,
            "intermediate_freq_Hz": radar.my_sdr.rx_lo,
            "radio_freq_Hz": radar.my_sdr.output_freq,
            "tone_freq_Hz": radar.my_sdr.signal_freq,
            "slow_time": radar.p2p_slow_time,
            "datetime_fmt": "YYYY-MM-DDTHH:MM:SS.ffffff",
            "cross_position": radar.p2p_cross 
           }


    # Save to a .mat file
    savemat(f"data/data_mat_{timestamp}.mat", mdic)
    print(f"Matrix saved to 'data_mat_{timestamp}.mat'")

def update(store, update_cnt, pulse):
    """
    Tells SDR to capture data
    Removes non-linear portion of received signal
    Preforms preliminary data storage in 2D array
	"""
    radar.my_phaser._gpios.gpio_burst = 0
    radar.my_phaser._gpios.gpio_burst = 1
    radar.my_phaser._gpios.gpio_burst = 0
    data = radar.my_sdr.rx()
    chan1 = data[0]
    chan2 = data[1]
    sum_data = chan1 + chan2

    # select just the linear portion of the last chirp
    rx_bursts = np.zeros((radar.my_sdr.num_chirps, radar.good_ramp_samples), dtype=complex)
    for burst in range(radar.my_sdr.num_chirps):
        start_index = radar.start_offset_samples + burst * radar.num_samples_frame
        stop_index = start_index + radar.good_ramp_samples
        rx_bursts[burst] = sum_data[start_index:stop_index]
        burst_data = np.ones(radar.fft_size, dtype=complex) * 1e-10
        # win_funct = np.blackman(len(rx_bursts[burst]))
        win_funct = np.ones(len(rx_bursts[burst]))
        burst_data[radar.start_offset_samples:(radar.start_offset_samples + radar.good_ramp_samples)] = rx_bursts[burst] * win_funct
    
    # Save the linear portion to array for later save
    store[:, update_cnt, pulse] = burst_data
    return store
