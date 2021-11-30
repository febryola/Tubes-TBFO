from lib.cnf.reductor import Reductor
from lib.cfg import CFG

def test_01():
  data = {
    "groups":{},
    "terminals":["1","0"],
    "rules":{
      "S": [["S","T"],["S","U","1"],["0"]],
      "B": [["1","S","1"],["0","T"],[]],
      "C": [["S","0","0","1","B"],["1","0"]]
    }
  }

  obj = CFG(data["rules"], data["groups"], data["terminals"],"I")
  red = Reductor(obj)

  res = red.transform()

  ans = {
    "S": (("S","T"),("S","S_0"),("0",)),
    "S_0": (("U","1"),),
    "B": (("1","S_1"),("0","T"),()),
    "C": (("S","S_2"), ("1","0")),
    "S_1": (("S","1"),),
    "S_2": (("0","S_3"),),
    "S_3": (("0","S_4"),),
    "S_4": (("1","B"),),
  }

  for i in res.rules:
    assert set(res.rules[i]) == set(ans[i])

def test_02():
  data = {
    "groups":{},
    "terminals":["1","0"],
    "rules":{
      "A": [["A","B","C"],["B","0","0"],["0"]],
      "S_0": [[]],
      "S_1": [[]],
    }
  }

  obj = CFG(data["rules"], data["groups"], data["terminals"],"a")
  red = Reductor(obj)

  res = red.transform()

  ans = {
    "A": (("A","S_2"),("B","S_3"),("0",)),
    "S_0": ((),),
    "S_1": ((),),
    "S_2": (("B","C"),),
    "S_3": (("0","0"),)
  }

  for i in res.rules:
    assert set(res.rules[i]) == set(ans[i])