# Audio Visualization

This project provides real-time visualization of microphone audio levels using OpenCV and the SpeechRecognition library. It includes two main scripts:

1. **Microphone Audio Levels Visualization**
   - File: `visualize_energy_level.py`
   - Description: This script captures audio from the microphone, calculates the Root Mean Square (RMS) to visualize the audio level, and displays it in a graphical user interface (GUI) window using OpenCV. The user can see the audio levels represented by a progress bar and can quit the application by clicking the "Quit" button or pressing the ESC key.
   - Dependencies: `opencv-python`, `speechrecognition`, `cvui`, `numpy`

2. **Energy Threshold & Microphone Audio Levels Visualization**
   - File: `adjust_threshold.py`
   - Description: This script provides similar functionality to the previous script but includes a slider for adjusting the energy threshold parameter used in the SpeechRecognition library. The user can adjust the energy threshold using the slider, visualize the microphone audio levels, and quit the application using the "Quit" button or ESC key.
   - Dependencies: `opencv-python`, `speechrecognition`, `cvui`, `numpy`

## Installation
Python Version Requirement:
This project requires Python 3.10.

0. Install OS-level dependencies:
   - Linux Mint (required for compiling the pyaudio module):
   ```bash
   sudo apt install portaudio19-dev
   ```   
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
   python3 visualize_energy_level.py
   ```
   or
   ```bash
   python3 adjust_threshold.py
   ```
2. Adjust energy threshold levels as needed using GUI.

3. To quit the application, press the ESC key.

## References
0. About ALSA warnings: 
- https://blog.yjl.im/2012/11/pyaudio-portaudio-and-alsa-messages.html
1. speech_recognition library reference for Recognizer class and energy threshold:
- https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst#recognizer---recognizer
2. Getting microphone input as source
- https://github.com/Uberi/speech_recognition/blob/master/examples/audio_transcribe.py
3. Calculating the volume of the input with root mean square(rms):
- https://github.com/jiaaro/pydub/blob/master/pydub/pyaudioop.py#L142
- https://stackoverflow.com/questions/9763471/audioop-rms-why-does-it-differ-from-normal-rms
- https://docs.python.org/3/library/audioop.html#audioop.rms
4. cvui/opencv library reference for trackbar:
- https://github.com/Dovyski/cvui/blob/master/example/src/trackbar/trackbar.py
- https://docs.opencv.org/4.x/da/d6a/tutorial_trackbar.html

      
   
