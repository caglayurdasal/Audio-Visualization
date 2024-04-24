# Audio Visualization

This project provides real-time visualization of microphone audio levels using OpenCV and the SpeechRecognition library. It includes two main scripts:

1. **Microphone Audio Levels Visualization**
   - File: `microphone_audio_levels.py`
   - Description: This script captures audio from the microphone, calculates the Root Mean Square (RMS) to visualize the audio level, and displays it in a graphical user interface (GUI) window using OpenCV. The user can see the audio levels represented by a progress bar and can quit the application by clicking the "Quit" button or pressing the ESC key.
   - Dependencies: `opencv-python`, `speechrecognition`, `cvui`, `numpy`

2. **Energy Threshold & Microphone Audio Levels Visualization**
   - File: `energy_threshold_audio_levels.py`
   - Description: This script provides similar functionality to the previous script but includes a slider for adjusting the energy threshold parameter used in the SpeechRecognition library. The user can adjust the energy threshold using the slider, visualize the microphone audio levels, and quit the application using the "Quit" button or ESC key.
   - Dependencies: `opencv-python`, `speechrecognition`, `cvui`, `numpy`

## Installation

1. Clone the repository:
   ```bash
   git clone git@github.com:caglayurdasal/Audio-Visualization.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the desired script:
   ```bash
   python3 microphone_audio_levels.py
   ```
   or
   ```bash
   python3 energy_threshold_audio_levels.py
   ```

2. Adjust settings and interact with the graphical user interface as needed.

3. To quit the application, click the "Quit" button or press the ESC key.
