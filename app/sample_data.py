"""Synthetic support replies with fake personal details. No real customer data is used."""
import random

OPEN = ["Thanks for contacting us", "Thank you for reaching out", "Sorry for the trouble",
        "I am sorry to hear that", "Thanks for your patience", "Happy to help you today"]
BODY = [
    "I have checked order {o} and it will ship within two business days",
    "I have checked order {o} and it was delivered yesterday",
    "Your refund for order {o} has been issued and should appear in five days",
    "I can see order {o} is delayed and I have escalated it to the warehouse team",
    "Please reply to {e} with a photo of the damaged item",
    "I have sent a return label to {e} so you can send the item back",
    "You can reach us on {p} if you need anything else",
    "I have updated the delivery address on order {o}",
    "Your replacement for order {o} will arrive next week",
    "I have applied a discount to your next order as an apology",
]
CLOSE = ["Let me know if there is anything else I can do",
         "Please let us know if you have any other questions",
         "Have a great day", "We appreciate your business", "Thanks again for shopping with us"]


def generate_raw(count: int = 400, seed: int = 0) -> list[str]:
    rng = random.Random(seed)
    lines = []
    for _ in range(count):
        o = f"#{rng.randint(10000, 99999)}"
        e = f"user{rng.randint(1, 99)}@example.com"
        p = f"555-{rng.randint(100, 999)}-{rng.randint(1000, 9999)}"
        body = rng.choice(BODY).format(o=o, e=e, p=p)
        lines.append(f"{rng.choice(OPEN)}. {body}. {rng.choice(CLOSE)}.")
    return lines
