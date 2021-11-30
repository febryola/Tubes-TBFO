"""
Module cnf
Implementasi konverter CFG menjadi CNF
"""

from lib.cfg import CFG
from lib.cnf import Transformer
from lib.elimination.epsilon import EpsilonElimination
from lib.elimination.unit import  UnitElimination
from lib.elimination.useless import UselessElimination
from lib.cnf.reductor import Reductor

class CNF(Transformer):
  """Kelas Konverter CFG menjadi CNF"""
  def __init__(self, cfg: CFG) -> None:
    self.__cfg = cfg
  
  def __simplifyCFG(self):
    """Melakukan simplifikasi CFG"""
    ee = EpsilonElimination(self.__cfg).eliminate()
    ue = UnitElimination(ee).eliminate()
    newCFG = UselessElimination(ue).eliminate()

    self.__cfg = newCFG
  
  def transform(self) -> CFG:
    """Melakukan pengubahan CFG menjadi dalam bentuk CNF"""

    # Menyederhanakan CFG
    self.__simplifyCFG()

    reductor = Reductor(self.__cfg)
    return reductor.transform()
