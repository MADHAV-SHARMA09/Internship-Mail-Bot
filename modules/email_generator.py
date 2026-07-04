# modules/email_generator.py

import json
import re

from config.logger import logger
from modules.retry_handler import RetryHandler


class EmailGenerator:

    def __init__(self, gemini):

        self.gemini = gemini

    def generate(self, prompt):

        raw = RetryHandler.execute(

            lambda:

            self.gemini.generate(prompt)

        )

        logger.info(

            "Gemini response received."

        )

        raw = raw.strip()

        raw = raw.replace(

            "```json",

            ""

        )

        raw = raw.replace(

            "```",

            ""

        )

        match = re.search(

            r"\{.*\}",

            raw,

            re.DOTALL

        )

        if match is None:

            logger.error(raw)

            raise Exception(

                "Gemini returned invalid JSON."

            )

        try:

            data = json.loads(

                match.group()

            )

        except Exception:

            logger.error(raw)

            raise Exception(

                "Unable to parse Gemini JSON."

            )

        if "subject" not in data:

            raise Exception(

                "Missing subject."

            )

        if "email" not in data:

            raise Exception(

                "Missing email."

            )

        subject = str(

            data["subject"]

        ).strip()

        email = str(

            data["email"]

        ).strip()

        if len(subject) == 0:

            raise Exception(

                "Empty subject."

            )

        if len(email) < 100:

            raise Exception(

                "Email body too short."
            )

        return {

            "subject": subject,

            "email": email

        }