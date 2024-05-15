import cv2
import cvui
import numpy as np
import speech_recognition as sr
import audioop
import threading

# Constants for the progress bar
WINDOW_NAME = "Energy Threshold & Microphone Audio Levels"
BAR_WIDTH = 20
BAR_HEIGHT = 500
BAR_X = 100
BAR_Y = 50


def calculate_rms(audio_data):
    audio_np = np.frombuffer(audio_data.frame_data, dtype=np.int16)
    if len(audio_np) == 0:
        return 0.0  # Return 0 if no audio data is available
    rms = np.sqrt(np.mean(np.square(audio_np)))
    return rms if not np.isnan(rms) else 0.0  # Return 0 if rms is NaN


def draw_audio_bar(frame, rms):
    # Scale RMS to fit within the BAR_HEIGHT
    # Returns BAR_HEIGHT if calculated height exceeds BAR_HEIGHT
    bar_height = int(min(rms / 100, BAR_HEIGHT))
    border_color = 0xC0C0C0  # Silver
    color = 0x008000  # Default bar color is green
    if rms > 30000:
        color = 0xFF0000  # Change to red if audio level is high
    # Outline of the audio bar
    cvui.rect(frame, BAR_Y, BAR_X, BAR_HEIGHT, BAR_WIDTH, border_color)
    # Draw the progress
    cvui.rect(frame, BAR_Y, BAR_X, bar_height, BAR_WIDTH, border_color, color)
    print(f"bar_height={bar_height}")


def change_threshold(tValue):
    r = sr.Recognizer()
    r.energy_threshold = tValue


def speech_recognition_thread(r, source, energy_threshold):
    global frame
    while True:
        try:
            audio_data = r.listen(source, phrase_time_limit=0.5)
            rms = audioop.rms(audio_data.frame_data, 2)
            print(f"rms={int(rms)}")
            draw_audio_bar(frame, rms)
        except KeyboardInterrupt:
            print("Program terminated.\n")
            break


def user_interface_thread(energy_threshold, frame, r):
    while True:
        frame[:] = (49, 52, 49)
        if cvui.trackbar(frame, 50, 40, 900, energy_threshold, 100.0, 10000.0):
            r.energy_threshold = energy_threshold[0]
        print(f"energy_threshold={round(r.energy_threshold, 1)}")
        cvui.update()
        cv2.imshow(WINDOW_NAME, frame)
        if cv2.waitKey(20) == 27:
            print("ESC pressed.")
            break
    cv2.destroyAllWindows()


def main():
    r = sr.Recognizer()
    energy_threshold = [r.energy_threshold]  # cvui.trackbar() expects aValue parameter to be a mutable object
    r.dynamic_energy_threshold = False
    cvui.init(WINDOW_NAME)
    global frame
    frame = np.zeros((200, 1000, 3), np.uint8)

    with sr.Microphone() as source:
        # Create threads for speech recognition and user interface
        sr_thread_instance = threading.Thread(
            target=speech_recognition_thread, args=(r, source, energy_threshold)
        )
        ui_thread_instance = threading.Thread(
            target=user_interface_thread, args=(energy_threshold, frame, r)
        )

        # Start the threads
        sr_thread_instance.start()
        ui_thread_instance.start()

        # Wait for threads to finish
        sr_thread_instance.join()
        ui_thread_instance.join()


if __name__ == "__main__":
    main()
