import logging
from dataclasses import dataclass

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def log_action(message):
    logging.info(message)

@dataclass
class SoftwareDeveloper:
    """
    Represents a software developer with various personality traits.
    """
    curiosity: bool = False
    discipline: bool = False
    collaboration: bool = False
    documentation: bool = False
    tdd_mindset: bool = False

    def describe(self):
        """Prints the traits of the software developer."""
        print("\nDeveloper Traits:")
        for trait, value in self.__dict__.items():
            print(f"{trait.capitalize()}: {value}")

class DeveloperBuilder:
    def add_curiosity(self): pass
    def add_discipline(self): pass
    def add_collaboration(self): pass
    def add_documentation(self): pass
    def add_tdd_mindset(self): pass
    def get_developer(self): pass

class ConcreteDeveloperBuilder(DeveloperBuilder):
    """
    Concrete builder class for assembling a SoftwareDeveloper instance.
    """
    def __init__(self):
        self.developer = SoftwareDeveloper()

    def add_curiosity(self):
        self.developer.curiosity = True
        log_action("Curiosity trait added.")

    def add_discipline(self):
        self.developer.discipline = True
        log_action("Discipline trait added.")

    def add_collaboration(self):
        self.developer.collaboration = True
        log_action("Collaboration trait added.")

    def add_documentation(self):
        self.developer.documentation = True
        log_action("Documentation trait added.")

    def add_tdd_mindset(self):
        self.developer.tdd_mindset = True
        log_action("TDD mindset trait added.")

    def get_developer(self):
        return self.developer

class DeveloperDirector:
    """
    Director class that constructs a SoftwareDeveloper using a builder.
    """
    def __init__(self, builder):
        self.builder = builder

    def construct_developer(self):
        self.builder.add_curiosity()
        self.builder.add_discipline()
        self.builder.add_collaboration()
        self.builder.add_documentation()
        self.builder.add_tdd_mindset()
        return self.builder.get_developer()

# Execution logic
builder = ConcreteDeveloperBuilder()
director = DeveloperDirector(builder)
developer = director.construct_developer()
developer.describe()

print("\nSteps:")
print("1. Define traits")
print("2. Build each trait step-by-step")
print("3. Assemble traits into a SoftwareDeveloper")