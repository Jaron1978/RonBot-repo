import os
import unittest

os.environ.setdefault("AWS_EC2_METADATA_DISABLED", "true")

from answer import CONTACT_MESSAGE, PRIVACY_MESSAGE, build_answer
from retrieve import load_knowledge


class RonBotQuestionSetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chunks = load_knowledge()

    def test_answers_current_role(self):
        answer = build_answer(
            "What is Ron's current role?",
            self.chunks,
        )

        self.assertIn("Senior Information Technology Engineer", answer)
        self.assertIn("Redpanda", answer)

    def test_answers_skills_question(self):
        answer = build_answer(
            "What skills does Ron have?",
            self.chunks,
        )

        self.assertIn("AWS", answer)
        self.assertIn("Python", answer)
        self.assertIn("Linux", answer)

    def test_answers_broad_work_history_question(self):
        answer = build_answer(
            "What previous roles has Ron held?",
            self.chunks,
        )

        self.assertIn("Nexxen", answer)
        self.assertIn("Yoti", answer)
        self.assertIn("William Hill", answer)
        self.assertIn("ASOS.com", answer)
        self.assertIn("Genesis Oil & Gas", answer)
        self.assertIn("Kalamazoo-Reynolds", answer)
        self.assertIn("Heritage Care", answer)

    def test_answers_cloud_certifications(self):
        answer = build_answer(
            "What cloud certifications does Ron have?",
            self.chunks,
        )

        self.assertIn("AWS Certified Cloud Practitioner", answer)
        self.assertIn("Azure Fundamentals", answer)

    def test_answers_ronbot_summary(self):
        answer = build_answer(
            "Tell me about RonBot.",
            self.chunks,
        )

        self.assertIn("AI-powered portfolio assistant", answer)
        self.assertIn("website", answer)

    def test_uses_history_for_a_follow_up(self):
        answer = build_answer(
            "What about his current role?",
            self.chunks,
            history=[
                {
                    "role": "user",
                    "content": "Where does Ron work?",
                },
                {
                    "role": "assistant",
                    "content": "Ron works at Redpanda.",
                },
            ],
        )

        self.assertIn("Redpanda", answer)

    def test_unknown_question_uses_contact_fallback(self):
        answer = build_answer(
            "What is Ron's favourite film?",
            self.chunks,
        )

        self.assertEqual(answer, CONTACT_MESSAGE)

    def test_private_question_uses_privacy_guardrail(self):
        answer = build_answer(
            "Where does Ron live?",
            self.chunks,
        )

        self.assertEqual(answer, PRIVACY_MESSAGE)


if __name__ == "__main__":
    unittest.main()
