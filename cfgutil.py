"""
module cfgutil
Driver untuk melakukan konversi CFG menjadi dalam format JSON
ataupun membentuk CNF dari CFG.
"""

import os
import argparse

from lib.converter.cfg import convertCFGToJson, convertCFGToYaml
from lib.cfg import CFG
from lib.cnf.cnf import CNF

parser = argparse.ArgumentParser(description="CFG Utility")
parser.add_argument("input", help="Input file path")
parser.add_argument("output", help="Output file path")

parser.add_argument("--mode","-m", nargs=1, 
  help="CFG Util mode", choices=["cnf","translate"])

parser.add_argument("--input-format", "-if",
  help="Input format file", choices=["formatted","json","yaml"], nargs=1)

parser.add_argument("--output-format", "-of",
  help="Input format file", choices=["formatted","json","yaml"], nargs=1)

args = parser.parse_args()

if not os.path.isfile(args.input):
  print("\033[31mError:\033[0m", end=" ")
  print("Input file path is not valid")
  print()
  exit(-1)

if not os.access(os.path.dirname(os.path.abspath(args.output)), os.W_OK):
  print("\033[31mError:\033[0m", end=" ")
  print("Output file path is not writeable")
  print()
  exit(-1)

if args.mode[0] == "cnf":
  if args.input_format[0] == "formatted" or args.output_format[0] == "formatted":
    print("\033[31mError:\033[0m", end=" ")
    print("Input format or output format is not allowed in this mode. Allowed format: {yaml. json}")
    print()
    exit(-1)
  
  print("\033[36mConverting CFG to CNF\033[0m")
  print(f"Mode : {args.input_format[0]} -> {args.output_format[0]}")
  print("")

  rule = None
  if args.input_format[0] == "json":
    rule = CFG.loadFromJSON(args.input)
  else:
    rule = CFG.loadFromYAML(args.input)

  cnf = CNF(rule)
  res = cnf.transform()

  if args.output_format[0] == "json":
    res.saveToJSON(args.output)
  else:
    res.saveToYAML(args.output)
elif args.input_format != args.output_format:
  print("\033[36mTranslating CFG Format\033[0m")
  print(f"Mode : {args.input_format[0]} -> {args.output_format[0]}")

  if args.input_format[0] == "formatted":
    if(args.output_format[0] == "yaml"):
      convertCFGToYaml(args.input, args.output)
    elif(args.output_format[0] == "json"):
      convertCFGToJson(args.input, args.output)
  elif args.input_format[0] == "yaml":
    obj = CFG.loadFromYAML(args.input)

    if(args.output_format[0] == "json"):
      obj.saveToJSON(args.output)
    else:
      obj.saveRules(args.output)
  else:
    obj = CFG.loadFromJSON(args.input)

    if(args.output_format[0] == "yaml"):
      obj.saveToYAML(args.output)
    else:
      obj.saveRules(args.output)
else:
    print("\033[31mError:\033[0m", end=" ")
    print("Input format and output format must be different")
    print()
    exit(-1)
