# modules/retry_handler.py

import time

from config.config import MAX_RETRIES


class RetryHandler:

    @staticmethod

    def execute(function):

        attempt = 0

        while attempt < MAX_RETRIES:

            try:

                return function()

            except Exception as e:

                attempt += 1

                message = str(e).lower()

                if (

                    "429" in message

                    or

                    "quota" in message

                    or

                    "resource_exhausted" in message

                ):

                    raise

                wait = 2 ** attempt

                print(

                    f"Retry {attempt}/{MAX_RETRIES}"

                )

                print(

                    f"Waiting {wait} seconds..."

                )

                time.sleep(wait)

        raise Exception(

            "Maximum retries exceeded."

        )