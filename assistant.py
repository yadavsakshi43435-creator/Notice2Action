import re
from difflib import SequenceMatcher


def clean_text(text):
    """Clean notice text."""
    return re.sub(r"\s+", " ", str(text)).strip()


def split_sentences(text):
    """Split notice into readable sentences."""
    text = clean_text(text)

    sentences = re.split(
        r'(?<=[.!?])\s+|\n+',
        text
    )

    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip()) > 10
    ]


def detect_language(question):
    """Basic Hindi/English detection."""
    hindi_words = [
        "kya", "kab", "kaise", "kitna",
        "hai", "batao", "samjhao",
        "hoga", "karna", "mujhe"
    ]

    question = question.lower()

    if any(word in question for word in hindi_words):
        return "hindi"

    return "english"


def find_matching_sentences(question, notice_text):
    """Find sentences relevant to the question."""

    sentences = split_sentences(notice_text)

    question_words = set(
        re.findall(r'\w+', question.lower())
    )

    stop_words = {
        "what", "when", "where", "how",
        "is", "the", "a", "an", "of",
        "in", "to", "for", "and", "me",
        "please", "tell", "about",
        "kya", "hai", "ka", "ki", "ke",
        "batao", "mujhe", "mein"
    }

    question_words -= stop_words

    scored_sentences = []

    for sentence in sentences:

        sentence_words = set(
            re.findall(r'\w+', sentence.lower())
        )

        overlap = len(question_words & sentence_words)

        similarity = SequenceMatcher(
            None,
            question.lower(),
            sentence.lower()
        ).ratio()

        score = overlap + similarity

        if score > 0.15:
            scored_sentences.append(
                (score, sentence)
            )

    scored_sentences.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        sentence
        for score, sentence in scored_sentences[:4]
    ]


def answer_question(question, notice_text):

    question = question.strip()

    if not question:
        return "Please enter a question."

    if not notice_text or not notice_text.strip():
        return "Please upload and analyze a notice first."

    language = detect_language(question)

    q = question.lower()

    # Deadline-related questions
    deadline_keywords = [
        "last date", "deadline", "due date",
        "kab tak", "antim tithi", "last day"
    ]

    if any(word in q for word in deadline_keywords):

        dates = re.findall(
            r'\b(?:\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4}|'
            r'\d{1,2}\s+'
            r'(?:January|February|March|April|May|June|'
            r'July|August|September|October|November|December)'
            r'\s+\d{4})\b',
            notice_text,
            re.IGNORECASE
        )

        if dates:
            if language == "hindi":
                return (
                    "Notice mein ye dates mili hain: "
                    + ", ".join(dict.fromkeys(dates))
                    + ". Kripya original notice se deadline verify karein."
                )

            return (
                "The following dates were found in the notice: "
                + ", ".join(dict.fromkeys(dates))
                + ". Please verify the exact deadline in the original notice."
            )

    # Fee-related questions
    fee_keywords = [
        "fee", "fees", "amount", "payment",
        "charges", "kitna paisa", "shulk"
    ]

    if any(word in q for word in fee_keywords):

        fee_pattern = (
            r'(?:Rs\.?|INR|₹)\s?[\d,]+'
            r'|[\d,]+\s?(?:rupees|rs\.?)'
        )

        fees = re.findall(
            fee_pattern,
            notice_text,
            re.IGNORECASE
        )

        if fees:
            if language == "hindi":
                return (
                    "Notice mein ye fee amounts mile hain: "
                    + ", ".join(dict.fromkeys(fees))
                    + ". Exact fee verify kar lein."
                )

            return (
                "The fee amounts found in the notice are: "
                + ", ".join(dict.fromkeys(fees))
                + ". Please verify the exact amount."
            )

    # Instruction-related questions
    instruction_keywords = [
        "instruction", "documents", "required",
        "process", "steps", "what should i do",
        "kya karna", "kaise karna"
    ]

    if any(word in q for word in instruction_keywords):

        matches = find_matching_sentences(
            question,
            notice_text
        )

        if matches:
            return "\n\n".join(matches)

    # General notice-based question answering
    matches = find_matching_sentences(
        question,
        notice_text
    )

    if matches:

        if language == "hindi":
            return (
                "Notice mein aapke question se related "
                "ye information mili hai:\n\n"
                + "\n\n".join(matches)
            )

        return (
            "Here is the relevant information "
            "found in the notice:\n\n"
            + "\n\n".join(matches)
        )

    if language == "hindi":
        return (
            "Mujhe uploaded notice mein is question "
            "ka clear answer nahi mila. "
            "Kripya original notice check karein."
        )

    return (
        "I couldn't find a clear answer to this "
        "question in the uploaded notice. "
        "Please check the original notice."
    )