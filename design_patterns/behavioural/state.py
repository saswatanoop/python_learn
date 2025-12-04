"""
=====================================================
STATE PATTERN (Behavioral)
=====================================================

WHAT IS STATE?
--------------
State allows an object to alter its behavior when its internal state changes.
It encapsulates state-specific behavior into separate state classes and
the context delegates requests to the current state.

WHY USE STATE?
--------------
- Avoids large conditional (if/elif or switch) blocks that check state.
- Each state class encapsulates behavior and transitions, improving clarity.
- Makes adding new states easier (OCP) and keeps Context lean (SRP).
- Useful for workflows, finite-state machines, UI components, protocol handlers.

WHEN TO USE
-----------
- Complex workflows with distinct state-dependent behavior (order lifecycle, connection states, document editing states).
- When behavior changes frequently based on internal state.
- When transitions and allowed operations differ per state.

COMMON PARTS
------------
- State (interface): methods for operations that vary by state.
- ConcreteState: implement behavior and possibly trigger transitions.
- Context: holds a reference to current State and delegates operations.

SOLID MAPPING
-------------
- SRP: move state-specific logic into state classes.
- OCP: add new states without changing existing ones.
- DIP: Context depends on State abstraction, not concrete states.

CAUTIONS
--------
- Avoid putting too much transition logic in Context — prefer state classes.
- Keep states lightweight and cohesive.
- For complex graphs consider using a state machine library.

THIS FILE: 
- Problem without State
- State Pattern implementation for an Order lifecycle (Created -> Paid -> Shipped -> Delivered / Cancelled)
=====================================================
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


# =====================================================
# 1) WITHOUT STATE (THE PROBLEM)
# =====================================================

def process_order_without_state(order_status: str, action: str) -> str:
    """
    Example of a fragile if/elif implementation.
    As states or actions grow, this becomes unreadable and error-prone.
    """
    if order_status == "created":
        if action == "pay":
            return "transition to paid"
        if action == "cancel":
            return "transition to cancelled"
        return "invalid action"
    elif order_status == "paid":
        if action == "ship":
            return "transition to shipped"
        if action == "refund":
            return "transition to refunded"
        return "invalid action"
    elif order_status == "shipped":
        if action == "deliver":
            return "transition to delivered"
        return "invalid action"
    return "unknown status"


# =====================================================
# 2) STATE PATTERN (SOLUTION)
# =====================================================

class OrderState(ABC):
    """
    State interface: defines operations that vary by concrete state.
    Methods return next state or raise when operation is invalid.
    """

    @abstractmethod
    def pay(self, order: "Order") -> None:
        pass

    @abstractmethod
    def ship(self, order: "Order") -> None:
        pass

    @abstractmethod
    def deliver(self, order: "Order") -> None:
        pass

    @abstractmethod
    def cancel(self, order: "Order") -> None:
        pass


# -------- Concrete States --------

class CreatedState(OrderState):
    def pay(self, order: "Order") -> None:
        order._set_state(PaidState())
        order.log("Payment received; state -> PAID")

    def ship(self, order: "Order") -> None:
        order.log("Cannot ship: payment pending")

    def deliver(self, order: "Order") -> None:
        order.log("Cannot deliver: not shipped")

    def cancel(self, order: "Order") -> None:
        order._set_state(CancelledState())
        order.log("Order cancelled; state -> CANCELLED")


class PaidState(OrderState):
    def pay(self, order: "Order") -> None:
        order.log("Already paid")

    def ship(self, order: "Order") -> None:
        order._set_state(ShippedState())
        order.log("Order shipped; state -> SHIPPED")

    def deliver(self, order: "Order") -> None:
        order.log("Cannot deliver: not shipped yet")

    def cancel(self, order: "Order") -> None:
        order._set_state(CancelledState())
        order.log("Order cancelled; state -> CANCELLED (refund required)")


class ShippedState(OrderState):
    def pay(self, order: "Order") -> None:
        order.log("Already paid and shipped")

    def ship(self, order: "Order") -> None:
        order.log("Already shipped")

    def deliver(self, order: "Order") -> None:
        order._set_state(DeliveredState())
        order.log("Order delivered; state -> DELIVERED")

    def cancel(self, order: "Order") -> None:
        order.log("Cannot cancel: already shipped")


class DeliveredState(OrderState):
    def pay(self, order: "Order") -> None:
        order.log("Already completed")

    def ship(self, order: "Order") -> None:
        order.log("Already delivered")

    def deliver(self, order: "Order") -> None:
        order.log("Already delivered")

    def cancel(self, order: "Order") -> None:
        order.log("Cannot cancel: already delivered")


class CancelledState(OrderState):
    def pay(self, order: "Order") -> None:
        order.log("Cannot pay: order cancelled")

    def ship(self, order: "Order") -> None:
        order.log("Cannot ship: order cancelled")

    def deliver(self, order: "Order") -> None:
        order.log("Cannot deliver: order cancelled")

    def cancel(self, order: "Order") -> None:
        order.log("Already cancelled")


# -------- Context --------

@dataclass
class Order:
    order_id: str
    _state: OrderState = CreatedState()

    def _set_state(self, state: OrderState) -> None:
        self._state = state

    def log(self, message: str) -> None:
        print(f"[Order {self.order_id}] {message}")

    # Operations delegate to current state
    def pay(self) -> None:
        self._state.pay(self)

    def ship(self) -> None:
        self._state.ship(self)

    def deliver(self) -> None:
        self._state.deliver(self)

    def cancel(self) -> None:
        self._state.cancel(self)

    def status(self) -> str:
        return self._state.__class__.__name__.replace("State", "").upper()


# =====================================================
# DEMO / USAGE
# =====================================================
if __name__ == "__main__":
    print("--- Problem without state (fragile if/elif) ---")
    print(process_order_without_state("created", "pay"))
    print(process_order_without_state("paid", "ship"))
    print(process_order_without_state("shipped", "deliver"))

    print("\n--- State Pattern (clean behavior delegation) ---")
    order = Order(order_id="A100")
    print("Initial status:", order.status())

    order.pay()    # transition to Paid
    print("Status:", order.status())

    order.ship()   # transition to Shipped
    print("Status:", order.status())

    order.deliver()  # transition to Delivered
    print("Status:", order.status())

    # try invalid transitions
    order.cancel()  # cannot cancel after delivered
    print("Final status:", order.status())
