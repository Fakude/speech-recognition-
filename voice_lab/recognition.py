"""Audio capture and cloud recognition adapter.

The third-party dependencies are imported only when audio mode is selected so
typed demonstration mode remains usable in a fresh Python installation.
"""

from __future__ import annotations


class RecognitionError(RuntimeError):
    """A friendly, actionable speech-recognition error."""


def recognise_once(language: str, calibration_seconds: float, timeout: float | None, phrase_time_limit: float | None) -> str:
    try:
        import speech_recognition as sr
    except ImportError as error:
        raise RecognitionError("Audio mode needs SpeechRecognition and PyAudio. Run: pip install -r requirements.txt") from error

    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as microphone:
            print(f"Calibrating microphone for {calibration_seconds:.1f} seconds…")
            recognizer.adjust_for_ambient_noise(microphone, duration=calibration_seconds)
            print("Listening… speak now.")
            audio = recognizer.listen(microphone, timeout=timeout, phrase_time_limit=phrase_time_limit)
        return recognizer.recognize_google(audio, language=language)
    except sr.WaitTimeoutError as error:
        raise RecognitionError("No speech was detected before the timeout.") from error
    except sr.UnknownValueError as error:
        raise RecognitionError("I could not understand that audio. Try a quieter space or speak closer to the microphone.") from error
    except sr.RequestError as error:
        raise RecognitionError(f"The speech service could not be reached: {error}") from error
    except OSError as error:
        raise RecognitionError("No working microphone was found. Check your device permissions and audio input.") from error


def speak(text: str) -> None:
    """Read a transcript aloud if pyttsx3 is installed."""
    try:
        import pyttsx3
    except ImportError as error:
        raise RecognitionError("Speech playback needs pyttsx3. Run: pip install -r requirements.txt") from error
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
