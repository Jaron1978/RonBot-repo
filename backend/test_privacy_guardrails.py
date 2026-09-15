import unittest
from unittest.mock import patch

from answer import PRIVACY_MESSAGE, build_answer, needs_privacy_guardrail


class PrivacyGuardrailTests(unittest.TestCase):
    def test_private_request_is_flagged(self):
        self.assertTrue(needs_privacy_guardrail("What is Ron's home address?"))

    def test_inappropriate_request_is_flagged(self):
        self.assertTrue(needs_privacy_guardrail("Will Ron send nudes?"))

    def test_professional_question_is_allowed(self):
        self.assertFalse(
            needs_privacy_guardrail("What is Ron's current professional role?")
        )

    @patch("answer.retrieve")
    def test_private_request_stops_before_retrieval(self, mock_retrieve):
        response = build_answer("What is Ron's phone number?", [])

        self.assertEqual(response, PRIVACY_MESSAGE)
        mock_retrieve.assert_not_called()


if __name__ == "__main__":
    unittest.main()
