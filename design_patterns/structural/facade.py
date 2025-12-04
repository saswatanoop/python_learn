"""
=====================================================
FACADE PATTERN (Structural)
=====================================================

WHAT IS FACADE?
----------------
Facade provides a simple, unified interface to a complex system of classes.
It hides internal complexity and exposes only what the client needs.

WHY USE FACADE?
----------------
- To simplify interactions with complex subsystems.
- To reduce coupling: clients depend only on the facade, not individual classes.
- To avoid overwhelming the client with details required in proper order.
- To improve readability and maintainability.

REAL USE CASES
----------------
- Payment gateways (many steps → one facade method)
- Media conversion libraries
- Database connection pooling
- Complex workflows needing orchestration
- SDK wrappers
- Subsystems with strict operation sequences

SOLID MAPPING
-------------
- SRP: Facade has one job → simplify usage.
- OCP: You can improve internals without changing client-facing API.
- DIP: Clients depend on the Facade, not the complex subsystem.

WHEN NOT TO USE
----------------
- When the subsystem is already simple.
- When a direct call is clearer than hiding logic behind a facade.

=====================================================
CODE: WITHOUT FACADE + WITH FACADE
=====================================================
"""

from __future__ import annotations


# =====================================================
# 1) WITHOUT FACADE (the problem: client coordinates too much)
# =====================================================

class PaymentValidator:
    def validate(self, card_number: str) -> bool:
        return len(card_number) == 16


class PaymentAuthorizer:
    def authorize(self, card_number: str, amount: float) -> bool:
        return amount <= 50000  # stub


class PaymentProcessorBackend:
    def capture(self, card_number: str, amount: float) -> str:
        return f"Charged ₹{amount:.2f} to card ****{card_number[-4:]}"


def pay_without_facade(card_number: str, amount: float) -> str:
    validator = PaymentValidator()
    if not validator.validate(card_number):
        return "Invalid card"

    authorizer = PaymentAuthorizer()
    if not authorizer.authorize(card_number, amount):
        return "Authorization failed"

    backend = PaymentProcessorBackend()
    return backend.capture(card_number, amount)


# =====================================================
# 2) WITH FACADE (clean client usage)
# =====================================================

class PaymentFacade:
    """
    Facade shields client from validation, authorization, and capture workflow.
    Client simply calls pay(), unaware of subsystem steps.
    """

    def __init__(self):
        self._validator = PaymentValidator()
        self._authorizer = PaymentAuthorizer()
        self._backend = PaymentProcessorBackend()

    def pay(self, card_number: str, amount: float) -> str:
        if not self._validator.validate(card_number):
            return "Invalid card"

        if not self._authorizer.authorize(card_number, amount):
            return "Authorization failed"

        return self._backend.capture(card_number, amount)


# =====================================================
# DEMO
# =====================================================
if __name__ == "__main__":
    print("--- Without Facade (client manages everything) ---")
    print(pay_without_facade("1111222233334444", 1200))

    print("\n--- With Facade (client calls one simple method) ---")
    facade = PaymentFacade()
    print(facade.pay("1111222233334444", 1200))
