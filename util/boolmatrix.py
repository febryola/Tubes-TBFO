"""
module boolmatrix
Implementasi matriks boolean untuk perhitungan unit production.
Matriks merupakan matriks persegi.
"""

import numpy as np

class BoolMatrix:
  """Kelas matriks boolean"""

  def __init__(self, size) -> None:
    self.__size = size
    self.__matrix = np.identity(self.__size, dtype=bool)
  
  @property
  def matrix(self) -> np.ndarray:
    """Mengembalikan Array"""
    return self.__matrix
  
  def transitiveClosure(self) -> np.ndarray:
    """Menghitung klosur menghantar dari matriks boolean"""
    res = self.__matrix.copy()
    it = 1

    while(it < self.__size):
      res = res @ res
      it = it * 2
    
    return res