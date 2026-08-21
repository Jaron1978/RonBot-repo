from retrieve import load_knowledge, retrieve


CONTACT_MESSAGE = (
    "I couldn't find enough information on Ron's website to answer that accurately. "
    "Please use the Contact page to ask Ron directly."
)


def build_answer(question, chunks):
    results = retrieve(question, chunks, limit=3)

    if not results:
        return CONTACT_MESSAGE

    top_score, top_chunk = results[0]
    text = top_chunk.get("text", "")

    # Very simple first-pass grounding rules.
    question_lower = question.lower()

    if "breed" in question_lower and "breed" not in text.lower():
        return (
            "Ron's website tells me that his dogs are called Thor and Loki, "
            "but it doesn't say what breed they are. "
            "Please use the Contact page if you'd like to ask Ron directly."
        )

    return (
        "I found this on Ron's website:\n\n"
        f"{text[:700]}\n\n"
        f"Source: {top_chunk.get('source_url', 'Unknown')}"
    )


def main():
    chunks = load_knowledge()

    print(f"RonBot loaded {len(chunks)} website knowledge chunks.")
    print("Type 'quit' to exit.\n")

    while True:
        question = input("Ask RonBot: ").strip()

        if question.lower() in {"quit", "exit"}:
            break

        print()
        print(build_answer(question, chunks))
        print()


if __name__ == "__main__":
    main()
