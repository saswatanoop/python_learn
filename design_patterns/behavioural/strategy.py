"""
=====================================================
STRATEGY PATTERN (Behavioral)
=====================================================

1) WHAT IS STRATEGY?
--------------------
    Strategy allows choosing an algorithm/behavior at runtime by
    encapsulating each behavior inside its own class.

    It removes big if/elif chains and replaces them with clean,
    pluggable strategy objects.

------------------------------------------------------
2) WHY IS IT USED?
------------------------------------------------------
    Without Strategy:
        if payment == "CARD": ...
        elif payment == "UPI": ...
        elif payment == "WALLET": ...
    This violates SRP, OCP and becomes hard to maintain.

    With Strategy:
        - Each behavior is isolated in its own class
        - You can plug in different strategies dynamically
        - Code becomes cleaner, testable, extensible

------------------------------------------------------
3) REAL-WORLD USE CASES
------------------------------------------------------
    - Payment methods (Card / UPI / Wallet)
    - Sorting algorithms
    - Pricing rules (festival, discount, loyalty)
    - Authentication types
    - Notification senders (SMS / Email / Push)
    - Routing algorithms
    - Recommendation engines

------------------------------------------------------
4) SOLID PRINCIPLES SATISFIED
------------------------------------------------------
    - SRP: Each concrete strategy has one responsibility: its algorithm.
    - OCP: Add new strategies without modifying existing classes.
    - DIP: PaymentProcessor depends on PaymentStrategy interface, not concrete types.

------------------------------------------------------
5) WHEN TO NOT USE STRATEGY
------------------------------------------------------
    - When there is only ONE behavior → overkill.
    - When behavior depends on internal object STATE → use State Pattern.
    - When strategy needs too much information → redesign context/strategy boundaries.

=====================================================
PYTHON IMPLEMENTATION (Using ABC Interface)
=====================================================
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


# ----------------------------------------------------
# STRATEGY INTERFACE
# ----------------------------------------------------
class PaymentStrategy(ABC):
    """Abstract interface for payment behaviors."""

    @abstractmethod
    def pay(self, amount: float) -> str:
        """Perform the payment and return a receipt string."""
        pass


# ----------------------------------------------------
# CONCRETE STRATEGIES
# ----------------------------------------------------

@dataclass
class CardPayment(PaymentStrategy):
    card_number: str

    def pay(self, amount: float) -> str:
        last4 = self.card_number[-4:]
        return f"Paid ₹{amount:.2f} using Card ****{last4}"


@dataclass
class UpiPayment(PaymentStrategy):
    upi_id: str

    def pay(self, amount: float) -> str:
        return f"Paid ₹{amount:.2f} using UPI {self.upi_id}"


@dataclass
class WalletPayment(PaymentStrategy):
    wallet: str

    def pay(self, amount: float) -> str:
        return f"Paid ₹{amount:.2f} using Wallet {self.wallet}"


# ----------------------------------------------------
# CONTEXT
# ----------------------------------------------------
class PaymentProcessor:
    """
    Context class that uses a PaymentStrategy.
    It does NOT know the concrete strategy type (DIP).
    """

    def __init__(self, strategy: PaymentStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PaymentStrategy):
        """Swap strategy at runtime."""
        self.strategy = strategy

    def process(self, amount: float) -> str:
        """Calls the selected strategy."""
        return self.strategy.pay(amount)


# ----------------------------------------------------
# EXAMPLE USAGE (Only runs when executed directly)
# ----------------------------------------------------
if __name__ == "__main__":
    processor = PaymentProcessor(CardPayment("1234567890123456"))
    print(processor.process(500))

    processor.set_strategy(UpiPayment("user@bank"))
    print(processor.process(250))

    processor.set_strategy(WalletPayment("PayFast"))
    print(processor.process(100))
