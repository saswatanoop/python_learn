"""
=====================================================
ADAPTER PATTERN (Structural)
=====================================================

WHAT IS ADAPTER?
----------------
Adapter converts the interface of a class (the Adaptee) into another interface
the client expects (the Target). It lets classes with incompatible interfaces
work together without changing their source code.

WHY USE ADAPTER?
----------------
- Integrate third-party or legacy code with your current system.
- Avoid changing existing client code when underlying APIs differ.
- Keep client code dependent on a stable target interface.

TWO COMMON VARIANTS
-------------------
- Object Adapter (composition): Adapter holds a reference to the Adaptee.
- Class Adapter (inheritance): less common in Python; usually use composition.

WHEN TO USE
-----------
- A library provides a useful class but with a different method signature.
- You must support multiple third-party implementations behind a single interface.
- You want to avoid rippling changes when swapping vendors.

SOLID MAPPING
-------------
- SRP: Adapter has single responsibility — translate calls between interfaces.
- OCP: Add new adapters for new Adaptees without modifying clients.
- DIP: Clients depend on the Target abstraction, not concrete Adaptee types.

COMMON PITFALLS
---------------
- Over-adapting: don't adapt trivial differences; sometimes a thin wrapper suffices.
- Performance: adapters add a small call indirection (usually negligible).
- Leaky abstraction: adapter should not expose Adaptee details to clients.

=====================================================
CODE: Problem (without adapter) + Adapter solution
=====================================================
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


# -------------------------
# TARGET INTERFACE (what client expects)
# -------------------------
class PaymentStrategy(ABC):
    """
    Client code depends on this interface.
    It expects a float amount in rupees and a 'pay' method.
    """

    @abstractmethod
    def pay(self, amount: float) -> str:
        pass


# -------------------------
# ADAPTEE (third-party / legacy library)
# -------------------------
@dataclass
class LegacyGateway:
    """
    A legacy payment gateway that the vendor provides.
    It only accepts integer paise (cents) and exposes a different method name.
    We cannot modify this class (assume third-party).
    """

    merchant_id: str

    def send_payment_in_paise(self, amount_paise: int) -> str:
        # Imagine a complex vendor call here
        return f"LegacyGateway({self.merchant_id}): paid {amount_paise} paise"


# -------------------------
# PROBLEM: WITHOUT ADAPTER
# -------------------------
def pay_without_adapter():
    """
    Client code has to know legacy API details or wrap conditional logic.
    This creates coupling and spreads adaptee-specific knowledge.
    """
    gateway = LegacyGateway(merchant_id="M-001")
    # client must convert rupees->paise and call the vendor-specific method
    amount_rupees = 123.45
    amount_paise = int(round(amount_rupees * 100))
    return gateway.send_payment_in_paise(amount_paise)


# -------------------------
# SOLUTION: OBJECT ADAPTER
# -------------------------
class LegacyGatewayAdapter(PaymentStrategy):
    """
    Adapter implements the Target (PaymentStrategy) and translates calls
    to the LegacyGateway (Adaptee). Uses composition.
    """

    def __init__(self, legacy_gateway: LegacyGateway) -> None:
        self._gateway = legacy_gateway

    def pay(self, amount: float) -> str:
        # translate float rupees to integer paise expected by legacy API
        amount_paise = int(round(amount * 100))
        # call the adaptee and return a result consistent with PaymentStrategy
        return self._gateway.send_payment_in_paise(amount_paise)


# -------------------------
# ALTERNATIVE: SMALL WRAPPER (when adaptation is trivial)
# -------------------------
class ThinWrapper(PaymentStrategy):
    """
    Sometimes a tiny wrapper without elaborate logic is enough.
    Prefer this when the interface difference is minimal.
    """

    def __init__(self, legacy_gateway: LegacyGateway) -> None:
        self._gateway = legacy_gateway

    def pay(self, amount: float) -> str:
        return self._gateway.send_payment_in_paise(int(round(amount * 100)))


# -------------------------
# DEMO / USAGE
# -------------------------
if __name__ == "__main__":
    print("--- Problem without Adapter (client knows legacy API) ---")
    print(pay_without_adapter())  # client had to convert and call vendor method

    print("\n--- Adapter (clean client) ---")
    legacy = LegacyGateway(merchant_id="M-002")
    adapter = LegacyGatewayAdapter(legacy)
    # client uses the stable PaymentStrategy interface and doesn't care about vendor details
    print(adapter.pay(250.75))

    print("\n--- Thin wrapper (when trivial) ---")
    wrapper = ThinWrapper(legacy)
    print(wrapper.pay(10.0))
