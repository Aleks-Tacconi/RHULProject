import os
import base64
import tempfile

from elevenlabs import ElevenLabs
import openai
import speech_recognition as sr
from playsound3 import playsound

class AI:
    def __init__(self) -> None:
        api_key_gpt = os.getenv("OPENAI_API_KEY")
        api_key_eleven = os.getenv("ELEVEN_LABS_API_KEY")
        self.__model = openai.OpenAI(api_key=api_key_gpt)
        self.__image_path = os.path.join("db", "image.png")
        self.__voice_model = ElevenLabs(api_key=api_key_eleven)

    def __encode_image(self) -> str:
        with open(file=self.__image_path, mode="rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def image_prompt(self, prompt: str) -> str | None:
        image = self.__encode_image()
        response = self.__model.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image}"},
                        },
                    ],
                }
            ],
            max_tokens=100,
        )

        return response.choices[0].message.content

    def text_prompt(self, prompt: str) -> str | None:
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

    def speak(self):
        r = sr.Recognizer()
        while 1:
            try:
                with sr.Microphone() as source2:

                    r.adjust_for_ambient_noise(source2, duration=0.2)

                    audio2 = r.listen(source2, timeout=10, phrase_time_limit=30)

                    MyText = r.recognize_google(audio2)
                    return MyText

            except sr.UnknownValueError:
                print("Error")

    def generate_response_voice_backup(self, prompt) -> None:
        gpt = self.__model

        response = gpt.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=prompt
        )

        audio_path = os.path.abspath("answer.wav")
        with open(audio_path, "wb") as f:
            f.write(response.content)

        try:
            playsound(audio_path)
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)

    def generate_response_voice(self, text):
        client = self.__voice_model

        audio_stream = client.text_to_speech.convert_as_stream(
            voice_id="bIQlQ61Q7WgbyZAL7IWj",
            output_format="mp3_44100_128",
            text=text,
            model_id="eleven_flash_v2"
        )

        audio_bytes = b''.join([chunk for chunk in audio_stream])

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
            temp_file.write(audio_bytes)
            temp_file_path = temp_file.name
        playsound(temp_file_path)

        os.remove(temp_file_path)

