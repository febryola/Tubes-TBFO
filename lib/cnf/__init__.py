"""Module cnf
Modul yang berisi implementasi CNF
"""

from abc import ABC, abstractmethod

class Transformer(ABC):
  """Abstract class untuk transformer"""
  @abstractmethod
  def transform(self):
    pass