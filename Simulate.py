"""
This file uses the functions in Predict.py to run a simulation
"""

import numpy as np
import csv
from Predict import *
import random


def loadStates(file):
    """
    Uses the provided file to load in the states to a list, and returns the list
    """
    statedict={}
    with open(file, "r", encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            statedict[row["State"]] = int(row["Votes"])
    return statedict

def loadP(file):
    """
    Uses the provided file to load regression predictions and returns the dictionary
    """
    preds = {}
    with open(file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            preds[row["state"]] = float(row["votes"])
    return preds

ecollege = 'Data/Votes.csv'

states = loadStates(ecollege)

statepolls = getAS(loadPolls(filename, abbrevs), abbrevs)
reg = loadP("Data/histpredictions.csv")
last = loadP("Data/2016v.csv")

def simulate(statepolls, reg, last, scollege, trials, incumbent=0.5, vswing=2, pweight=.6, rweight=0.4):
    rwin = {} # Chance R win by state
    dneed = {} # Count of state wins if D wins
    rneed = {} # Count of state wins if R wins
    avg = {} # Each state's average
    
    for state in scollege:
        rwin[state] = 0
        dneed[state] = 0
        rneed[state] = 0
        avg[state] = 0
    
    wins = 0
    ties = 0
    for i in range(trials):
        votes = 0
        swing = round(vswing* random.random(), 5)
        statewin = {}
        for state in scollege:
            p = statepolls[state]
            if p != (None, None):
                v = np.random.normal(statepolls[state][0]*pweight + reg[state]*(1-pweight)*rweight + last[state]*(1-pweight)*(1-rweight) +
                                     incumbent, statepolls[state][1]) + swing
            else:
                v = reg[state]*rweight + last[state]*(1-rweight) + incumbent
            if v >= 0:
                rwin[state] += 1
                votes += scollege[state]
                statewin[state] = True
            else:
                statewin[state] = False
            avg[state] += v
                
        if votes >= 270:
            wins += 1
            for state in statewin:
                if statewin[state]:
                    rneed[state] += 1
        elif votes == 269:
            ties += 1
        else:
            for state in statewin:
                if not statewin[state]:
                    dneed[state] += 1
        
    for state in rwin:
        rwin[state] /= trials
        dneed[state] /= (trials - wins - ties)
        rneed[state] /= wins
        avg[state] /= trials
        

    return (rwin, wins/trials, ties/trials, rneed, dneed, avg)

x,y,z,a,b,c = simulate(statepolls, reg, last, states, 1000000)