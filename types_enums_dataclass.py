"""
Type Hinting, Enums, and Data Classes (Python) - Concise Notes

Type Hinting (typing):
    - Adds expected types for variables, parameters, and return values.
    - Improves readability and static analysis (no runtime effect).
    - Common types: list[int], dict[str, int], tuple[int, int], set[str]
    - Optional[T] == T | None (Python 3.10+)
    - Callable[[A, B], R] → function type

Enums (enum.Enum):
    - Define named constant values.
    - Useful for states, categories, and choices.
    - Members are unique and comparable using "is".
    - Can be int-based or str-based and may contain methods.

Data Classes (dataclasses.dataclass):
    - Automatically generate __init__, __repr__, __eq__, etc.
    - Great for classes meant mainly to store data.
    - Options:
          frozen=True  → immutable
          order=True   → adds comparison methods
    - Supports default values and __post_init__ for validation.
"""

# ------------------------------------------------
# Type Hinting Examples
# ------------------------------------------------
from typing import List, Dict, Tuple, Optional, Callable


def greet(name: str) -> str:
    return f"Hello, {name}"


def add_numbers(a: int, b: int) -> int:
    return a + b


def get_user() -> Dict[str, int]:
    return {"age": 25}


def process_list(values: List[int]) -> List[int]:
    return [v * 2 for v in values]


def maybe_number(flag: bool) -> Optional[int]:
    return 10 if flag else None


def operate(func: Callable[[int, int], int]) -> int:
    return func(3, 4)


# ------------------------------------------------
# Enum Examples
# ------------------------------------------------
from enum import Enum


class Status(Enum):
    SUCCESS = 1
    ERROR = 2
    PENDING = 3


class Direction(str, Enum):
    NORTH = "north"
    SOUTH = "south"


# usage
print(Status.SUCCESS.name, Status.SUCCESS.value)
print(Direction.NORTH)


# ------------------------------------------------
# Data Class Examples
# ------------------------------------------------
from dataclasses import dataclass


@dataclass
class Point:
    x: int
    y: int


@dataclass
class User:
    name: str
    active: bool = True
    score: int = 0


@dataclass(frozen=True)
class Config:
    timeout: int


@dataclass
class Product:
    name: str
    price: float

    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")


# usage
p = Point(10, 20)
u = User("Alice")
cfg = Config(30)
item = Product("Laptop", 999.99)

print(p, u, cfg, item)
