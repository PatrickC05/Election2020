import csv
import numpy as np

class State():
    """
    A state contains critical information about a state
    to determine its preference
    
    There are others things to consider as well, but this is a really important part
    """
    def __init__(self, name, votes = None, polls=[], approval=[]):
        self.name = name
        self.votes = votes
        self.polls = polls #List of polls, each element is poll data
        self.approval = approval #List of approval ratings, each element is poll data
        
    def __str__(self):
        return self.name
    
    def getVotes(self):
        return self.votes
    
    def getPolls(self):
        return self.polls
    
    def getApproval(self):
        return self.approval
    
    def addPoll(self, poll):
        self.polls.append(poll)
        
    def addApproval(self, approval):
        self.approval.append(approval)

