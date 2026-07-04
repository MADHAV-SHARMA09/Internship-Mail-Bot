# modules/gmail_sender.py

import os
import smtplib
import ssl

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase

from email import encoders

from config.config import (

    GMAIL_EMAIL,

    GMAIL_PASSWORD,

    RESUME_PATH

)

from config.logger import logger


class GmailSender:

    def send(

        self,

        receiver,

        subject,

        body

    ):

        message = MIMEMultipart()

        message["From"] = GMAIL_EMAIL

        message["To"] = receiver

        message["Subject"] = subject

        message.attach(

            MIMEText(

                body,

                "plain"

            )

        )

        if os.path.exists(RESUME_PATH):

            with open(

                RESUME_PATH,

                "rb"

            ) as file:

                part = MIMEBase(

                    "application",

                    "octet-stream"

                )

                part.set_payload(

                    file.read()

                )

            encoders.encode_base64(part)

            part.add_header(

                "Content-Disposition",

                'attachment; filename="Madhav_Sharma_Resume.pdf"'

            )

            message.attach(part)

        context = ssl.create_default_context()

        with smtplib.SMTP(

            "smtp.gmail.com",

            587

        ) as smtp:

            smtp.ehlo()

            smtp.starttls(

                context=context

            )

            smtp.login(

                GMAIL_EMAIL,

                GMAIL_PASSWORD

            )

            smtp.sendmail(

                GMAIL_EMAIL,

                receiver,

                message.as_string()

            )

        logger.info(

            f"Mail sent to {receiver}"

        )