"""
Модель бюджета
"""

from dataclasses import dataclass


@dataclass
class Budget:
    amount: float = 0.0
    pk: int = 0
