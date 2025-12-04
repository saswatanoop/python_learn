"""
=====================================================
COMPOSITE PATTERN (Structural)
=====================================================

WHAT IS COMPOSITE?
------------------
Composite lets you treat **individual objects (Leaf)** and **groups of objects (Composite)**
uniformly by putting them under a common interface.

WHY USE COMPOSITE?
-------------------
- To represent tree structures (folders/files, UI components, menus, org chart).
- To allow clients to treat leaf and composite objects the same.
- To avoid `if isinstance(node, Leaf)` style code everywhere.

WITHOUT COMPOSITE (Problem)
---------------------------
Clients must check:
    if item is a leaf → do X
    if item is a group → iterate its children and do X

This creates branching logic, violates OCP, and spreads structure awareness everywhere.

WITH COMPOSITE (Solution)
-------------------------
Define a Component interface (e.g., render(), get_size()).
Leaf implements it.
Composite implements it by delegating to its children.

Clients do:
    root.render()
and don’t care if root is a file or a folder.

SOLID MAPPING
-------------
- SRP: Leaf and Composite separate concerns; Composite handles only group behavior.
- OCP: Add new Leaves or Composites without modifying existing code.
- DIP: Client depends on Component abstraction, not concrete leaves or composites.

COMMON USE CASES
----------------
- File system (Folder + File)
- UI hierarchy (Container + Button/Label/etc)
- Company org chart (Manager + Employee)
- Expression Trees (AddNode, MultiplyNode, ConstantNode)
- Menu systems

=====================================================
CODE: WITHOUT COMPOSITE + WITH COMPOSITE
=====================================================
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


# =====================================================
# 1) WITHOUT COMPOSITE (the problem)
# =====================================================

class FileNoComposite:
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self.size = size


class FolderNoComposite:
    def __init__(self, name: str) -> None:
        self.name = name
        self.children: List[object] = []  # holds files & folders

    def add(self, item) -> None:
        self.children.append(item)


def get_total_size_no_composite(item) -> int:
    """
    Problem: must inspect the type of item.
    This logic is duplicated everywhere.
    """
    if isinstance(item, FileNoComposite):
        return item.size
    elif isinstance(item, FolderNoComposite):
        return sum(get_total_size_no_composite(child) for child in item.children)
    else:
        raise TypeError("Unknown item")


# =====================================================
# 2) WITH COMPOSITE PATTERN (solution)
# =====================================================

# -------------------------
# COMPONENT INTERFACE
# -------------------------
class FileSystemComponent(ABC):
    @abstractmethod
    def get_size(self) -> int:
        pass


# -------------------------
# LEAF
# -------------------------
class File(FileSystemComponent):
    def __init__(self, name: str, size: int) -> None:
        self.name = name
        self._size = size

    def get_size(self) -> int:
        return self._size


# -------------------------
# COMPOSITE
# -------------------------
class Folder(FileSystemComponent):
    def __init__(self, name: str) -> None:
        self.name = name
        self._children: List[FileSystemComponent] = []

    def add(self, component: FileSystemComponent) -> None:
        self._children.append(component)

    def get_size(self) -> int:
        # Composite delegates behavior to children
        return sum(child.get_size() for child in self._children)


# =====================================================
# DEMO
# =====================================================
if __name__ == "__main__":
    print("--- Without Composite (type checking everywhere) ---")
    f1 = FileNoComposite("a.txt", 120)
    f2 = FileNoComposite("b.txt", 300)
    folder = FolderNoComposite("docs")
    folder.add(f1)
    folder.add(f2)
    print("Total:", get_total_size_no_composite(folder))

    print("\n--- With Composite (uniform treatment) ---")
    root = Folder("root")
    root.add(File("file1.txt", 120))
    root.add(File("file2.txt", 300))

    sub = Folder("subfolder")
    sub.add(File("image.png", 800))
    sub.add(File("video.mp4", 2000))

    root.add(sub)

    print("Total size:", root.get_size())
    # No branching logic, no isinstance checks, client just calls get_size()
