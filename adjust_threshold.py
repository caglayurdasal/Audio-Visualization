import cv2
import cvui
import numpy as np
import speech_recognition as sr

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
    return rms if not np.isnan(rms) else 0.0  # Return 0 if rms is nan


def draw_audio_bar(frame, rms):
    # Scale RMS to fit within the BAR_HEIGHT
    # Returns BAR_HEIGHT if calculated height exceeds BAR_HEIGHT
    bar_height = int(min(rms / 50 * BAR_HEIGHT, BAR_HEIGHT))
    border_color = 0xC0C0C0  # Silver
    color = 0x008000  # Default bar color is green
    if rms > 15000:
        color = 0xFF0000  # Change to red if audio level is high

    # Outline of the audio bar
    cvui.rect(frame, BAR_Y, BAR_X, BAR_HEIGHT, BAR_WIDTH, border_color)
    # Draw the progress
    cvui.rect(frame, BAR_Y, BAR_X, bar_height, BAR_WIDTH, border_color, color)


def change_threshold(tValue):
    r = sr.Recognizer()
    r.energy_threshold = tValue


def main():
    r = sr.Recognizer()
    energy_threshold = [
        r.energy_threshold
    ]  # cvui.trackbar() expects aValue parameter to be a mutable object
    r.dynamic_energy_threshold = False
    cvui.init(WINDOW_NAME)
    frame = np.zeros((200, 600, 3), np.uint8)

    with sr.Microphone() as source:
        while True:
            try:
                frame[:] = (49, 52, 49)
                audio_data = r.listen(source, phrase_time_limit=0.5)
                rms = calculate_rms(audio_data)

                draw_audio_bar(frame, rms)
                print(f"rms: {str(rms)}")

                # Draw the trackbar and update the energy threshold
                # if cvui.trackbar(frame, 50, 40, 500, energy_threshold, 100.0, 4000.0):
                #     r.energy_threshold = energy_threshold[0]
                cv2.createTrackbar("slider", WINDOW_NAME, 100, 4000, change_threshold)

                # Update components
                cvui.update()
                cv2.imshow(WINDOW_NAME, frame)

                if cv2.waitKey(20) == 27:
                    print("ESC pressed.")
                    break

            except KeyboardInterrupt:
                print("Program terminated.\n")
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
