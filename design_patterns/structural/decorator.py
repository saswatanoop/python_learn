"""
=====================================================
DECORATOR PATTERN (Structural)
=====================================================

WHAT IS DECORATOR?
------------------
Decorator adds behavior *dynamically* to an object without modifying
its class. It wraps an existing object inside another object.

This avoids subclass explosion and keeps behavior flexible at runtime.

WHY USE DECORATOR?
------------------
- Want to add optional features to objects without changing their class.
- Want combinations of features without creating 2^N subclasses.
- Want runtime, pluggable augmentations (logging, caching, auth, compression).

Common Real Uses:
- Logging decorators
- Caching decorators
- Authorization decorators
- Compression/Encryption wrappers
- Stream decorators (like Java IO streams)
- Middleware patterns

PROBLEM DECORATOR SOLVES
------------------------
Without Decorator, adding variations leads to class explosion:

    Coffee
    CoffeeWithMilk
    CoffeeWithSugar
    CoffeeWithMilkAndSugar
    CoffeeWithCream
    CoffeeWithCreamAndSugar
    ...

Too many subclasses → violates SRP, OCP, becomes unmaintainable.

Decorator allows:

    base = SimpleCoffee()
    coffee = MilkDecorator(SugarDecorator(base))

Clean, flexible, avoid inheritance explosion.

SOLID MAPPING
-------------
- SRP: Each decorator has single responsibility (single enhancement).
- OCP: Add new decorators without modifying existing code.
- DIP: Client depends on Component interface.

WHEN NOT TO USE
---------------
- When behavior doesn't need runtime flexibility.
- When simple subclassing is enough.
- When wrapping adds unnecessary complexity.

=====================================================
CODE: WITHOUT DECORATOR + WITH DECORATOR
=====================================================
"""

from __future__ import annotations
from abc import ABC, abstractmethod


# =====================================================
# 1) WITHOUT DECORATOR (the problem: many subclasses)
# =====================================================

class Coffee:
    def cost(self) -> float:
        return 50.0  # basic coffee

# Now every variation becomes a separate subclass:

class CoffeeWithMilk(Coffee):
    def cost(self) -> float:
        return super().cost() + 10.0

class CoffeeWithSugar(Coffee):
    def cost(self) -> float:
        return super().cost() + 5.0

class CoffeeWithMilkAndSugar(Coffee):
    def cost(self) -> float:
        return super().cost() + 10.0 + 5.0

# Adding cream creates more subclasses → combinatorial explosion.


# =====================================================
# 2) WITH DECORATOR (clean, scalable solution)
# =====================================================

# -------------------------
# COMPONENT INTERFACE
# -------------------------
class CoffeeComponent(ABC):
    @abstractmethod
    def cost(self) -> float:
        pass


# -------------------------
# CONCRETE COMPONENT
# -------------------------
class SimpleCoffee(CoffeeComponent):
    def cost(self) -> float:
        return 50.0


# -------------------------
# BASE DECORATOR
# -------------------------
class CoffeeDecorator(CoffeeComponent):
    """
    Decorator implements the same interface and wraps another component.
    """

    def __init__(self, component: CoffeeComponent) -> None:
        self._component = component

    def cost(self) -> float:
        return self._component.cost()


# -------------------------
# CONCRETE DECORATORS
# -------------------------
class MilkDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 10.0


class SugarDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 5.0


class CreamDecorator(CoffeeDecorator):
    def cost(self) -> float:
        return super().cost() + 15.0


# =====================================================
# DEMO
# =====================================================
if __name__ == "__main__":
    print("--- Without Decorator (subclass explosion) ---")
    plain = Coffee()
    print("Plain coffee:", plain.cost())

    milk = CoffeeWithMilk()
    print("Milk coffee:", milk.cost())

    mix = CoffeeWithMilkAndSugar()
    print("Milk + Sugar coffee:", mix.cost())

    print("\n--- With Decorator (flexible composition) ---")
    base = SimpleCoffee()

    coffee1 = MilkDecorator(base)
    print("Coffee + Milk:", coffee1.cost())

    coffee2 = SugarDecorator(MilkDecorator(base))
    print("Coffee + Milk + Sugar:", coffee2.cost())

    coffee3 = CreamDecorator(SugarDecorator(MilkDecorator(base)))
    print("Coffee + Milk + Sugar + Cream:", coffee3.cost())
