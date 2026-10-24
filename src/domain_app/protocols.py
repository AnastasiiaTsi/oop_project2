from typing import Protocol
from domain_app.value_objects import Money

class PaymentGateway(Protocol):
    def process_payment(self, amount: Money) -> str:
        ...

class Notifier(Protocol):
    def send(self, recipient: str, message: str) -> None:
        ...