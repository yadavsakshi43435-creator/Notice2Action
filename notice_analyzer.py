
import re

def analyze_notice(text):
    """
    Identify dates, fees and important instructions
    from extracted college notice text.
    """

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    # 1. Find dates
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
            pattern, text, re.IGNORECASE
        )
        dates.extend(matches)

    dates = list(dict.fromkeys(dates))

    # 2. Find fee-related information
    fees = []

    fee_keywords = [
        "fee", "fees", "amount", "payment",
        "registration", "₹", "rs.", "inr"
    ]

    for line in lines:
        if any(word in line.lower() for word in fee_keywords):
            if re.search(r'\d+', line):
                fees.append(line)

    # 3. Find important instructions
    action_keywords = [
        "submit", "register", "apply", "attend",
        "contact", "bring", "upload", "complete",
        "mandatory", "required", "last date",
        "deadline", "report"
    ]

    instructions = []

    for line in lines:
        if any(word in line.lower() for word in action_keywords):
            instructions.append(line)

    return {
        "dates": dates,
        "fees": list(dict.fromkeys(fees)),
        "instructions": list(dict.fromkeys(instructions))
    }