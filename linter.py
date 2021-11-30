from lib.cyk.cyk import CYK
from datetime import datetime
import os
import argparse

parser = argparse.ArgumentParser(
  description="Python script grammar checker",
  epilog="\033[93mBeware:\033[0m This program is currently in develompent. May be broken.")

parser.add_argument("path",
  help="python script path", type=str)

parser.add_argument("-c","--config", type=str, action="store", 
  help="CNF Config file (JSON format)", nargs=1, required=True)

args = parser.parse_args()

if not os.path.isfile(args.path):
  print("\033[31mError:\033[0m", end=" ")
  print("Python script path is not valid")
  print()
  exit(-1)

if not os.path.isfile(args.config[0]):
  print("\033[31mError:\033[0m", end=" ")
  print("Configuration file is not valid")
  print()
  exit(-1)
  
print("""\033[32m
  _____       _   _                   _      _       _            
 |  __ \     | | | |                 | |    (_)     | |           
 | |__) |   _| |_| |__   ___  _ __   | |     _ _ __ | |_ ___ _ __ 
 |  ___/ | | | __| '_ \ / _ \| '_ \  | |    | | '_ \| __/ _ \ '__|
 | |   | |_| | |_| | | | (_) | | | | | |____| | | | | ||  __/ |   
 |_|    \__, |\__|_| |_|\___/|_| |_| |______|_|_| |_|\__\___|_|   
         __/ |                                                    
        |___/                                                     
\033[0m""")
print()
print("Version: 1.0.0")
print()

# Do something
cykObj = CYK(args.config[0], args.path)
res = cykObj.parse()

if cykObj.validityCheck():
  print("\033[32mINFO :\033[0m No syntax error detected")
else:
  print("\033[31mError :\033[0m Syntax error detected\n")
  
print("\033[36mQUestion\033[0m\nDo you want to save the CYK table logs?\n")

resp = input("Answer [Y/n]: ")
if resp.lower() == "y":
  pathlog = input("Input the path : ")
  f = open(pathlog, "w")

  f.write("// CYK Logs\n")
  f.write(f"// Timestamp : {datetime.now()}\n")
  f.write("\n")

  f.write("Token symbol :\n")
  for i in range(len(cykObj.tokens)):
    f.write(f"{i}. {cykObj.tokens[i]}\n")

  f.write("\n")
  cnt = 1

  for i in res:
    f.write(f"Row {cnt}\n")
    
    term = 0
    for j in i:
      f.write(f"Terminal {cnt}.{term}:\n")
      f.write("[")
      f.write(", ".join(j))
      f.write("]\n\n")
      term += 1
    cnt += 1
    f.write("\n-----\n")

  f.close()