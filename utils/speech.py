from typing import Any, Tuple

import speech_recognition as sr


def speak() -> Tuple[Any, float] | None:
    """Captures microphone input and returns the recognized speech

    This function captures audio input from the microphone. It then uses a speech recognition
    library to recognize the speech and return the recognized text.

    Returns:
        Tuple[Any, float] | None: A tuple containing the recognized speech (Any) and the confidence score (float)
                                  of the recognition. Returns None if no speech is recognized.
    """
    recognizer = sr.Recognizer()
    while True:
        try:
            with sr.Microphone() as source2:
                recognizer.adjust_for_ambient_noise(source2, duration=1)
                audio_2 = recognizer.listen(source2, timeout=10, phrase_time_limit=30)

                return recognizer.recognize_google(audio_2)

        except sr.UnknownValueError:
            print("Error")
