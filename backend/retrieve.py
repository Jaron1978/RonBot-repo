import json
import re
from pathlib import Path


KNOWLEDGE_FILE = (
    Path(__file__).resolve().parent.parent
    / "knowledge"
    / "ronbot_knowledge.jsonl"
)

MIN_RELEVANCE_SCORE = 3
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

QUERY_EXPANSIONS = {
    # Names
    "called": {"name", "named", "names"},
    "named": {"name", "called", "names"},
    "name": {"named", "called", "names"},
    "names": {"name", "named", "called"},

    # Education
    "study": {"studying", "studies", "education", "degree", "university", "bsc", "computing"},
    "studying": {"study", "studies", "education", "degree", "university", "bsc", "computing"},
    "studies": {"study", "studying", "education", "degree", "university", "bsc", "computing"},
    "degree": {"education", "university", "bsc", "computing", "studying"},

    # Current employment
    "job": {"work", "role", "engineer", "employment", "career"},
    "work": {"job", "role", "engineer", "employment", "career"},
    "role": {"job", "work", "engineer", "employment", "career"},

    # Previous employment
    "before": {"previous", "prior"},   
    "previous": {"before", "prior"},
    "prior": {"before", "previous"},

   # School / secondary education
    "school": {"education", "secondary", "academy", "stewards", "gcse"},
    "secondary": {"school", "education", "academy", "stewards", "gcse"},
    "academy": {"school", "secondary", "education", "stewards", "gcse"},
    "gcse": {"gcses", "education", "secondary", "school", "qualifications"},
    "gcses": {"gcse", "education", "secondary", "school", "qualifications"},
}


NAMING_WORDS = {"called", "name", "named", "names"}

def tokenize(text):
    """Convert text into useful searchable words."""
    words = re.findall(r"[a-z0-9]+", text.lower())

    tokens = {
        word
        for word in words
        if word not in STOP_WORDS and len(word) > 1
    }

    expanded_tokens = set(tokens)

    for token in tokens:
        expanded_tokens.update(QUERY_EXPANSIONS.get(token, set()))

    return expanded_tokens
    

def score_chunk(question, chunk):
    """Score a knowledge chunk against the user's question."""
    question_words = tokenize(question)
    chunk_words = tokenize(chunk.get("text", ""))
    title_words = tokenize(chunk.get("title", ""))

    text_matches = len(question_words & chunk_words)
    title_matches = len(question_words & title_words)

    naming_bonus = 0
    relationship_bonus = 0
    skills_bonus = 0

    question_lower = question.lower()
    chunk_text = chunk.get("text", "")
    chunk_text_lower = chunk_text.lower()

    # Broad skills questions should favour Work Experience
    # and Certifications rather than unrelated website pages.
    if "skill" in question_lower or "skills" in question_lower:
        title_lower = chunk.get("title", "").lower()

        if "work experience" in title_lower:
            skills_bonus = 5

        elif "certifications" in title_lower:
            skills_bonus = 4

    # Questions about Ron's role before joining Redpanda.
    if "before redpanda" in question_lower:
        if "redpanda" in chunk_text_lower and "nexxen" in chunk_text_lower:
            relationship_bonus = 6
    if any(word in question_lower for word in NAMING_WORDS):
        if "dogs" in question_words and re.search(
            r"\bdogs\b.{0,50}\b[A-Z][a-z]+\s+and\s+[A-Z][a-z]+\b",
            chunk_text
        ):
            naming_bonus = 3

    return (
        text_matches
        + (title_matches * 3)
        + naming_bonus
        + relationship_bonus
        + skills_bonus
    )

def retrieve(question, chunks, limit=3):
    """Return the strongest website chunks for a question."""
    scored = []

    for chunk in chunks:
        score = score_chunk(question, chunk)

        if score >= MIN_RELEVANCE_SCORE:
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
