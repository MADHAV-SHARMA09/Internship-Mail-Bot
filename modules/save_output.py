# modules/save_output.py

import os
import pandas as pd


class OutputManager:

    def __init__(self, output_file):

        self.output_file = output_file

        if not os.path.exists(output_file):

            columns = [

                "#",
                "COMPANY NAME",
                "HR EMAIL ID",
                "SUBJECT",
                "EMAIL BODY",
                "STATUS",
                "ERROR"

            ]

            pd.DataFrame(columns=columns).to_excel(
                output_file,
                index=False
            )

    def append(self, row):

        df = pd.read_excel(self.output_file)

        df.loc[len(df)] = row

        df.to_excel(
            self.output_file,
            index=False
        )