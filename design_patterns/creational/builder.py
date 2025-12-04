"""
=====================================================
BUILDER PATTERN (Creational)
=====================================================

WHAT IS BUILDER?
----------------
Builder separates the construction of a complex object from its representation.
It allows creating different representations (variations) of a product using the same construction process (director). 
Useful when an object has many optional parameters or construction involves several steps.

WHY USE BUILDER?
----------------
- Avoids telescoping constructors (many parameters). 
- Keeps construction code readable and maintainable.
- Allows constructing different product variants using the same process.
- Good when building involves multiple steps or complex orchestration.

WHEN TO USE
-----------
- Product has many optional fields.
- Construction is multi-step or conditional.
- You want to hide complex construction from client code.
- You want immutable final objects created step-by-step.

SOLID MAPPING
-------------
- SRP: Builder has single responsibility — constructing a product.
- OCP: Add new builders for new product variants without changing director.
- DIP: Director depends on Builder abstraction, not concrete builders.

WHEN NOT TO USE
---------------
- For trivial object creation (simple dataclass) — overkill.
- When product creation is simple and doesn’t require multi-step orchestration.
- When client needs to mutate product frequently; Builder is for one-time, clear construction.

IMPLEMENTATION NOTES
--------------------
- Use an abstract Builder (ABC) declaring step methods and a method to return the product.
- Concrete builders implement steps and maintain the product state during construction.
- Director is optional: client can call builder steps directly (fluent builders).
- For Pythonic usage, fluent builder methods or factory functions are also common.
"""

# builder_examples.py
from dataclasses import dataclass
from typing import Optional


# ------------------------
# Example WITHOUT Builder
# ------------------------
# Problem: many optional fields lead to long constructors or unclear calls.
@dataclass
class UserProfile:
    username: str
    email: str
    age: Optional[int] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    location: Optional[str] = None
    newsletter_opt_in: bool = False

# Call sites become unclear:
# - Which argument is which when many positional args are used?
# - Using many keywords is verbose and repetitive.
u1 = UserProfile(
    username="alice",
    email="alice@example.com",
    age=30,
    bio="Loves hiking",
    avatar_url="http://...",
    location="Bengaluru",
    newsletter_opt_in=True,
)
# Or with defaults, but still long:
u2 = UserProfile("bob", "bob@example.com")  # okay for small cases


# ------------------------
# Example WITH Fluent Builder
# ------------------------
# Benefits:
# - Chainable .with_xxx(...) returning self
# - Only required field(s) enforced at build time
# - Clear, readable call sites

@dataclass(frozen=True)
class UserProfileBuilt:
    username: str
    email: str
    age: Optional[int]
    bio: Optional[str]
    avatar_url: Optional[str]
    location: Optional[str]
    newsletter_opt_in: bool


class UserProfileBuilder:
    def __init__(self, username: str, email: str) -> None:
        # required fields provided in ctor; optional via chainable setters
        self._username = username
        self._email = email
        self._age: Optional[int] = None
        self._bio: Optional[str] = None
        self._avatar_url: Optional[str] = None
        self._location: Optional[str] = None
        self._newsletter_opt_in: bool = False

    # chainable setters — each returns self
    def with_age(self, age: int) -> "UserProfileBuilder":
        self._age = age
        return self

    def with_bio(self, bio: str) -> "UserProfileBuilder":
        self._bio = bio
        return self

    def with_avatar(self, url: str) -> "UserProfileBuilder":
        self._avatar_url = url
        return self

    def with_location(self, loc: str) -> "UserProfileBuilder":
        self._location = loc
        return self

    def opt_in_newsletter(self) -> "UserProfileBuilder":
        self._newsletter_opt_in = True
        return self

    # final build method returns the immutable product
    def build(self) -> UserProfileBuilt:
        # optional: validation before creating the product
        if "@" not in self._email:
            raise ValueError("invalid email")
        return UserProfileBuilt(
            username=self._username,
            email=self._email,
            age=self._age,
            bio=self._bio,
            avatar_url=self._avatar_url,
            location=self._location,
            newsletter_opt_in=self._newsletter_opt_in,
        )


# ------------------------
# Usage / demonstration
# ------------------------
if __name__ == "__main__":
    # without builder (verbose but straightforward)
    print(u1)

    # with fluent builder (readable, only set what you need)
    profile = (
        UserProfileBuilder("charlie", "charlie@example.com")
        .with_age(28)
        .with_bio("Pythonista")
        .with_location("Mumbai")
        .opt_in_newsletter()
        .build()
    )
    print(profile)

    # minimal usage with builder (only required fields)
    minimal = UserProfileBuilder("diana", "diana@example.com").build()
    print(minimal)
