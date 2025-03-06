# -*- coding: utf-8 -*-
"""AI Module

This module defines an AI class that integrates OpenAI's GPT-4o for text generation,
ElevenLabs for text-to-speech, and SpeechRecognition for speech input

File:
    ai/ai.py

Classes:
    AI: Class for handling API calls
"""

import os
from typing import Any, Tuple

import elevenlabs
import openai
import speech_recognition as sr
from playsound3 import playsound


class AI:
    """AI Object.

    Attributes:
        __model (OpenAI):  GPT-4o API client.
        __voice_model (ElevenLabs): ElevenLabs API client for text-to-speech.

    Methods:
        text_prompt(prompt: str) -> str | None: Generates a response based on the given prompt.
        generate_response_voice_backup(prompt: str) -> None: Generates an audio file using
                                                             OpenAI's text-to-speech.
        
    """
    def __init__(self) -> None:
        api_key_gpt = os.getenv("OPENAI_API_KEY")
        self.__model = openai.OpenAI(api_key=api_key_gpt)

        api_key_eleven = os.getenv("ELEVEN_LABS_API_KEY")
        self.__voice_model = elevenlabs.ElevenLabs(api_key=api_key_eleven)

    def text_prompt(self, prompt: str) -> str | None:
        """Generates a response based on the given prompt.

        This method uses the gpt-4o model to generate a response
        replying to the given text prompt.

        Args:
            prompt (str): The text prompt.

        Returns:
            str | None: The generated response | None if there was an Error.
        """
        response = self.__model.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        return response.choices[0].message.content

    def speak(self) -> Tuple[Any, float] | None:
        # TODO: This does not need to be instance method, move to utils
        recognizer = sr.Recognizer()
        while True:
            try:
                with sr.Microphone() as source2:
                    recognizer.adjust_for_ambient_noise(source2, duration=1)
                    audio_2 = recognizer.listen(
                        source2, timeout=10, phrase_time_limit=30
                    )

                    return recognizer.recognize_amazon(audio_2)

            except sr.UnknownValueError:
                print("Error")

    def generate_response_voice_backup(self, prompt: str) -> None:
        """Generates an audio file using OpenAI's text-to-speech.

        This method converts the given text prompt into speech using OpenAI's
        TTS and saves it as a .wav file.

        Args:
            prompt (str): The text to synthesize into speech.
        """

        response = self.__model.audio.speech.create(
            model="tts-1", voice="nova", input=prompt
        )

        audio_path = os.path.abspath("answer.wav")

        with open(file=audio_path, mode="wb") as f:
            f.write(response.content)

        try:
            playsound(audio_path)
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)
