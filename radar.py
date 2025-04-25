# Library imports
import adi
import numpy as np
import os
import sys
import time
from datetime import datetime

# Local imports
import motors
import update_func

def getDefaultComment():
    return ""

'''
Standard device instantiation and setup
'''
def setup_radar(plutoGui):
    # KEY SETUP PARAMETERS
    sample_rate = 20e6    # Sample rate specific to Pluto
    center_freq = 2.1e9  # Pluto LO frequency - IF frequency
    signal_freq = 100e3  # Information being sent
    rx_gain = 50   # range: (-3, 70)
    output_freq = 10e9
    default_chirp_bw = 500e6
    ramp_time = 500      # ramp time in us (micro seconds)
    num_slices = 100     # this sets how much time will be displayed on the waterfall plot
    plot_freq = 100e3    # x-axis freq range to plot
    num_chirps = 1

    # Instantiate all the Devices
    rpi_ip = "ip:phaser.local"  # IP address of the Raspberry Pi
    sdr_ip = "ip:pluto.local"  # "192.168.2.1, or pluto.local" - Transceiver IP address
    global my_phaser, my_sdr
    my_sdr = adi.ad9361(uri=sdr_ip)   # Create objects
    my_phaser = adi.CN0566(uri=rpi_ip, sdr=my_sdr)

    # Initialize both ADAR1000s, set gains to max, and all phases to 0
    my_phaser.configure(device_mode="rx")   # Receive device mode
    my_phaser.load_gain_cal()
    my_phaser.load_phase_cal()
    for i in range(0, 8):
        my_phaser.set_chan_phase(i, 0) # 0 degrees for straight ahead

    gain_list = [8, 34, 84, 127, 127, 84, 34, 8]  # Blackman taper - helps with side lobes
    for i in range(0, len(gain_list)):
        my_phaser.set_chan_gain(i, gain_list[i], apply_cal=True)

    # Setup Raspberry Pi GPIO states
    my_phaser._gpios.gpio_tx_sw = 0  # 0 = TX_OUT_2, 1 = TX_OUT_1
    # v 1=Use onboard PLL/LO source  (0=disable PLL and VCO, and set switch to use external LO input) v
    my_phaser._gpios.gpio_vctrl_1 = 1
    # v 1=Send LO to transmit circuitry  (0=disable Tx path, and send LO to LO_OUT) v
    my_phaser._gpios.gpio_vctrl_2 = 1

    # Configure SDR Rx
    my_sdr.sample_rate = int(sample_rate)
    my_sdr.rx_lo = int(center_freq)  # set this to output_freq - (the freq of the HB100)
    my_sdr.rx_enabled_channels = [0, 1]  # enable Rx1 (voltage0) and Rx2 (voltage1)
    my_sdr.gain_control_mode_chan0 = "manual"  # manual or slow_attack
    my_sdr.gain_control_mode_chan1 = "manual"  # manual or slow_attack
    my_sdr.rx_hardwaregain_chan0 = int(rx_gain)  # range: (-3, 70)
    my_sdr.rx_hardwaregain_chan1 = int(rx_gain)  # range: (-3, 70)

    # Configure SDR Tx
    my_sdr.tx_lo = int(center_freq)
    my_sdr.tx_enabled_channels = [0, 1]
    # v Must set cyclic buffer to true for the tdd burst mode.  Otherwise Tx will turn on and off randomly v
    my_sdr.tx_cyclic_buffer = True
    # v Sets attenuation, using channel 1 with 0 db of attenuation v
    my_sdr.tx_hardwaregain_chan0 = -88  # range: [0, -88]
    my_sdr.tx_hardwaregain_chan1 = -0   # range: [0, -88]

    my_sdr.output_freq = output_freq
    my_sdr.signal_freq = signal_freq
    my_sdr.num_chirps = num_chirps
    my_sdr.bw = default_chirp_bw
    my_sdr.ramp_time = ramp_time

    '''
    Configuration specific to chirp synchronization (**)
    '''
    # Configure the ADF4159 Rampling PLL
    vco_freq = int(my_sdr.output_freq + my_sdr.signal_freq + center_freq)
    BW = default_chirp_bw
    num_steps = int(my_sdr.ramp_time)    # works best with 1 step per microsecond
    my_phaser.frequency = int(vco_freq / 4)
    my_phaser.freq_dev_range = int(BW / 4)      # total freq deviation of the complete freq ramp in Hz
    my_phaser.freq_dev_step = int((BW / 4) / num_steps)  # This is fDEV, in Hz.  Can be positive or negative
    my_phaser.freq_dev_time = int(my_sdr.ramp_time)  # total time (microseconds) of the complete frequency ramp
    print("requested freq dev time = ", my_sdr.ramp_time)
    # v 12 bit delay word.  4095*PFD = 40.95 us.  For sawtooth ramps, this is also the length of the Ramp_complete signal v
    my_phaser.delay_word = 4095
    my_phaser.delay_clk = "PFD"  # can be 'PFD' or 'PFD*CLK1'
    my_phaser.delay_start_en = 0  # delay start
    my_phaser.ramp_delay_en = 0  # delay between ramps.
    my_phaser.trig_delay_en = 0  # triangle delay
    # ramp_mode can be:  "disabled", "continuous_sawtooth", "continuous_triangular",
    # "single_sawtooth_burst", "single_ramp_burst"
    my_phaser.ramp_mode = "single_sawtooth_burst"  # **
    my_phaser.sing_ful_tri = 0  # full triangle enable/disable -- this is used with the single_ramp_burst mode
    my_phaser.tx_trig_en = 1  # ** start a ramp with TXdata **
    my_phaser.enable = 0  # 0 = PLL enable.  Write this last to update all the registers

    ''' ** TDD controller is necessary for chirp synchronization ** '''
    # Configure TDD controller - programming inside Pluto to control timing
    sdr_pins = adi.one_bit_adc_dac(sdr_ip)
    # If set to True, this enables external capture triggering using the L24N GPIO on the Pluto.
    # If set to False, an internal trigger pulse will be generated every second.
    sdr_pins.gpio_tdd_ext_sync = True
    tdd = adi.tddn(sdr_ip)
    sdr_pins.gpio_phaser_enable = True
    tdd.enable = False         # disable TDD to configure the registers
    tdd.sync_external = True
    tdd.startup_delay_ms = 0
    PRI_ms = my_sdr.ramp_time/1e3 + 1.0  # each chirp is spaced this far apart
    tdd.frame_length_ms = PRI_ms
    tdd.burst_count = my_sdr.num_chirps       # number of chirps in one continuous receive buffer

    # Channel 0 controls timing of TXdata outputs
    # Channel 1 controls start timing of Pluto receive buffer
    # Channel 2 controls transmit buffer timing
    tdd.channel[0].enable = True
    tdd.channel[0].polarity = False
    tdd.channel[0].on_raw = 0
    tdd.channel[0].off_raw = 10
    tdd.channel[1].enable = True
    tdd.channel[1].polarity = False
    tdd.channel[1].on_raw = 0
    tdd.channel[1].off_raw = 10
    tdd.channel[2].enable = True
    tdd.channel[2].polarity = False
    tdd.channel[2].on_raw = 0
    tdd.channel[2].off_raw = 10
    tdd.enable = True
    
    ### End chirp sync specific configuration ###
    
    ''' 
    Ramp Sampling and FFT Sizing for Frequency Chirp Processing
    '''
    # From start of each ramp, how many "good" points do we want?
    # For best freq linearity, stay away from the start of the ramps
    ramp_time_s = my_sdr.ramp_time / 1e6
    begin_offset_time = 0.10 * ramp_time_s   # time in seconds
    print("actual freq dev time = ", my_sdr.ramp_time)
    global good_ramp_samples
    good_ramp_samples = int((ramp_time_s-begin_offset_time) * my_sdr.sample_rate)
    start_offset_time = tdd.channel[0].on_ms/1e3 + begin_offset_time
    global start_offset_samples
    start_offset_samples = int(start_offset_time * my_sdr.sample_rate)

    # size the fft for the number of ramp data points
    power = 8
    global fft_size, num_samples_frame
    fft_size = int(2**power)
    num_samples_frame = int(tdd.frame_length_ms/1000*my_sdr.sample_rate)
    while num_samples_frame > fft_size:
        power = power+1
        fft_size = int(2**power)
        if power == 18:
            break
    print("fft_size =", fft_size)

    # Pluto receive buffer size needs to be greater than total time for all chirps
    total_time = tdd.frame_length_ms * my_sdr.num_chirps   # time in ms
    print("Total Time for all Chirps:  ", total_time, "ms")
    buffer_time = 0
    power = 6
    while total_time > buffer_time:
        power = power+1
        buffer_size = int(2**power)
        buffer_time = buffer_size/my_sdr.sample_rate*1000   # buffer time in ms
        if power == 6:
            break     # max pluto buffer size is 2**23, but for tdd burst mode, set to 2**22
    print("buffer_size:", buffer_size)
    my_sdr.rx_buffer_size = buffer_size
    print("buffer_time:", buffer_time, " ms")

    # Calculate and print summary of ramp parameters
    c = 3e8
    wavelength = c / my_sdr.output_freq
    freq = np.linspace(-my_sdr.sample_rate / 2, my_sdr.sample_rate / 2, int(fft_size))
    slope = BW / ramp_time_s
    dist = (freq - my_sdr.signal_freq) * c / (2 * slope)
    plot_dist = False
    print(
        """
    CONFIG:
    Sample rate: {sample_rate}MHz
    Num samples: 2^{Nlog2}
    Bandwidth: {BW}MHz
    Ramp time: {ramp_time}ms
    Output frequency: {output_freq}MHz
    IF: {signal_freq}kHz
    """.format(
            sample_rate=my_sdr.sample_rate / 1e6,
            Nlog2=int(np.log2(my_sdr.rx_buffer_size)),
            BW=BW / 1e6,
            ramp_time=my_sdr.ramp_time / 1e3,
            output_freq=my_sdr.output_freq / 1e6,
            signal_freq=my_sdr.signal_freq / 1e3,
        )
    )

    '''
    Create sine waveform for Pluto transmitter
    '''
    N = int(2**18)
    fc = int(my_sdr.signal_freq)
    ts = 1 / float(my_sdr.sample_rate)
    t = np.arange(0, N * ts, ts)
    i = np.cos(2 * np.pi * t * fc) * 2 ** 14
    q = np.sin(2 * np.pi * t * fc) * 2 ** 14
    iq = 1 * (i + 1j * q)

    # transmit data from Pluto
    my_sdr._ctx.set_timeout(30000)
    my_sdr._rx_init_channels()
    my_sdr.tx([iq, iq])  # only send data to the 2nd channel (that's all we need)
    
    plutoGui.log_message("Done setting up Pluto")
    

def collect_data(plutoGui, distance, step_count, speed, wait, comment):
    plutoGui.log_message("Starting data collection")
    
    # Create array to share with load and update
    # 80 x 300 array with complex type
    rows, cols, pulses = 32768, distance, 1
    store = np.zeros((rows, cols, pulses), dtype=complex)
    global p2p_slow_time, p2p_cross
    p2p_slow_time = []
    p2p_cross = []
    
    for i in range(distance):
        for i_pulse in range(pulses):
            store = update_func.update(store, i, i_pulse)
        p2p_slow_time.append(datetime.now().isoformat())
        p2p_cross.append(i*step_count)
        time.sleep(0.5)
        if motors.motorsSetUp:
            motors.step_once(step_count, speed)
        else:
            plutoGui.log_message("ERROR: Motors are not set up. Click 'Setup motors' and try again")
            break
        plutoGui.log_message(f"{i+1}/{distance} steps completed")
        time.sleep(wait)

    update_func.load(store, comment)
    
    plutoGui.log_message("Done collecting data")
    
def collect_continuous_data(plutoGui, step_count, speed, comment):
    cross_pos_count = abs(int(step_count/30))
    plutoGui.log_message(f"Starting continuous data collection with {cross_pos_count} cross positions")
    
    # Create array to share with load and update
    # 80 x 300 array with complex type
    rows, cols, pulses = 32768, cross_pos_count, 1
    store = np.zeros((rows, cols, pulses), dtype=complex)
    global p2p_slow_time, p2p_cross
    p2p_slow_time = []
    p2p_cross = []

    if motors.motorsSetUp:
        motors.step_once(step_count, speed)
    else:
        plutoGui.log_message("ERROR: Motors are not set up. Click 'Setup motors' and try again")

    for i in range(cross_pos_count):
        for i_pulse in range(pulses):
            store = update_func.update(store, i, i_pulse)
        p2p_slow_time.append(datetime.now().isoformat())
        p2p_cross.append(i*step_count)
        plutoGui.log_message(f"{i+1}/{cross_pos_count} cross position collections completed")
        time.sleep(30/(speed/60))

    update_func.load(store, comment)

    plutoGui.log_message("Done collecting data")
    
