HIGH_RISK_KEYWORDS = [
    "suicide",
    "kill myself",
    "end my life",
    "want to die",
    "don't want to live",
    "do not want to live",
    "self harm",
    "self-harm",
    "hurt myself"
]


def check_safety(message: str):
    """
    Basic safety screening for high-risk messages.
    Returns a response if the message requires escalation.
    Otherwise returns None.
    """

    text = message.lower().strip()

    for keyword in HIGH_RISK_KEYWORDS:
        if keyword in text:
            return (
                "I'm sorry you're going through something this difficult. "
                "PsyBot isn't an emergency or crisis service, and I can't "
                "provide the immediate help you may need. Please reach out "
                "to a trusted person or a qualified mental health professional "
                "right now. If you may be in immediate danger, contact your "
                "local emergency service."
            )

    return None