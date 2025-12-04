"""
=====================================================
FACTORY PATTERN (Creational)
=====================================================

WHAT IS FACTORY?
----------------
Factory Pattern moves object creation into a separate component so
the client never directly instantiates concrete classes.  
This improves maintainability, reduces coupling, and keeps the system open
for extension (OCP).

WHY USE FACTORY?
----------------
Without factory, you use many `if/elif` statements to decide which class
to instantiate. This violates:
- SRP (creation + usage mixed)
- OCP (add new product -> modify existing code)
- DIP (client depends on concrete classes)

Factory isolates creation and allows adding new product types without changing
client code.

VARIANTS
--------
1) Simple Factory (a function creating objects based on input)
   - Easy and pythonic, but still contains if/elif inside the factory.

2) Factory Method (abstract creator + concrete creators)
   - True design pattern.
   - Removes if/elif entirely.
   - Extensible: add new creators without modifying existing code.

WHEN TO USE FACTORY
-------------------
- When object creation varies based on conditions.
- When client should depend only on abstractions.
- When adding new product types is expected.
- When construction is complex or environment-specific.

SOLID PRINCIPLES SATISFIED
--------------------------
- SRP: Object creation isolated from usage.
- OCP: New product types added by adding new creators, not modifying old code.
- DIP: Client depends on product abstraction, never concrete classes.

WHEN NOT TO USE IT
------------------
- Simple direct instantiation is enough.
- Few product types, unlikely to change.
- Over-engineering for small scripts.

This file includes:
- Code WITHOUT factory (the problem)
- Simple Factory version
- Factory Method version (proper design pattern)
=====================================================
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


# =====================================================
# 1) WITHOUT FACTORY (THE PROBLEM)
# =====================================================

@dataclass
class PdfDocument:
    title: str
    content: str

    def render(self):
        return f"PDF: {self.title}\n{self.content}"


@dataclass
class HtmlDocument:
    title: str
    content: str

    def render(self):
        return f"<html><body><h1>{self.title}</h1>{self.content}</body></html>"


# client code manually selects which class to instantiate
def generate_document_without_factory(kind: str, title: str, content: str):
    """
    Problem:
    - if/elif grows as new types are added
    - violates OCP, SRP, DIP
    - client depends on concrete classes directly
    """
    if kind == "pdf":
        return PdfDocument(title, content)
    elif kind == "html":
        return HtmlDocument(title, content)
    else:
        raise ValueError("Unknown document type")


# =====================================================
# 2) SIMPLE FACTORY (FUNCTION-BASED)
# =====================================================

def create_document(kind: str, title: str, content: str):
    """
    Simple Factory:
    - client no longer instantiates concrete classes
    - creation is centralized
    - still uses if/elif internally → not fully OCP-compliant
    Useful for small projects, Python scripts.
    """
    kind = kind.lower()
    if kind == "pdf":
        return PdfDocument(title, content)
    elif kind == "html":
        return HtmlDocument(title, content)
    raise ValueError("Unknown document type")


# =====================================================
# 3) FACTORY METHOD (TRUE DESIGN PATTERN)
# =====================================================

# -------- PRODUCT INTERFACE --------
class Document(ABC):
    @abstractmethod
    def render(self) -> str:
        pass


# -------- CONCRETE PRODUCTS --------
@dataclass
class PdfDoc(Document):
    title: str
    content: str

    def render(self) -> str:
        return f"PDF: {self.title}\n{self.content}"


@dataclass
class HtmlDoc(Document):
    title: str
    content: str

    def render(self) -> str:
        return f"<html><body><h1>{self.title}</h1>{self.content}</body></html>"


# -------- CREATOR INTERFACE --------
class DocumentCreator(ABC):
    """
    Declares factory method `create_document`.
    Subclasses override it to decide which concrete product to make.
    """

    @abstractmethod
    def create_document(self, title: str, content: str) -> Document:
        pass

    # Optional helper: uses the product after creation
    def render_document(self, title: str, content: str) -> str:
        doc = self.create_document(title, content)
        return doc.render()


# -------- CONCRETE CREATORS --------
class PdfCreator(DocumentCreator):
    def create_document(self, title: str, content: str) -> Document:
        return PdfDoc(title, content)


class HtmlCreator(DocumentCreator):
    def create_document(self, title: str, content: str) -> Document:
        return HtmlDoc(title, content)


# =====================================================
# DEMO
# =====================================================
if __name__ == "__main__":
    print("--- WITHOUT FACTORY ---")
    doc1 = generate_document_without_factory("pdf", "Report", "Data")
    print(doc1.render())

    print("\n--- SIMPLE FACTORY ---")
    doc2 = create_document("html", "Home", "Welcome!")
    print(doc2.render())

    print("\n--- FACTORY METHOD ---")
    html_creator = HtmlCreator()
    print(html_creator.render_document("News", "Breaking story"))
    
    pdf_creator = PdfCreator()
    print(pdf_creator.render_document("Invoice", "Amount: ₹500"))
