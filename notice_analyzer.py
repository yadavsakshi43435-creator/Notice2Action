import re
from datetime import datetime


def extract_deadline(text):
    """Extract a clearly mentioned deadline from a line."""

    patterns = [
        (
            r'\b\d{4}-\d{2}-\d{2}\b',
            ["%Y-%m-%d"]
        ),
        (
            r'\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b',
            ["%d/%m/%Y", "%d-%m-%Y"]
        ),
        (
            r'\b\d{1,2}\s+'
            r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
            r'[a-z]*,?\s+\d{4}\b',
            [
                "%d %b %Y",
                "%d %B %Y",
                "%d %b, %Y",
                "%d %B, %Y"
            ]
        )
    ]

    for pattern, formats in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)

        for match in matches:
            for fmt in formats:
                try:
                    return datetime.strptime(
                        match,
                        fmt
                    ).date().isoformat()

                except ValueError:
                    continue

    return None


def analyze_notice(text):
    """
    Analyze college notice and extract:
    dates, fees, instructions and individual tasks.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # 1. Extract dates
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b\d{4}-\d{2}-\d{2}\b',
        r'\b\d{1,2}\s+'
        r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
        r'[a-z]*,?\s+\d{4}\b'
    ]

    dates = []

    for pattern in date_patterns:
        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE
        )

        dates.extend(matches)

    dates = list(dict.fromkeys(dates))

    # 2. Extract fees
    fees = []

    fee_keywords = [
        "fee", "fees", "amount", "payment",
        "registration", "₹", "rs.", "inr"
    ]

    for line in lines:

        if any(word in line.lower() for word in fee_keywords):

            if re.search(r'\d+', line):
                fees.append(line)

    fees = list(dict.fromkeys(fees))

    # 3. Extract instructions
    action_keywords = [
        "submit", "register", "apply", "attend",
        "contact", "bring", "upload", "complete",
        "mandatory", "required", "last date",
        "deadline", "report", "pay", "fill",
        "download", "visit", "collect", "deposit"
    ]

    instructions = []

    for line in lines:

        if any(word in line.lower() for word in action_keywords):
            instructions.append(line)

    instructions = list(dict.fromkeys(instructions))

    # 4. Extract individual tasks
    tasks = []

    for line in instructions:

        deadline = extract_deadline(line)

        task = {
            "task_title": line[:150],
            "description": line,
            "deadline": deadline,
            "source_text": line
        }

        tasks.append(task)

    return {
        "dates": dates,
        "fees": fees,
        "instructions": instructions,
        "tasks": tasks
    }