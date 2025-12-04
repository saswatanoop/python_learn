"""
=====================================================
SINGLETON PATTERN (Creational)
=====================================================

WHAT IS SINGLETON?
------------------
Ensure a class has exactly one instance and provide a global access point to it.

WHY (and why not) use it?
-------------------------
Why:
- Manage a single shared resource (config, global registry, logger, DB connection pool).
- Ensure single point of control.

Why NOT:
- Often introduces global state and hidden dependencies → harder to test.
- Can violate SRP and DIP; usually considered an anti-pattern if overused.
- Prefer dependency injection (pass singletons explicitly) in testable systems.

COMMON WAYS TO IMPLEMENT (Python)
--------------------------------
1) Module-level instance (simplest and Pythonic)
2) Classic class with locking (thread-safe lazy init)
3) Metaclass-based singleton (compact, reusable)
Also: use frameworks/DI containers instead of singletons in large systems.

CAUTIONS
--------
- Prefer explicit injection over global singletons in most LLD.
- If using singleton, make thread-safety and lifecycle (close/dispose) explicit.
- Avoid using singleton for mutable global state.

=====================================================
CODE: 3 concise implementations + demo
=====================================================
"""

from __future__ import annotations
import threading
from dataclasses import dataclass
from typing import Optional


# =====================================================
# 1) MODULE-LEVEL SINGLETON (Pythonic & simplest)
# =====================================================
# Put this in module `config.py`:
#
#   DEFAULT_CONFIG = Config({...})
#
# Importers do:
#   from config import DEFAULT_CONFIG
#
# This is simple, thread-safe at import time, and idiomatic.
#
# Pros: simple, clear, testable by replacing module symbol in tests.
# Cons: instance created at import time (eager), not lazily initialized.

@dataclass
class AppConfig:
    env: str
    version: str


# Example module-level instance (would normally live in its own module)
DEFAULT_CONFIG = AppConfig(env="production", version="1.0.0")


# =====================================================
# 2) THREAD-SAFE LAZY SINGLETON (classic approach)
# =====================================================
class Logger:
    """Lazy, thread-safe singleton via class-level private state."""

    _instance: Optional["Logger"] = None
    _lock = threading.Lock()

    def __init__(self, prefix: str = "") -> None:
        # Danger: __init__ can be called multiple times if not careful.
        # Keep it idempotent or use __new__ for strict control.
        self.prefix = prefix

    @classmethod
    def instance(cls, prefix: str = "") -> "Logger":
        # Double-checked locking
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls(prefix=prefix)
        return cls._instance

    def log(self, message: str) -> None:
        print(f"{self.prefix}{message}")


# =====================================================
# 3) METACLASS-BASED SINGLETON (compact & reusable)
# =====================================================
class SingletonMeta(type):
    """Metaclass that makes any class a singleton."""
    _instances: dict[type, object] = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # thread-safe creation
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Cache(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._store = {}

    def set(self, k, v):
        self._store[k] = v

    def get(self, k, default=None):
        return self._store.get(k, default)


# =====================================================
# DEMO / USAGE
# =====================================================
if __name__ == "__main__":
    print("=== Module-level singleton ===")
    print("DEFAULT_CONFIG:", DEFAULT_CONFIG)

    print("\n=== Lazy Logger singleton ===")
    l1 = Logger.instance(prefix="[L1] ")
    l2 = Logger.instance(prefix="[L2] ")
    l1.log("hello from l1")
    l2.log("hello from l2")
    print("Same instance?", l1 is l2)  # True

    print("\n=== Metaclass Singleton (Cache) ===")
    c1 = Cache()
    c2 = Cache()
    c1.set("x", 42)
    print("c2.get('x'):", c2.get("x"))
    print("Same instance?", c1 is c2)

    # Note: metaclass-based creation uses __call__, so constructor args are only
    # used on first creation. Be careful: subsequent calls ignore different args.

"""
INTERVIEW TALKING POINTS
- Mention downsides: testability issues, hidden global state, lifecycle management.
- Prefer DI/explicit passing of shared instances when possible.
- If singleton is required:
  - prefer module-level singletons for simplicity,
  - use lazy creation with explicit locking if expensive to create,
  - metaclass is compact but be careful with constructor arguments and side-effects.
"""
