import cv2
import numpy as np
import speech_recognition as sr
import cvui

# Constants for the progress bar
WINDOW_NAME = "Microphone Audio Levels"
BAR_WIDTH = 20
BAR_HEIGHT = 500
BAR_X = 50
BAR_Y = 50

# Constants for the slider
SLIDER_X = 400
SLIDER_Y = 50
SLIDER_WIDTH = 20
SLIDER_HEIGHT = 200
SLIDER_MIN = 500
SLIDER_MAX = 4000
slider_value = SLIDER_MIN

def calculate_rms(audio_data):
    """
    Calculates Root Mean Square (RMS) to quantify the
    average amplitude of audio signal over time.
    """
    audio_np = np.frombuffer(audio_data.frame_data, dtype=np.int16).astype(np.float32)
    rms = np.sqrt(np.mean(np.square(audio_np)))
    return rms


def draw_audio_bar(frame, rms):
    # Scale RMS to fit within the BAR_HEIGHT
    # Returns BAR_HEIGHT if calculated height exceeds BAR_HEIGHT
    bar_height = int(min(rms / 5500 * BAR_HEIGHT, BAR_HEIGHT))
    border_color = 0xC0C0C0  # Silver
    color = 0x008000  # Default bar color is green
    if rms > 5000:
        color = 0xFF0000  # Change to red if audio level is high

    # Outline of the audio bar
    cvui.rect(frame, BAR_Y, BAR_X, BAR_HEIGHT, BAR_WIDTH, border_color)
    # Draw the progress
    cvui.rect(frame, BAR_Y, BAR_X, bar_height, BAR_WIDTH, border_color, color)


def main():
    # Create a new Recognizer instance
    r = sr.Recognizer()

    # Create a new Microphone instance and use it as source in context manager
    with sr.Microphone() as source:
        print("Adjusting for ambient noise.")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Mic listening:")

        # OpenCV setup
        frame = np.zeros((300, 600, 3), np.uint8)
        cvui.init(WINDOW_NAME)

        while True:
            try:
                # Listen for audio
                audio_data = r.listen(source, phrase_time_limit=0.5)

                # Calculate RMS to visualize audio level
                rms = calculate_rms(audio_data)

                # Clear the frame
                frame[:] = (49, 52, 49)

                # Check for "Quit" button press to exit
                button = cvui.button(frame, 280, 100, "Quit")
                if button:
                    print("Quit button pressed")
                    break
                cvui.update()

                # Draw the audio bar
                draw_audio_bar(frame, rms)

                # Add a slider for adjusting energy threshold
                cvui.trackbar(frame, SLIDER_X, SLIDER_Y, SLIDER_WIDTH, SLIDER_HEIGHT, slider_value, SLIDER_MIN, SLIDER_MAX)

                # Update energy threshold based on slider value
                r.energy_threshold = slider_value

                # Show the content
                cvui.imshow(WINDOW_NAME, frame)

                # Check for ESC key press to exit
                if cv2.waitKey(20) == 27:
                    print("ESC pressed.")
                    break

            except KeyboardInterrupt:
                print("\n\nProgram terminated.")
                break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
