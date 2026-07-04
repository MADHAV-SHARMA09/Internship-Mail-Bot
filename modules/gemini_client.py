# modules/gemini_client.py

import google.generativeai as genai
from config.config import API_KEYS, MODEL_NAME
from config.logger import logger


class GeminiClient:

    def __init__(self):

        if len(API_KEYS) == 0:
            raise Exception("No Gemini API Keys Found.")

        self.keys = API_KEYS
        self.current = 0

        self.configure()

    def configure(self):

        genai.configure(
            api_key=self.keys[self.current]
        )

        self.model = genai.GenerativeModel(
            MODEL_NAME
        )

        logger.info(
            f"Using Gemini API Key {self.current+1}"
        )

    def next_key(self):

        self.current += 1

        if self.current >= len(self.keys):

            raise Exception(
                "ALL_API_KEYS_EXHAUSTED"
            )

        logger.warning(
            f"Switching to API Key {self.current+1}"
        )

        self.configure()

    def generate(self, prompt):

        while True:

            try:

                response = self.model.generate_content(

                    prompt,

                    generation_config={

                        "temperature": 0.8,

                        "top_p": 0.95,

                        "response_mime_type": "application/json"

                    }

                )

                if not response.text.strip():

                    raise Exception(
                        "Gemini returned empty response."
                    )

                return response.text

            except Exception as e:

                msg = str(e).lower()

                if (

                    "429" in msg

                    or

                    "quota" in msg

                    or

                    "resource_exhausted" in msg

                ):

                    logger.warning(

                        "Quota exhausted."

                    )

                    self.next_key()

                    continue

                raise