"""
This file uses the functions in Predict.py to run a simulation
"""

import numpy as np
import math
import csv


class State(object):
    """
    A state contains critical information about a state
    to determine its preference
    
    There are others things to consider as well, but this is a really important part
    """
    def __init__(self, name, votes = None):
        self.name = name
        self.votes = votes
        
    def __str__(self):
        return self.name
    
    def getVotes(self):
        return self.votes

def loadStates(file):
    """
    Uses the provided file to load in the states to a list, and returns the list
    """
    statedict={}
    with open(file, "r", encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            statedict[row["State"]] = State(row["State"], votes = row["Votes"])
    return statedict

ecollege = 'Data/Votes.csv'

states = loadStates(ecollege)