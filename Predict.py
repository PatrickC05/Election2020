import csv
import numpy as np
import math

abbreviations = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}

class State(object):
    """
    A state contains critical information about a state
    to determine its preference
    
    There are others things to consider as well, but this is a really important part
    """
    def __init__(self, name, votes = None, polls=[]):
        self.name = name
        self.votes = votes
        self.polls = polls #List of polls, each element is poll data
        
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
        

class Poll(object):
    """
    A poll gives a rough estimate of how the electorate in a state is thinking
    """
    def __init__(self, pollster, start, end, state = None, sample = 0,
                 method = None, Dpct = 0, Rpct = 0):
        self.pollster = pollster
        self.start = start
        self.end = end
        self.state = state
        self.sample = sample
        self.N = method
        self.Dpct = Dpct
        self.Rpct = Rpct
        self.Rmargin = Rpct - Dpct
        s = Dpct + Rpct
        self.Dpct = round(Dpct*100.0/s, 2)
        self.Rpct = round(Rpct*100.0/s, 2)
        
        
    def __str__(self):
        if self.margin > 0:
            m = "Trump +" + str(self.margin)
        elif self.margin < 0:
            m = "Biden +" + str(-self.margin)
        else:
            m = "TIE"
        return self.name + " Date: " + self.start +"-" + self.end + " Result: " + m
    
    def getState(self):
        return self.state
    
    def getMethod(self):
        return self.method
    
    def getMargin(self):
        return self.Rmargin