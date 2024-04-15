import cv2
import cvui
import numpy as np
import speech_recognition as sr

WINDOW_NAME = "Energy Threshold"


def calculate_rms(audio_data):
    audio_np = np.frombuffer(audio_data.frame_data, dtype=np.int16)
    rms = np.sqrt(np.mean(np.square(audio_np)))
    return rms


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

                # Draw the trackbar and update the energy threshold
                if cvui.trackbar(frame, 10, 40, 500, energy_threshold, 100.0, 4000.0):
                    r.energy_threshold = energy_threshold[0]

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
