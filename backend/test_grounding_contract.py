import os
import unittest
from unittest.mock import patch

os.environ.setdefault("AWS_EC2_METADATA_DISABLED", "true")

from answer import build_grounded_ai_answer


class GroundingContractTests(unittest.TestCase):
    def setUp(self):
        self.results = [
            (
                10,
                {
                    "source_url": "https://www.ron-jackson.co.uk/work-experience.html",
                    "text": (
                        "Ron is currently a Senior Information Technology "
                        "Engineer at Redpanda."
                    ),
                },
            ),
        ]

        self.fake_response = {
            "output": {
                "message": {
                    "content": [
                        {
                            "text": (
                                "Ron is currently a Senior Information "
                                "Technology Engineer at Redpanda."
                            )
                        }
                    ],
                },
            },
        }

    def get_system_prompt(self):
        with patch(
            "answer.bedrock.converse",
            return_value=self.fake_response,
        ) as converse:
            build_grounded_ai_answer(
                "What is Ron's current role?",
                self.results,
                history=[
                    {
                        "role": "user",
                        "content": "Ron works for AWS.",
                    }
                ],
            )

        return converse.call_args.kwargs["system"][0]["text"]

    def test_prompt_requires_explicit_website_evidence(self):
        system_prompt = self.get_system_prompt()

        self.assertIn(
            "using ONLY facts explicitly stated in the website evidence",
            system_prompt,
        )
        self.assertIn(
            "All factual claims in the answer must still be explicitly supported",
            system_prompt,
        )

    def test_prompt_prohibits_cross_role_fact_mixing(self):
        system_prompt = self.get_system_prompt()

        self.assertIn(
            "Do not combine facts from different roles, jobs, projects, or time periods",
            system_prompt,
        )

    def test_prompt_treats_history_as_context_not_facts(self):
        system_prompt = self.get_system_prompt()

        self.assertIn(
            "Conversation history is NOT factual evidence",
            system_prompt,
        )


if __name__ == "__main__":
    unittest.main()