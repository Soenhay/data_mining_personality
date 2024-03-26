# ReadMe


Developed in VSCode but shouldn't be required.

## About

A simple program to simulate generating and assigning quests to players based on a simple personality profile, how many quests are left to finish the game, and what personalites best fist the quests.

Originally written in Summer 2021 for a Data Mining class.

## Dev Env Setup

Create new venv:
python -m venv .venv

Activate venv:
.venv\scripts\activate 

Install packages:
pip install -r requirements.txt

Run main.py (main entry point. no command line args.):
Use Runa and Debug button in VSCode
OR
python .\main.py   

View output files in \output directory


## NOTES:

See commands.txt for some of the commands I used to set up the environment.
The db was unfinished and unused.
The default launch.json can be used for VSCODE since it wasn't customized.
I am including the latest RunSummaries.csv file so you do not have to run it many times to see the regression and prediction.

## Roadmap or TODO wishlist

- Factor in rarity of personality type.
- Create better analytics and benchmarks.
- Add evovling player personalities.
- Simulate players joining and leaving the game. Dynamic quest assignment updating based on current active players.
