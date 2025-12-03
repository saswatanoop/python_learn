

"""
SOLID Principles (Concise Notes)

S — Single Responsibility Principle (SRP): A class should have one reason to change.
    - A class should change for only one actor’s needs.
    - If two different stakeholders require modifications, split the class.

O — Open/Closed Principle (OCP): Open for extension, closed for modification.
    - Add new behavior via subclasses, not by editing existing code.

L — Liskov Substitution Principle (LSP): Subclasses must be usable wherever the parent is expected.
    - No breaking or changing expected behavior.

I — Interface Segregation Principle (ISP): Clients should not depend on methods they don't use.
    - Prefer small, specific interfaces over large, general ones.

D — Dependency Inversion Principle (DIP): High-level code should depend on abstractions, not concrete classes.
    - Use abstract base classes (ABCs) for loose coupling and flexibility.


Mini Project: Notification System demonstrating SOLID (Python) using ABCs

- SRP: classes have single responsibilities (format, send, persist)
- OCP: add new Sender subclasses to extend behaviour w/o modifying service
- LSP: concrete senders substitute abstract Sender safely
- ISP: small, focused interfaces (Formatter, Sender, Repository)
- DIP: NotificationService depends on abstractions (ABCs), not concrete classes
"""


from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List


# ---------------------
# Domain models
# ---------------------
class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Message:
    to: str
    body: str
    priority: Priority = Priority.MEDIUM


# ---------------------
# Abstractions as ABCs (DIP, ISP)
# ---------------------
class Formatter(ABC):
    @abstractmethod
    def format(self, msg: Message) -> str:
        """Return formatted payload for the message"""
        pass


class Sender(ABC):
    @abstractmethod
    def send(self, recipient: str, payload: str) -> bool:
        """Send payload to recipient. Return True on success."""
        pass


class Repository(ABC):
    @abstractmethod
    def save(self, msg: Message) -> None:
        """Persist message"""
        pass


# ---------------------
# Implementations (SRP)
# ---------------------
class SimpleFormatter(Formatter):
    def format(self, msg: Message) -> str:
        header = f"[{msg.priority.name}]"
        return f"{header} To: {msg.to} — {msg.body}"


class HTMLFormatter(Formatter):
    def format(self, msg: Message) -> str:
        return (
            f"<div class='msg'><b>{msg.priority.name}</b>"
            f"<p>{msg.body}</p><i>To: {msg.to}</i></div>"
        )


# ---------------------
# Concrete Senders (LSP - substitutable)
# ---------------------
class EmailSender(Sender):
    def send(self, recipient: str, payload: str) -> bool:
        print(f"[Email] -> {recipient}: {payload}")
        return True


class SMSSender(Sender):
    def send(self, recipient: str, payload: str) -> bool:
        print(f"[SMS] -> {recipient}: {payload}")
        return True


class PushSender(Sender):
    def send(self, recipient: str, payload: str) -> bool:
        print(f"[Push] -> {recipient}: {payload}")
        return True


# OCP: adding a new sender doesn't change NotificationService
class SlackSender(Sender):
    def send(self, recipient: str, payload: str) -> bool:
        print(f"[Slack] -> {recipient}: {payload}")
        return True


# ---------------------
# Repository (SRP)
# ---------------------
class InMemoryRepo(Repository):
    def __init__(self):
        self._store: List[Message] = []

    def save(self, msg: Message) -> None:
        self._store.append(msg)
        print(f"[Repo] Saved message for {msg.to} (priority={msg.priority.name})")

    def all(self) -> List[Message]:
        return list(self._store)


# ---------------------
# High-level module depends on abstractions -> DIP
# ---------------------
class NotificationService:
    """
    Depends on:
      - Formatter (Formatter ABC)
      - List[Sender] (Sender ABC)
      - Repository (Repository ABC)
    """
    def __init__(self, formatter: Formatter, senders: List[Sender], repo: Repository):
        self._formatter = formatter
        self._senders = senders
        self._repo = repo

    def notify(self, msg: Message) -> None:
        payload = self._formatter.format(msg)        # formatting delegated (SRP)
        for s in self._senders:
            ok = s.send(msg.to, payload)            # any Sender must implement send()
            if not ok:
                print(f"[Warning] sender {s} failed for {msg.to}")
        self._repo.save(msg)                         # persisting delegated (SRP)


# ---------------------
# Usage / Demo
# ---------------------
if __name__ == "__main__":
    formatter = SimpleFormatter()               # swap with HTMLFormatter if desired
    senders: List[Sender] = [EmailSender(), SMSSender()]
    repo = InMemoryRepo()

    service = NotificationService(formatter, senders, repo)

    m1 = Message(to="alice@example.com", body="Welcome aboard!", priority=Priority.HIGH)
    service.notify(m1)

    # OCP: extend behavior by adding a new sender at runtime (no change in NotificationService)
    service._senders.append(SlackSender())
    m2 = Message(to="team-channel", body="Deployment finished", priority=Priority.MEDIUM)
    service.notify(m2)

    print("\nStored messages:", repo.all())
