import json

from answer import build_answer
from retrieve import load_knowledge


chunks = load_knowledge()


def lambda_handler(event, context):
    """Handle RonBot API requests."""

    try:
        body = event.get("body", event)

        if isinstance(body, str):
            body = json.loads(body)

        question = body.get("question", "").strip()

        if not question:
            return {
                "statusCode": 400,
                "headers": {
                    "Content-Type": "application/json"
                },
                "body": json.dumps({
                    "error": "Question is required."
                }),
            }

        answer = build_answer(question, chunks)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "answer": answer
            }),
        }

    except (json.JSONDecodeError, AttributeError):
        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "Invalid request."
            }),
        }
