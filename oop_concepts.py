"""
OOP Principles (Python)

1. Abstraction:
   - Hides unnecessary implementation details; exposes only essential behavior.
   - Achieved via methods, interfaces, and abstract classes (abc module).
   - Encapsulation helps implement abstraction.

2. Encapsulation:
   - Bundles data + behavior inside a class.
   - Controls access via public / protected / private naming conventions.
   - Use @property for controlled access.

3. Inheritance:
   - Child class reuses and extends behavior of a parent class.
   - Models an "is-a" relationship.
   - Enables code reuse and polymorphism.

4. Polymorphism:
   - Same method name behaves differently based on the object.
   - Achieved through method overriding in inheritance.
   - Works naturally with lists of mixed subclasses.

Design Concepts:

Coupling:
   - Degree of dependency between components.
   - Low coupling = easier maintenance and flexibility.

Cohesion:
   - How focused a class/module is on a single purpose.
   - High cohesion = clearer and more maintainable code.

Abstract Classes:
   - Cannot be instantiated.
   - Define required methods using @abstractmethod.
   - Subclasses must implement abstract methods.

Composition:
   - Building complex objects using simpler ones.
   - Represents a "has-a" relationship (e.g., Car has-a Engine).
   - Preferred over deep inheritance for flexibility.

MRO (Method Resolution Order):
   - Defines the order Python searches for attributes/methods.
   - Uses the C3 Linearization algorithm.
   - Crucial in multiple inheritance.
   - View MRO using:
         ClassName.mro()
         or ClassName.__mro__
   - Search order:
         1) Class itself
         2) Left-to-right base classes
         3) Each parent’s MRO
         4) No class repeated
"""


# ------------------------------------------------
# 1. Abstraction Example (Abstract Class)
# ------------------------------------------------
from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def pay(self, amount):
        pass  # hides implementation

class CreditCardPayment(Payment):
    def pay(self, amount):
        return f"Paid {amount} via Credit Card"

class UpiPayment(Payment):
    def pay(self, amount):
        return f"Paid {amount} via UPI"


# ------------------------------------------------
# 2. Encapsulation Example (public/protected/private)
# ------------------------------------------------
class Account:
    def __init__(self, owner, balance):
        self.owner = owner          # public
        self._balance = balance     # protected
        self.__pin = 1234           # private (name-mangled)

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value >= 0:
            self._balance = value


# ------------------------------------------------
# 3. Inheritance Example
# ------------------------------------------------
class Animal:
    def speak(self):
        return "Some animal sound"

class Dog(Animal):
    def speak(self):
        return "Woof!"

class Cat(Animal):
    def speak(self):
        return "Meow!"


# ------------------------------------------------
# 4. Polymorphism Example (same method name)
# ------------------------------------------------
animals = [Dog(), Cat(), Animal()]
for a in animals:
    print(a.speak())


# ------------------------------------------------
# Composition Example (has-a relationship)
# ------------------------------------------------
class Engine:
    def start(self):
        return "Engine started"

class Car:
    def __init__(self):
        self.engine = Engine()  # Car has-a Engine

    def drive(self):
        return self.engine.start() + " → Car driving"


# ------------------------------------------------
# MRO Example (multiple inheritance)
# ------------------------------------------------
class A:
    def process(self):
        return "A"

class B(A):
    def process(self):
        return "B → " + super().process()

class C(A):
    def process(self):
        return "C → " + super().process()

class D(B, C):  # MRO: D → B → C → A → object
    pass

d = D()
print(d.process())       # B → C → A
print(D.mro())           # shows the linearized MRO
