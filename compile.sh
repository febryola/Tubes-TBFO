#!/bin/bash
python cfgutil.py  --mode translate -if formatted -of json data/cfg.txt data/cfg.json
python cfgutil.py  --mode cnf -if json -of json data/cfg.json data/cnf.json
