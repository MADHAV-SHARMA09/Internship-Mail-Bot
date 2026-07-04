# modules/checkpoint.py

import json
import os


class CheckPoint:

    def __init__(self, path):

        self.path = path

    def save(self, row_number):

        data = {
            "last_processed_row": row_number
        }

        with open(
            self.path,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def load(self):

        if not os.path.exists(self.path):
            return 0

        with open(
            self.path,
            "r"
        ) as file:

            data = json.load(file)

        return data.get(
            "last_processed_row",
            0
        )

    def reset(self):

        self.save(0)