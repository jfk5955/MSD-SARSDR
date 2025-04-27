# Data Collection Setup and Instructions

## What You Need
1. Laptop with terminal that supports X11 forwarding  
   (e.g., XQuartz for Mac, MobaXterm for Windows)
2. Data collection platform

## Setup Instructions

1. Plug **the Pluto** (bottom board) into one of the USB 2.0 ports (grey port) on the Raspberry Pi (top board) using the USB A to micro USB cable.
2. Plug **the USB-C power cable** into the Phaser receiver (middle board) to power all three boards.
3. Plug **the USB A cable from the motor controller** into one of the USB 2.0 ports on the Pi.
4. Screw **the horn antenna** into the port next to the already occupied port on the Phaser receiver.
5. After about a minute, the Pi should be fully booted up.  
   Connect to its Wi-Fi hotspot "**pluto**" from your laptop.  
   **Password:** `analogpluto`
6. Once connected, run the following command in the terminal to connect to the Pi:

   ```bash
   ssh -X analog@10.42.0.1
   ```
   **Password:** `analog`

   **NOTE:**
   The Pi defaults to starting a WiFi hotspot since you might lose connection to RIT WiFi on a roof top. But if you want to use RIT WiFi then you can connect to it with this command (assuming RIT IT didn't remove this profile since it's under a graduating students account):

   ```bash
   ssh -X analog@pluto.student.rit.edu
   ```
   
8. The Pi has two repositories downloaded:
   - **PhaserRadarLabs:** contains all the John Kraft labs associated with the Phaser.
   - **MSD-SARSDR (this repo):** contains all the code needed to operate the data collection platform.
   
   Navigate to this repo:
   ```bash
   cd MSD-SARSDR
   ```
9. Start the GUI to control the track-mounted platform:

   ```bash
   python3 main.py
   ```
   **NOTE:**  
   The GUI is running on the Pi, not your laptop, so you must maintain your connection to the Pi to avoid data collection failure.
10. In the GUI:
   - Press **"Setup Motors"** and **"Setup Radar"** before attempting data collection.
   - Once completed, **completion messages** will show up in the log box on the right.
   - If the motors fail to connect (and you've completed step 3), try changing the **port path** number from `0` to `1` below the log box.  
     This port path can change if extra devices are plugged into the Pi.

---

## Data Collection Profiles

You can now drive the motors and collect data using either of the two profiles:

### 1. Stepwise Collection
- The platform will complete **steps** across the track, collecting data **between** steps.
- Adjustable in GUI:
  - Number of steps
  - Distance per step
  - Wait time between transmissions
- **Important:**  
  Since the motors do not send confirmation upon completing a step, setting the **wait time** correctly is crucial.  
  A **hardcoded 0.5-second** wait time after each transmission ensures enough time for transmit/receive completion.

### 2. Continuous Collection
- The radar transmits and receives **while the motors are moving**.
- A cross-position collection is done every **30 mm** (hardcoded in `radar.py`, **line 256**).
- **Notes:**
  - The timing based on motor speed is not perfect.  
    Data collection may finish before the platform reaches the end of the track, indicating that the platform is moving slower than calculated.
  - **Calibration** may be needed in the motor setup code to fix this.
- The number of pulses per cross-position/step is hardcoded in `radar.py`, **line 261**.

---

## Important GUI Features

### Kill Button
- Stops sending any more commands to the motors and radar.
- **Warning:**  
  If clicked during data collection, **no data** will be saved.
- Used primarily to **prevent accidentally running the platform off the track**.
- **Caution:**  
  Motors will continue moving for the remaining distance of the last step command sent to the motors.
  Example: If "# of mm/step" is set to **10,000 mm** (10 meters) and the "# of steps is set to 1", the motors will **not stop** until they complete the 10 meters or unless you **switch off the power** to the motor controller.

---

## Motor Calibration

- Motors have only been calibrated **once** at the beginning of the project.
- **Recalibration is recommended.**
- To recalibrate:
  - Adjust `defaultStepSize` in `motors.py` (**line 5**).
  - "defaultStepSize" = number of motor steps needed to move 1 mm.
- Calibration method:
  - Tape a measuring tape to the track
  - Tell motors to move **100 mm**.
  - Adjust the "defaultStepSize" based on overshoot or undershoot relative to 100 mm.

---

## Offloading Data

- Once a data collection is complete, a message will appear in the terminal (not in the GUI log box) indicating the saved file name, e.g.,

  ```
  data_mat_2025-04-24_13-52-28.mat
  ```

- To download the file from the Pi to your laptop:

  ```bash
  scp analog@10.42.0.1:/home/analog/MSD-SARSDR/data/<file name> /<path to local destination>/
  ```

---
