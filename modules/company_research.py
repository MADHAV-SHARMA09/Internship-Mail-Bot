# modules/company_research.py

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS

from config.logger import logger


class CompanyResearch:

    def __init__(self):

        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/137.0 Safari/537.36"
            )
        }

    def search(self, company):

        queries = [

            f"{company} official website",
            f"{company} about",
            f"{company} careers",
            f"{company} AI",
            f"{company} LinkedIn"

        ]

        urls = []

        blacklist = [

            "bing.com",
            "youtube.com",
            "facebook.com",
            "instagram.com",
            "twitter.com",
            "x.com",
            "wikipedia.org",
            "reddit.com",
            "quora.com",
            "glassdoor.com",
            "indeed.com",
            "aclick"

        ]

        with DDGS() as ddgs:

            for query in queries:

                try:

                    results = list(
                        ddgs.text(
                            query,
                            max_results=3
                        )
                    )

                    for result in results:

                        url = result.get("href", "").strip()

                        if not url:
                            continue

                        url_lower = url.lower()

                        if any(bad in url_lower for bad in blacklist):
                            continue

                        if url not in urls:
                            urls.append(url)

                except Exception as e:

                    logger.warning(e)

        return urls[:6]

    def scrape(self, url):

        try:

            logger.info(f"Researching {url}")

            response = requests.get(

                url,

                headers=self.headers,

                timeout=5

            )

            response.raise_for_status()

            soup = BeautifulSoup(

                response.text,

                "html.parser"

            )

            for tag in soup(

                [

                    "script",

                    "style",

                    "header",

                    "footer",

                    "nav",

                    "svg",

                    "img",

                    "noscript"

                ]

            ):

                tag.decompose()

            text = soup.get_text(" ")

            text = " ".join(text.split())

            return text[:2500]

        except Exception as e:

            logger.warning(f"Skipping {url}")

            return ""

    def get_company_info(self, company):

        urls = self.search(company)

        if len(urls) == 0:

            return f"{company} is a technology company."

        info = ""

        for url in urls:

            page = self.scrape(url)

            if len(page) < 200:
                continue

            info += page
            info += "\n\n"

        if len(info.strip()) == 0:

            return f"{company} is a technology company."

        return info[:6000]