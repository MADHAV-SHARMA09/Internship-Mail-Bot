# main.py

import random
import time

from config.config import *
from config.logger import logger

from modules.company_research import CompanyResearch
from modules.email_generator import EmailGenerator
from modules.excel_reader import ExcelReader
from modules.gemini_client import GeminiClient
from modules.gmail_sender import GmailSender
from modules.prompt_builder import PromptBuilder
from modules.save_output import OutputManager


def menu():

    print("\n" + "=" * 60)
    print(" AI Internship Bot ")
    print("=" * 60)
    print("1. Continue Pending Companies")
    print("2. Start From Beginning")
    print("3. Exit")
    print("=" * 60)

    while True:

        choice = input("Enter Choice : ").strip()

        if choice in ["1", "2", "3"]:
            return choice

        print("Invalid Choice.")


def main():

    logger.info("=" * 60)
    logger.info("Starting Internship Bot")

    reader = ExcelReader(COMPANY_FILE)

    df = reader.load()

    choice = menu()

    if choice == "3":
        return

    if choice == "2":

        logger.info("Resetting Excel Status")

        reader.clear_status(df)

        df = reader.load()

    print()

    print(df[["COMPANY NAME", "STATUS"]])

    print()

    research = CompanyResearch()

    gemini = GeminiClient()

    prompt_builder = PromptBuilder(PROMPT_FILE)

    generator = EmailGenerator(gemini)

    sender = GmailSender()

    output = OutputManager(OUTPUT_FILE)

    sent = 0

    for index, row in reader.pending(df):

        if sent >= EMAILS_PER_RUN:

            logger.info("Email limit reached.")

            break

        company = str(row["COMPANY NAME"]).strip()

        email = str(row["HR EMAIL ID"]).strip()

        logger.info(f"Processing : {company}")

        try:

            company_info = research.get_company_info(company)

            prompt = prompt_builder.build(

                company,

                company_info

            )

            generated = generator.generate(prompt)

            # Uncomment after Gmail works
            sender.send(

                email,

                generated["subject"],

                generated["email"]

            )

            df.loc[index, "STATUS"] = "Completed"

            df.loc[index, "SUBJECT"] = generated["subject"]

            df.loc[index, "EMAIL BODY"] = generated["email"]

            df.loc[index, "ERROR"] = ""

            reader.save(df)

            output.append([

                row["#"],

                company,

                email,

                generated["subject"],

                generated["email"],

                "Completed",

                ""

            ])

            logger.info(f"Sent -> {company}")

            sent += 1

            wait = random.randint(20, 45)

            logger.info(f"Sleeping {wait} seconds")

            time.sleep(wait)

        except Exception as e:

            error = str(e)

            logger.error(error)

            # Stop immediately if all API keys are exhausted
            if error == "ALL_API_KEYS_EXHAUSTED":

                logger.error("All Gemini API Keys exhausted.")
                logger.error("Stopping bot.")
                break

            df.loc[index, "STATUS"] = "Failed"

            df.loc[index, "ERROR"] = error

            reader.save(df)

            output.append([

                row["#"],

                company,

                email,

                "",

                "",

                "Failed",

                error

            ])

    logger.info("Bot Finished")
    logger.info("=" * 60)


if __name__ == "__main__":

    main()