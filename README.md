# Tubes TBFO : Python Syntax Checker
This is our first project that maintained by 3 people :
|            Name            |     NIM   |
| ---------------------------| --------- |
| Bayu Samudra               | 13520128  |
| Febryola Kurnia Putri      | 13520140  |
| Aloysius Gilang Pramudya   | 13520147  |

## What is this project about :
we created this project to fill the requirements of formal language theory classes and otomata at ITB
Informatics engineering. This project is to create a python compiler that will evaluate the correctness
of the syntax entered by the user into the program. The program will provide information to the user
whether the syntax entered error or not

## The Process
This web was made under several conditions:
* Using CFG
* Using CNF
* Using CYK
* Using FA

## How to run
To run this program, you can run this command in terminal:

```
python linter.py -c data/cnf.json filename.py
```
you can see the example below
```
python linter.py -c data/cnf.json test/tc/tc0.py
```
