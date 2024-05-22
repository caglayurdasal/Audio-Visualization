import cv2
import cvui
import numpy as np
import speech_recognition as sr
import audioop
import threading

# Constants for the progress bar
WINDOW_NAME = "Energy Threshold & Microphone Audio Levels"
BAR_WIDTH = 500
BAR_HEIGHT = 20
BAR_X = 100
BAR_Y = 100

program_running = True
r = sr.Recognizer()


def calculate_rms(audio_data):
    audio_np = np.frombuffer(audio_data.frame_data, dtype=np.int16)
    if len(audio_np) == 0:
        return 0.0  # Return 0 if no audio data is available

    rms = np.sqrt(np.mean(np.square(audio_np)))
    return rms if not np.isnan(rms) else 0.0  # Return 0 if rms is NaN


def draw_audio_bar(frame, rms):
    # Scale RMS to fit within the BAR_HEIGHT
    # Returns BAR_HEIGHT if calculated height exceeds BAR_HEIGHT
    bar_width = int(min(rms / 100, BAR_WIDTH))
    border_color = 0xC0C0C0
    color = 0x008000  # Default bar color is green
    if rms > 30000:
        color = 0xFF0000  # Change to red if audio level is high

    # Outline of the audio bar
    cvui.rect(frame, BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT, border_color)
    # Draw the progress
    cvui.rect(frame, BAR_X, BAR_Y, bar_width, BAR_HEIGHT, border_color, color)


def speech_recognition_thread(r, source, rms_data):
    global program_running
    while program_running:
        try:
            audio_data = r.listen(source, phrase_time_limit=0.5)
            current_rms = audioop.rms(audio_data.frame_data, 2)
            rms_data.append(current_rms)  # add current rms value to list
            if len(rms_data) > 1:
                rms_data.pop(0)  # current rms value will be the only value in the list
            print(f"rms={int(current_rms)}")

        except KeyboardInterrupt:
            print("Program terminated.\n")
            break


def user_interface_thread(r, frame, rms_data):
    global program_running
    energy_threshold = [
        r.energy_threshold
    ]  # cvui.trackbar() expects aValue parameter to be a mutable object
    cvui.init(WINDOW_NAME)

    while program_running:
        try:
            frame[:] = (49, 52, 49)
            if rms_data:
                rms = rms_data[0]
                draw_audio_bar(frame, rms)

            # Draw the trackbar and update the energy threshold
            if cvui.trackbar(frame, 50, 40, 900, energy_threshold, 100.0, 10000.0):
                r.energy_threshold = energy_threshold[0]

            print(f"energy_threshold={round(r.energy_threshold,1)}")

            # Update components
            cvui.update()
            cv2.imshow(WINDOW_NAME, frame)

            if cv2.waitKey(20) == 27:
                print("ESC pressed.")
                program_running = False
                break

        except KeyboardInterrupt:
            print("Program terminated.\n")
            break

    cv2.destroyAllWindows()


def main():
    r.dynamic_energy_threshold = False
    rms_data = []  # rms values
    frame = np.zeros((200, 1000, 3), np.uint8)  # Shared frame

    with sr.Microphone() as source:  # Initialize the microphone once
        # Create threads for speech recognition and user interface
        sr_thread = threading.Thread(
            target=speech_recognition_thread, args=(r, source, rms_data)
        )
        ui_thread = threading.Thread(
            target=user_interface_thread, args=(r, frame, rms_data)
        )

        # Start the threads
        sr_thread.start()
        ui_thread.start()

        # Wait for threads to finish
        sr_thread.join()
        ui_thread.join()


if __name__ == "__main__":
    main()
