"""
=====================================================
OBSERVER PATTERN (Behavioral)
=====================================================

WHAT IS OBSERVER?
-----------------
Observer defines a one-to-many dependency between objects so that when
one object (the Subject) changes state, all its dependents (Observers)
are automatically notified and updated.

WHY USE OBSERVER?
-----------------
- Decouples subject from observers: subject doesn't need concrete observer types.
- Supports event-driven architectures and publish/subscribe semantics.
- Useful in UI frameworks, event buses, caching invalidation, and reactive systems.

CORE PARTS
----------
- Subject: maintains list of observers and notifies them on state changes.
- Observer (interface): defines update(notification) method.
- ConcreteObserver: implements reaction logic.
- Clients register/unregister observers with the subject.

WHEN TO USE
-----------
- UI: view updates when model changes.
- Event systems: many components react to events from a source.
- Cache invalidation: multiple caches update when source data changes.
- Logging/monitoring: many listeners for single event stream.

SOLID MAPPING
-------------
- SRP: Subject focuses on state change & notification; observers focus on reaction.
- OCP: Add new observers without changing subject.
- DIP: Subject depends on Observer abstraction, not concrete observers.

CAUTIONS
--------
- Can cause memory leaks if observers aren't unregistered (use weak refs where needed).
- Can create cascading updates or event storms if not designed carefully.
- Consider thread-safety when subject and observers operate across threads.

=====================================================
CODE: WITHOUT OBSERVER + WITH OBSERVER
=====================================================
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol, List, Any


# =====================================================
# 1) WITHOUT OBSERVER (THE PROBLEM)
# =====================================================

class StockTickerDirect:
    """
    Problem: tight coupling. Every time price changes, the publisher must
    know and call each listener explicitly. Adding new listeners requires
    modifying publisher code.
    """
    def __init__(self) -> None:
        self.price = 0.0

    def update_price_and_notify(self, new_price: float) -> None:
        # imagine these are concrete listeners hardcoded here:
        self.price = new_price
        # direct, manual notifications (bad: tightly coupled)
        print(f"[Direct] Price updated to {self.price}. Notifying trading engine...")
        print(f"[Direct] Price updated to {self.price}. Notifying alert system...")
        # adding another listener would require changing this method


# =====================================================
# 2) OBSERVER PATTERN (SOLUTION)
# =====================================================

class Observer(ABC):
    """Observer interface: implement update(subject, info)."""
    @abstractmethod
    def update(self, subject: "Subject", info: Any = None) -> None:
        pass


class Subject:
    """
    Subject maintains observers and notifies them on changes.
    """

    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, info: Any = None) -> None:
        for obs in list(self._observers):
            obs.update(self, info)


# -------- Concrete Subject --------
class StockTicker(Subject):
    def __init__(self, symbol: str) -> None:
        super().__init__()
        self.symbol = symbol
        self._price: float = 0.0

    @property
    def price(self) -> float:
        return self._price

    def set_price(self, new_price: float) -> None:
        self._price = new_price
        # notify observers with an optional payload (e.g., price)
        self.notify({"symbol": self.symbol, "price": self._price})


# -------- Concrete Observers --------
class TradingEngine(Observer):
    def update(self, subject: Subject, info: Any = None) -> None:
        # react to price change: make trading decisions
        if info and info.get("price") is not None:
            price = info["price"]
            print(f"[TradingEngine] {info['symbol']} new price {price}. Evaluating orders.")


class AlertService(Observer):
    def __init__(self, threshold: float) -> None:
        self.threshold = threshold

    def update(self, subject: Subject, info: Any = None) -> None:
        if info and info.get("price") is not None:
            price = info["price"]
            if price > self.threshold:
                print(f"[AlertService] ALERT: {info['symbol']} price {price} > {self.threshold}")


class LoggerObserver(Observer):
    def update(self, subject: Subject, info: Any = None) -> None:
        print(f"[Logger] Event from {getattr(subject, 'symbol', 'subject')}: {info}")


# =====================================================
# DEMO / USAGE
# =====================================================
if __name__ == "__main__":
    print("--- Problem (without Observer) ---")
    direct = StockTickerDirect()
    direct.update_price_and_notify(101.5)

    print("\n--- Observer Pattern (decoupled) ---")
    ticker = StockTicker("ACME")
    trading = TradingEngine()
    alert = AlertService(threshold=150.0)
    logger = LoggerObserver()

    # attach observers (client code decides who listens)
    ticker.attach(trading)
    ticker.attach(alert)
    ticker.attach(logger)

    # price updates automatically notify all observers
    ticker.set_price(120.0)
    print("---")
    ticker.set_price(160.0)

    # detach observer when no longer interested
    ticker.detach(alert)
    print("--- After detaching AlertService ---")
    ticker.set_price(170.0)
