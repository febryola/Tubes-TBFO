""" Module cfg
Modul ini digunakan untuk menyimpan model dari CFG yang digunakan
"""

import yaml
import json
from lib.fa.enfa import ENFA

class CFG:
  def __init__(self, rules: dict, groups: dict, terminals: list, start: str) -> None:
    tmpRules = rules

    for i in tmpRules:
      data = list(tmpRules[i])
      for j in range(len(data)):
        data[j] = tuple(data[j])
      
      tmpRules[i] = tuple(data)

    self.__rules = tmpRules
    self.__groups = groups
    self.__terminals = tuple(terminals)
    self.__start = start

  @classmethod
  def loadFromJSON(cls, path: str):
    """Memuat data dari file JSON."""
    f = open(path)
    data = json.load(f)
    f.close()

    return cls(data["rules"], data["groups"], data["terminals"], data["start"])
  
  @classmethod
  def loadFromYAML(cls, path: str):
    """Memuat data dari file YAML."""
    f = open(path)
    data = yaml.safe_load(f)
    f.close()

    return cls(data["rules"], data["groups"], data["terminals"], data["start"])

  @property
  def groups(self) -> dict:
    """Mengembalikan groups CFG"""
    return self.__groups
  
  @property
  def terminals(self) -> tuple:
    """Mengembalikan terminal pada CFG"""
    return self.__terminals
  
  @property
  def rules(self) -> dict:
    """Mendapatkan data CFG"""
    return self.__rules
  
  @property
  def start(self) -> str:
    """Mendapatkan starting point dari CFG"""
    return self.__start
  
  def saveToYAML(self, path: str) -> None:
    """Simpan CFG ke file YAML"""
    f = open(path, "w")
    obj = {
      "start": self.__start,
      "groups": self.__groups,
      "terminals": list(self.__terminals),
      "rules": self.__rules
    }


    for i in obj["rules"]:
      data = list(obj["rules"][i])
      for j in range(len(data)):
        data[j] = list(data[j])
      
      obj["rules"][i] = list(data)
    
    yaml.dump(obj, f, default_flow_style=False)
    f.close()
  
  def saveToJSON(self, path:str):
    """Simpan CFG ke file JSON"""
    f = open(path, "w")

    obj = {
      "start": self.__start,
      "groups": self.__groups,
      "terminals": list(self.__terminals),
      "rules": self.__rules
    }

    for i in obj["rules"]:
      data = list(obj["rules"][i])
      for j in range(len(data)):
        data[j] = list(data[j])
      
      obj["rules"][i] = list(data)
    
    json.dump(obj, f)
    f.close()
  
  def saveRules(self, path:str) -> None:
    """Simpan Rules ke sebuah file. Rules yang disimpan sesuai dengan sintak CFG"""
    f = open(path, "w")
    
    lines = []
    lines.append("// Version: 1.0.0\n\n")
    lines.append("Start:\n")
    lines.append(self.__start + "\n")
    lines.append("\n")

    lines.append("Terminals:\n")
    for i in self.__terminals:
      lines.append(i + "\n")
    
    lines.append("\n")
    lines.append("Groups:\n")
    for i in self.__groups:
      lines.append(f"{i} = {self.__groups[i]}\n")

    lines.append("\n")
    lines.append("Rules:\n")
    for i in self.__rules:
      symbolStr = []
      for j in self.__rules[i]:
        symbolStr.append(" ".join(j))

      strRule = f"{i} -> {' | '.join(symbolStr)}"
      lines.append(strRule + "\n")
    
    f.writelines(lines)
    f.close()
  
  def getInvertedTable(self) -> dict:
    """Mendapatkan simbol pembangkit dari key"""
    inverted_cfg = {}

    for i in self.__rules:
      for j in self.__rules[i]:
        if j in inverted_cfg:
          if not i in inverted_cfg[j]:
            inverted_cfg[j] += (i,)
        else:
          inverted_cfg[j] = (i,)

    return inverted_cfg
  
  def getVariables(self) -> tuple:
    """Mendapatkan semua Variabel"""
    return tuple(self.__rules.keys())
  
  def groupCheck(self, groupName, value) -> bool:
    """Memeriksa value berdasarkan rule RE yang telah didefinisikan pada groupName
    
    Bila groupName tidak ada, dimunculkan error."""
    if groupName in self.__groups:
      tmp = ENFA(self.__groups[groupName])
      tmp.fit()

      return tmp.match(value)
    else:
      raise Exception("groupName tidak diemukan")

  def isTerminal(self, symbol: str) -> bool:
    """Mengembalikan true bila symbol merupakan terminal"""
    result = symbol in self.__terminals

    if result:
      return True
    else:
      checker = self.getGroupsChecker()
      for i in checker:
        result = checker[i](symbol)
      
      return result
  
  def isVariables(self, symbol:str) -> bool:
    """Mengembalikan true bila symbol adalah variable"""
    return symbol in self.getVariables()
  
  def getGroupName(self, symbol: str) -> object:
    """Mengembalikan nama simbol. Mengembalikan None bila bukan merupakan group."""
    checker = self.getGroupsChecker()

    for i in checker:
      if checker[i](symbol):
        return i
    
    return None