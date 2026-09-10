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
MAX_QUESTION_LENGTH = 1_000
MAX_HISTORY_TURNS = 6
MAX_HISTORY_MESSAGE_LENGTH = 1_000
ALLOWED_HISTORY_ROLES = {"user", "assistant"}
MAX_REQUEST_BODY_BYTES = 16_000

def validate_request(body):
    """Validate and sanitise an incoming RonBot request."""

    if not isinstance(body, dict):
        raise ValueError("Request body must be a JSON object.")

    question = body.get("question", "")

    if not isinstance(question, str):
        raise ValueError("Question must be text.")

    question = question.strip()

    if not question:
        raise ValueError("Question is required.")

    if len(question) > MAX_QUESTION_LENGTH:
        raise ValueError("Question is too long.")

    history = body.get("history", [])

    if not isinstance(history, list):
        raise ValueError("History must be a list.")

    if len(history) > MAX_HISTORY_TURNS:
        raise ValueError("Too many history turns.")

    clean_history = []

    for turn in history:
        if not isinstance(turn, dict):
            raise ValueError("Each history turn must be an object.")

        role = turn.get("role")
        content = turn.get("content")

        if role not in ALLOWED_HISTORY_ROLES:
            raise ValueError("History contains an invalid role.")

        if not isinstance(content, str):
            raise ValueError("History content must be text.")

        content = content.strip()

        if not content:
            raise ValueError("History content cannot be empty.")

        if len(content) > MAX_HISTORY_MESSAGE_LENGTH:
            raise ValueError("History content is too long.")

        clean_history.append({
            "role": role,
            "content": content,
        })

    return question, clean_history

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
            if len(body.encode("utf-8")) > MAX_REQUEST_BODY_BYTES:
                raise ValueError("Request body is too large.")

            body = json.loads(body)

        question, history = validate_request(body)

        answer = build_answer(question, chunks, history=history)

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

    except (json.JSONDecodeError, AttributeError, ValueError) as error:
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
