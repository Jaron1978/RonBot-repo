from retrieve import load_knowledge, retrieve


CONTACT_MESSAGE = (
    "I couldn't find enough information on Ron's website to answer that accurately. "
    "Please use the Contact page to ask Ron directly."
)

TECHNICAL_DEPTH_TERMS = {
    "technical",
    "implementation",
    "architecture",
    "retrieve",
    "retrieval",
    "grounding",
    "knowledge",
    "jsonl",
    "ingestion",
}

def wants_technical_depth(question):
    """Return True when the visitor explicitly asks for implementation detail."""
    question_lower = question.lower()

    return (
        any(term in question_lower for term in TECHNICAL_DEPTH_TERMS)
        or "how does ronbot work" in question_lower
        or "how is ronbot built" in question_lower
        or "how did you build ronbot" in question_lower
    )


def build_answer(question, chunks):
    results = retrieve(question, chunks, limit=3)

    if not results:
        return CONTACT_MESSAGE

    top_score, top_chunk = results[0]
    text = top_chunk.get("text", "")
    text_lower = text.lower()
    question_lower = question.lower()

    # Concise general answer for recruiter/casual questions about RonBot.
    if any(
        phrase in question_lower
        for phrase in {
            "what is ronbot",
            "tell me about ronbot",
            "what does ronbot do",
        }
    ) and not wants_technical_depth(question):
        combined_text = " ".join(
            chunk.get("text", "").lower()
            for _, chunk in results
        )

        if (
            "ai-powered interactive portfolio assistant" in combined_text
            and "using only information published on this website" in combined_text
        ):
            return (
                "RonBot is an AI-powered portfolio assistant that helps visitors "
                "explore Ron's experience, skills, certifications, education and projects "
                "using only information published on his website."
            )

    # Technical-depth answer for visitors asking how RonBot works.
    if wants_technical_depth(question):
        combined_text = " ".join(
            chunk.get("text", "").lower()
            for _, chunk in results
        )

        required_terms = {
            "website-only grounding",
            "website knowledge",
            "python",
            "retrieval",
        }

        if any(term in combined_text for term in required_terms):
            return (
                "RonBot currently works by using content published on Ron's portfolio "
                "as its knowledge source. The website is ingested into structured local "
                "knowledge, Python retrieval logic finds the most relevant chunks for a "
                "question, and the answer layer only responds when sufficient website "
                "evidence is available. If the evidence is insufficient, RonBot falls "
                "back to the Contact page rather than guessing."
            )

    # Dog breed guardrail.
    if "breed" in question_lower and "breed" not in text_lower:
        return (
            "Ron's website tells me that his dogs are called Thor and Loki, "
            "but it doesn't say what breed they are. "
            "Please use the Contact page if you'd like to ask Ron directly."
        )

    # Dog names.
    if "dog" in question_lower and any(
        word in question_lower for word in {"called", "name", "named", "names"}
    ):
        if "thor and loki" in text_lower:
            return "Ron's dogs are called Thor and Loki."
    # Current study / degree.
    if any(
        phrase in question_lower
        for phrase in {"what is ron studying", "what degree", "university", "study"}
    ):
        if "bsc (hons) computing & it" in text_lower and "open university" in text_lower:
            return (
                "Ron is currently studying part-time towards a "
                "BSc (Hons) in Computing & IT with The Open University."
            )
    # Secondary school.
    if any(
        phrase in question_lower
        for phrase in {
            "what school",
            "which school",
            "school did ron attend",
            "where did ron go to school",
        }
    ):
        for _, result_chunk in results:
            result_text_lower = result_chunk.get("text", "").lower()

            if "stewards academy" in result_text_lower and "harlow" in result_text_lower:
                return (
                    "Ron attended Stewards Academy in Harlow from 1990 to 1996."
                )

    # GCSE subjects.
    if "gcse" in question_lower or "gcses" in question_lower:
        for _, result_chunk in results:
            result_text_lower = result_chunk.get("text", "").lower()

            if (
                "english language" in result_text_lower
                and "english literature" in result_text_lower
                and "mathematics" in result_text_lower
                and "french" in result_text_lower
                and "history" in result_text_lower
                and "business studies" in result_text_lower
                and "computing" in result_text_lower
            ):
                return (
                    "Ron gained GCSEs in English Language, English Literature, "
                    "Mathematics, French, History, Business Studies and Computing."
                )
    # Current job.
    if any(
        phrase in question_lower
        for phrase in {
            "current job",
            "current role",
            "where does ron work",
            "where is ron working",
        }
    ):
        if "senior information technology engineer" in text_lower and "redpanda" in text_lower:
            return (
                "Ron is currently a Senior Information Technology Engineer at Redpanda."
            )

    # Previous employer before Redpanda.
    if any(
        phrase in question_lower
        for phrase in {
            "before redpanda",
            "before joining redpanda",
            "worked before redpanda",
            "previous employer",
        }
    ):
        if "systems engineer i" in text_lower and "nexxen" in text_lower:
            return (
                "Before joining Redpanda, Ron worked as a Systems Engineer I "
                "at Nexxen from January 2022 to February 2025."
            )

    # Cloud certifications.
    if (
        "cloud" in question_lower
        and ("certification" in question_lower or "certifications" in question_lower)
    ):
        if (
            "aws certified cloud practitioner" in text_lower
            and "cloud digital leader" in text_lower
            and "azure fundamentals" in text_lower
        ):
            return (
                "Ron currently holds the AWS Certified Cloud Practitioner, "
                "Google Cloud Digital Leader, and Microsoft Certified: "
                "Azure Fundamentals certifications."
            )

    # Current featured certifications.
    if (
        "certification" in question_lower or "certifications" in question_lower
    ):
        if (
            "aws certified cloud practitioner" in text_lower
            and "pcep" in text_lower
            and "getting started with artificial intelligence" in text_lower
            and "linux essentials certificate" in text_lower
        ):
            return (
                "Ron currently holds the AWS Certified Cloud Practitioner, "
                "Google Cloud Digital Leader, Microsoft Certified: Azure Fundamentals, "
                "PCEP Certified Entry-Level Python Programmer, "
                "IBM Getting Started with Artificial Intelligence, "
                "and Linux Essentials Certificate."
            )

    # Broad skills summary.
    if "skill" in question_lower or "skills" in question_lower:
        combined_text = " ".join(
            chunk.get("text", "").lower()
            for chunk in chunks
        )

        required_terms = {
            "aws",
            "azure",
            "linux",
            "python",
            "networking",
        }

        if all(term in combined_text for term in required_terms):
            return (
                "Ron has broad experience across IT support, systems engineering, "
                "cloud infrastructure and technical leadership. His core skills include "
                "AWS, Azure, Linux, Windows Server, networking, Python, Terraform, "
                "HTML/CSS, virtualisation, Active Directory, ServiceNow, Git/GitHub and AI."
            )

    return (
        "I found this on Ron's website:\n\n"
        f"{text[:700]}\n\n"
        f"Source: {top_chunk.get('source_url', 'Unknown')}"
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
