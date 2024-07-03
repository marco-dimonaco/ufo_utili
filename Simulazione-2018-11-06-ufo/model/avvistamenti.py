from dataclasses import dataclass


@dataclass
class Avvistamenti:
    year: int
    n: int

    def __str__(self):
        return f"{self.year} ({self.n})"
