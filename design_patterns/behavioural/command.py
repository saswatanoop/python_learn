"""
=====================================================
COMMAND PATTERN (Behavioral)
=====================================================

WHAT IS COMMAND?
----------------
Encapsulate a request as an object (a Command). The Command object
holds all information needed to execute an action (method, receiver,
parameters). Invokers call commands without knowing details of the action.
Receivers perform the actual work.

WHY USE COMMAND?
----------------
- Decouple sender (Invoker) from the receiver (who performs the action).
- Enable queuing, logging, retries, and undo/redo.
- Represent operations as objects (passable, storable, serializable).
- Support macro commands (batching multiple commands).

COMMON PARTS
------------
- Command (interface): execute() and optionally undo()
- ConcreteCommand: binds Receiver + required parameters
- Receiver: the domain object that performs the actual operation
- Invoker: asks command to execute; may keep history for undo or a queue for scheduling
- Client: creates commands and gives them to invoker

WHEN TO USE
-----------
- GUI buttons (click = command)
- Undo/redo systems
- Job queues, task scheduling
- Remote procedure invocation / network requests wrapped as objects
- Macro/batched operations

SOLID BENEFITS
--------------
- SRP: Command single responsibility — represent an action
- OCP: Add new commands without changing invoker/receiver code
- DIP: Invoker depends on Command abstraction, not concrete actions

THIS FILE SHOWS:
- Problem without Command
- Command implementation (with undo)
- MacroCommand (batch)
- Invoker with queue & history
=====================================================
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections import deque
from typing import List, Any, Optional


# =====================================================
# 1) WITHOUT COMMAND (THE PROBLEM)
# =====================================================

class Light:
    """Receiver: knows how to turn on/off a light."""
    def __init__(self) -> None:
        self._is_on = False

    def turn_on(self) -> str:
        self._is_on = True
        return "Light turned ON"

    def turn_off(self) -> str:
        self._is_on = False
        return "Light turned OFF"


def client_direct_control():
    """
    Client directly calls receiver methods. Problems:
    - Invoker (UI code) must know receiver methods
    - Hard to queue, log, undo or serialize actions
    """
    light = Light()
    print(light.turn_on())
    print(light.turn_off())


# =====================================================
# 2) COMMAND PATTERN (SOLUTION)
# =====================================================

class Command(ABC):
    """Command interface: execute and optional undo."""
    @abstractmethod
    def execute(self) -> Any:
        pass

    def undo(self) -> Any:
        """Optional undo; provide only if command is reversible."""
        raise NotImplementedError("Undo not implemented")


# -------- Concrete Commands --------

@dataclass
class TurnOnCommand(Command):
    receiver: Light

    def execute(self) -> str:
        return self.receiver.turn_on()

    def undo(self) -> str:
        # inverse operation for undo
        return self.receiver.turn_off()


@dataclass
class TurnOffCommand(Command):
    receiver: Light

    def execute(self) -> str:
        return self.receiver.turn_off()

    def undo(self) -> str:
        return self.receiver.turn_on()


# -------- MacroCommand (batch multiple commands) --------
class MacroCommand(Command):
    """
    Execute a list of commands in sequence. Undo reverses them in reverse order.
    Useful for batch operations or transactions.
    """
    def __init__(self, commands: Optional[List[Command]] = None) -> None:
        self._commands: List[Command] = list(commands) if commands else []

    def add(self, cmd: Command) -> None:
        self._commands.append(cmd)

    def execute(self) -> List[Any]:
        results = []
        for cmd in self._commands:
            results.append(cmd.execute())
        return results

    def undo(self) -> List[Any]:
        # undo in reverse
        results = []
        for cmd in reversed(self._commands):
            results.append(cmd.undo())
        return results


# =====================================================
# 3) INVOKER (queue + history for undo)
# =====================================================

class RemoteInvoker:
    """
    Invoker: receives Command objects and executes them.
    Keeps a history stack for undo and a queue for scheduled commands.
    """
    def __init__(self) -> None:
        self._history: List[Command] = []
        self._queue: deque[Command] = deque()

    def set_command(self, cmd: Command) -> None:
        """Execute immediately and record in history if undoable."""
        result = cmd.execute()
        # If undo is implemented, we'll record it (detect by method existence)
        if hasattr(cmd, "undo") and callable(getattr(cmd, "undo", None)):
            self._history.append(cmd)
        return result

    def queue_command(self, cmd: Command) -> None:
        """Enqueue a command to be executed later."""
        self._queue.append(cmd)

    def run_queue(self) -> List[Any]:
        """Execute all queued commands in FIFO order and add to history."""
        results = []
        while self._queue:
            cmd = self._queue.popleft()
            results.append(self.set_command(cmd))
        return results

    def undo_last(self) -> Any:
        """Undo the last executed command (if possible)."""
        if not self._history:
            return "Nothing to undo"
        last = self._history.pop()
        try:
            return last.undo()
        except NotImplementedError:
            return "Cannot undo this command"


# =====================================================
# DEMO / USAGE
# =====================================================

if __name__ == "__main__":
    print("--- Problem (no Command) ---")
    client_direct_control()

    print("\n--- Command Pattern (basic) ---")
    lamp = Light()
    on_cmd = TurnOnCommand(receiver=lamp)
    off_cmd = TurnOffCommand(receiver=lamp)

    invoker = RemoteInvoker()
    print("Execute ON:", invoker.set_command(on_cmd))
    print("Execute OFF:", invoker.set_command(off_cmd))

    print("\n--- Undo last (should turn ON) ---")
    print("Undo:", invoker.undo_last())

    print("\n--- Queueing commands and MacroCommand ---")
    # Queue single commands
    invoker.queue_command(on_cmd)
    invoker.queue_command(off_cmd)
    print("Run queue:", invoker.run_queue())

    # Macro: batch turn on then off (for illustration)
    macro = MacroCommand([TurnOnCommand(lamp), TurnOffCommand(lamp)])
    print("Macro execute:", macro.execute())
    print("Macro undo:", macro.undo())

"""
Notes:
- Commands are objects encapsulating an action and its receiver.
- Invoker handles command lifecycle: execute now, queue, or undo later.
- MacroCommand composes commands; useful for transactions or grouped operations.
- Undo requires concrete commands to implement inverse behavior; not all commands are reversible.
- Commands can be serialized (if parameters are serializable) and used to replay actions.
"""
