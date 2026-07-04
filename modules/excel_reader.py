# modules/excel_reader.py

import os
import pandas as pd


class ExcelReader:

    def __init__(self, excel_path):
        self.excel_path = excel_path

    def load(self):

        if not os.path.exists(self.excel_path):
            raise FileNotFoundError(
                f"Excel file not found:\n{self.excel_path}"
            )

        # Prevent blank cells from becoming NaN
        df = pd.read_excel(
            self.excel_path,
            keep_default_na=False
        )

        df.fillna("", inplace=True)

        # Remove spaces from column names
        df.columns = [str(c).strip() for c in df.columns]

        required = [
            "#",
            "COMPANY NAME",
            "HR EMAIL ID"
        ]

        for col in required:

            if col not in df.columns:

                raise Exception(
                    f"Missing Column : {col}"
                )

        extra = [

            "STATUS",
            "SUBJECT",
            "EMAIL BODY",
            "ERROR"

        ]

        for col in extra:

            if col not in df.columns:

                df[col] = ""

        return df

    def save(self, df):

        df.to_excel(
            self.excel_path,
            index=False
        )

    def clear_status(self, df):

        df["STATUS"] = ""
        df["SUBJECT"] = ""
        df["EMAIL BODY"] = ""
        df["ERROR"] = ""

        self.save(df)

    def pending(self, df):

        pending = []

        for index, row in df.iterrows():

            status = str(
                row["STATUS"]
            ).strip().lower()

            if status != "completed":

                pending.append(
                    (index, row)
                )

        return pending