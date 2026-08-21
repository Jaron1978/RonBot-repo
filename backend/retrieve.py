import json
import re
from pathlib import Path


KNOWLEDGE_FILE = (
    Path(__file__).resolve().parent.parent
    / "knowledge"
    / "ronbot_knowledge.jsonl"
)


def load_knowledge():
    """Load RonBot's website-only knowledge base."""
    chunks = []

    with KNOWLEDGE_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if line:
                chunks.append(json.loads(line))

    return chunks


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "does",
    "for", "from", "have", "he", "his", "how", "i", "in",
    "is", "it", "of", "on", "ron", "the", "to", "what",
    "when", "where", "who", "with"
}


def tokenize(text):
    """Convert text into useful searchable words."""
    words = re.findall(r"[a-z0-9]+", text.lower())

    return {
        word
        for word in words
        if word not in STOP_WORDS and len(word) > 1
    }

def score_chunk(question, chunk):
    """Score a knowledge chunk against the user's question."""
    question_words = tokenize(question)
    chunk_words = tokenize(chunk.get("text", ""))
    title_words = tokenize(chunk.get("title", ""))

    text_matches = len(question_words & chunk_words)
    title_matches = len(question_words & title_words)

    return text_matches + (title_matches * 3)

def retrieve(question, chunks, limit=3):
    """Return the strongest website chunks for a question."""
    scored = []

    for chunk in chunks:
        score = score_chunk(question, chunk)

        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)

    return scored[:limit]


def main():
    chunks = load_knowledge()

    print(f"RonBot loaded {len(chunks)} website knowledge chunks.")
    print("Type 'quit' to exit.\n")

    while True:
        question = input("Ask RonBot: ").strip()

        if question.lower() in {"quit", "exit"}:
            break

        results = retrieve(question, chunks)

        if not results:
            print("\nRonBot couldn't find that on Ron's website.")
            print("Please use the Contact page to ask Ron directly.\n")
            continue

        print("\nBest website matches:\n")

        for score, chunk in results:
            print(f"Score: {score}")
            print(f"Page: {chunk.get('title', 'Unknown')}")
            print(f"Source: {chunk.get('source_url', 'Unknown')}")
            print(f"Text: {chunk.get('text', '')[:500]}")
            print("-" * 60)

        print()


if __name__ == "__main__":
    main()
