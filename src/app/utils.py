import re

def validate_phone(phone: str) -> bool:
    if phone is not None and len(phone) > 7 and phone[0] == '+' and phone[1:].isdigit():
        return True
    return False


def validate_email(email: str) -> bool:
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(email_regex, email))