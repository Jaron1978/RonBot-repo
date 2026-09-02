import json
import logging
import os
import time

from answer import build_answer
from retrieve import load_knowledge


logger = logging.getLogger()

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logger.setLevel(getattr(logging, LOG_LEVEL, logging.INFO))

chunks = load_knowledge()


def lambda_handler(event, context):
    """Handle RonBot API requests."""

    start_time = time.perf_counter()
    request_id = getattr(context, "aws_request_id", "local")

    logger.info(
        "ronbot_request_started request_id=%s",
        request_id
    )

    try:
        body = event.get("body", event)

        if isinstance(body, str):
            body = json.loads(body)

        question = body.get("question", "").strip()

        if not question:
            logger.warning(
                "ronbot_request_rejected request_id=%s reason=missing_question",
                request_id
            )

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

        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

        logger.info(
            "ronbot_request_completed request_id=%s status=200 duration_ms=%s",
            request_id,
            duration_ms
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "answer": answer
            }),
        }

    except (json.JSONDecodeError, AttributeError) as error:
        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

        logger.warning(
            "ronbot_request_rejected request_id=%s reason=%s duration_ms=%s",
            request_id,
            type(error).__name__,
            duration_ms
        )

        return {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "Invalid request."
            }),
        }

    except Exception:
        duration_ms = round(
            (time.perf_counter() - start_time) * 1000,
            2
        )

        logger.exception(
            "ronbot_request_failed request_id=%s status=500 duration_ms=%s",
            request_id,
            duration_ms
        )

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "error": "RonBot is temporarily unavailable."
            }),
        }