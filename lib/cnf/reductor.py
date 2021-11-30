"""
module reductor
Mereduksi CFG menjadi CNF-like CFG. Pada tahap ini, CNF tidak
dilakukan penyederhanaan.
"""


from lib.cfg import CFG
from lib.cnf import Transformer

class Reductor(Transformer):
  """Kelas Pereduksi CFG menjadi dalam bentuk CNF-like CFG"""
  def __init__(self, cfg: CFG) -> None:
    self.__rules = {}
    self.__symbolCnt = 0

    # Menghindari Runtime Error
    self.__queue = list(cfg.rules.keys())

    self.__terminals = cfg.terminals
    self.__groups = cfg.groups
    self.__start = cfg.start

    for i in cfg.rules:
      self.__rules[i] = list(cfg.rules[i])
  
  def __getNewSymbol(self) -> str:
    """Mendapatkan Nama Symbol baru yang tidak ada di CFG"""
    cnt = self.__symbolCnt
    result = f"S_{cnt}"

    self.__symbolCnt += 1

    if result in self.__rules.keys():
      # Buat simbol baru selanjunya karena simbol sudah ada
      return self.__getNewSymbol()
    else:
      return result
  
  def __simplifyRule(self, rule: tuple) -> tuple:
    """Memberikan rule baru hasil penyederhanaan dan menyesuaikan dengan rule table"""
    if len(rule) < 3:
      # Bila panjangnya sudah < 3, do nothing
      return rule
    else:
      newName = self.__getNewSymbol()

      self.__rules[newName] = [rule[1:]]
      self.__queue.append(newName)

      return (rule[0], newName)
  
  def transform(self) -> CFG:
    """Melakukan pengubahan CFG menjadi dalam bentuk CNF"""

    while(len(self.__queue) > 0):
      i = self.__queue.pop(0)
      for j in range(len(self.__rules[i])):
        newTuple = tuple(self.__simplifyRule(self.__rules[i][j]))
        self.__rules[i][j] = newTuple
    
    result = {}
    for i in self.__rules:
      result[i] = tuple(self.__rules[i])

    return CFG(result, self.__groups, self.__terminals, self.__start)