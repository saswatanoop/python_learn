
"""
    class: blueprint, with attributes(data/information) and methods(actions/behaviors)
    object: instance of a class
            self: refers to the object itself, used to access attributes and methods within the class
"""

"""
Python OOP Minimal Cheat Sheet

Visibility (applies to attributes & methods):
    - Public:    name        → fully accessible
    - Protected: _name       → convention only (internal use)
    - Private:   __name      → name-mangled (_ClassName__name)

Class Attributes:
    - Defined in class body
    - Shared across all instances

Static Methods:
    - No self/cls access
    - Utility functions

Class Methods:
    - Operate on class (cls)
    - Useful for alternate constructors

Defining Methods:    
    - Instance Method: def func(self)
    - Class Method:    @classmethod def func(cls)
    - Static Method:   @staticmethod def func()
    
"""

class Dog:
    count = 0  # class attribute (no static-attribute concept in Python)

    def __init__(self, name):
        self.name = name         # public
        self._breed = "Unknown"  # protected (convention)
        self.__alive = True      # private (name-mangled to _Dog__alive)
        Dog.count += 1

    # property for controlled access to _breed
    @property
    def breed(self):
        return self._breed

    @breed.setter
    def breed(self, value):
        self._breed = value

    @classmethod
    def get_dog_count(cls):
        return cls.count

    @staticmethod
    def bark():
        return "Woof! 🐶"


# --- Usage / demo (concise) ---
d1 = Dog("Bruno")
d1.breed = "Labrador"   # uses setter
d2 = Dog("Lucy")

# class method and class attribute
print("count:", Dog.get_dog_count(), Dog.count)  # count: 2 2

# static method (callable from class or instance; no self/cls used)
print(Dog.bark())        # Woof! 🐶
print(d1.bark())         # Woof! 🐶 (works but prefer class call)


# --- Class attribute vs instance attribute trap ---
class Config:
    timeout = 10  # class attribute (shared)

c1 = Config()
c2 = Config()

c1.timeout = 500       # creates instance attribute on c1 only (does NOT change class value)
Config.timeout = 999   # updates class attribute (affects instances without instance override)

print("c1.timeout:", c1.timeout)      # 500   (instance attribute shadows class)
print("c2.timeout:", c2.timeout)      # 999   (reads updated class attribute)
print("Config.timeout:", Config.timeout)  # 999





