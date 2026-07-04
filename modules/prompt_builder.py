# modules/prompt_builder.py

from jinja2 import Template

from config.config import CANDIDATE


class PromptBuilder:

    def __init__(self, template_path):

        with open(
            template_path,
            "r",
            encoding="utf-8"
        ) as f:

            self.template = Template(f.read())

    def build(
        self,
        company,
        company_info
    ):

        return self.template.render(

            company=company,

            company_info=company_info,

            name=CANDIDATE["name"],

            college=CANDIDATE["college"],

            degree=CANDIDATE["degree"],

            batch=CANDIDATE["batch"],

            roles=", ".join(CANDIDATE["roles"]),

            skills=", ".join(CANDIDATE["skills"]),

            projects=", ".join(CANDIDATE["projects"])

        )