import csv
import numpy as np

class State():
    """
    A state contains critical information about a state
    to determine its preference
    
    There are others things to consider as well, but this is a really important part
    """
    def __init__(self, votes = None, polls=[], approval=[]):
        self.votes = votes
        self.polls = polls #List of polls, each element is poll data
        self.approval = approval #List of approval ratings, each element is poll data
        
    def getVotes(self):
        return self.votes
    
    def getPolls(self):
        return self.polls
    
    def getApproval(self):
        return self.approval