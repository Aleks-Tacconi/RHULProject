# -*- coding: utf-8 -*-
"""AI Module

This module defines an AI class that integrates OpenAI's GPT-4o for text generation,
ElevenLabs for text-to-speech

File:
    ai/ai.py

Classes:
    AI: Class for handling API calls
"""

import os
import threading

import elevenlabs
import openai
from playsound3 import playsound


class AI:
    """AI Object.

    Attributes:
        __model (OpenAI):  GPT-4o API client.
        __voice_model (ElevenLabs): ElevenLabs API client for text-to-speech.
        __prompt (str): custom instructions on how to respond

    Methods:
        text_prompt(prompt: str) -> str | None: Generates a response based on the given prompt.
        listen_and_respond() -> None: Captures voice input through microphone and responds by playing an
                                      audio file
        __listen_and_respond() -> None: Handles the logic of capturing and responding this function is ran in a 
                                        separate Thread.
        __generate_response_voice_backup(prompt: str) -> None: Generates an audio file using
                                                             OpenAI's text-to-speech.

    """

    def __init__(self) -> None:
        api_key_gpt = os.environ.get("OPENAI_API_KEY")
        self.__model = openai.OpenAI(api_key=api_key_gpt)

        api_key_eleven = os.getenv("ELEVEN_LABS_API_KEY")
        self.__voice_model = elevenlabs.ElevenLabs(api_key=api_key_eleven)

        self.__prompt = "Must refer to me as the chosen one. 30 Word limit. You are a game assistant meant to help the player: "

    def listen_and_respond(self) -> None:
        """Captures voice input through microphone and responds by playing an audio file"""
        threading.Thread(target=self.__listen_and_respond).start()

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

    def __listen_and_respond(self) -> None:
        """Captures voice input through microphone and responds by playing an audio file"""

        #speech = speak()
        #print(speech)
        # speech = "Hello"
        #response = self.text_prompt(self.__prompt + speech)
        #print(response)

        #if response is not None:
            #self.__generate_response_voice(response)

    def generate_response_voice(self, prompt: str) -> None:
        """Generates an audio file using OpenAI's text-to-speech."""
        threading.Thread(target=self.__generate_response_voice, args=(prompt,)).start()

    def __generate_response_voice(self, prompt: str) -> None:
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
