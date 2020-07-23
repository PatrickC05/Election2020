import csv
import numpy as np
import math
from datetime import date

filename = 'Data/president_polls.csv'

abbrevs = {
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



class Poll(object):
    """
    A poll gives a rough estimate of how the electorate in a state is thinking
    """
    def __init__(self, question_id, end=None, state=None, pop=None, rate=None, sample=None, method=None, Dpct = 0, Rpct = 0):
        self.question_id = question_id
        self.date = end
        self.state = state
        self.pop = pop
        self.rate = rate
        self.sample = sample
        self.method = method
        self.Dpct = Dpct
        self.Rpct = Rpct
        
    def getDpct(self):
        return self.Dpct
    
    def getRpct(self):
        return self.Rpct
    
    
    def addDpct(self, Dpct):
        self.Dpct = Dpct
    
    def addRpct(self, Rpct):
        self.Rpct = Rpct
        
    def getPop(self):
        return self.pop
    
    def getMethod(self):
        return self.method
    
    def getMargin(self):
        return self.Rpct - self.Dpct
    
    def getGrade(self):
        return self.rate
    
    def getSample(self):
        return self.sample

    def __str__(self):
        if self.getMargin() > 0:
            m = "Trump +" + str(self.getMargin())
        elif self.getMargin() < 0:
            m = "Biden +" + str(-self.getMargin())
        else:
            m = "TIE"
        return self.state + " Date: "+ self.date + " Result: " + m
    
    def __eq__(self, other):
        return self.question_id == other.question_id

def loadPolls(file, states):
    polls = {}
    for state in states:
        polls[state] = []
    pending = {}
    day = str(date.today()).split('-')
    with open(file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            qid = row["question_id"]
            end = row["end_date"]
            intime = False
            if end != '':
                enddate = end.split('/')
                if (int(day[1]) - int(enddate[0]) <= 1) or (int(day[1]) - int(enddate[0] == 2 and int(day[2]) <= int(enddate[1]))):
                    if enddate[2] == "2020" or enddate[2] == "20":
                        intime = True
                        
            if (row['state'] in abbrevs and row['fte_grade'] != '' and row['sponsor_candidate'] == ''
                and row['partisan'] == '' and row['tracking'] == '' and row['sample_size'] != '' and intime):
                
                if qid not in pending.keys():
                    try:
                        pending[qid] = Poll(qid, end=end, state=row['state'], 
                                            pop=row['population_full'],rate=row['fte_grade'],
                                            sample=int(row['sample_size']),method=row["methodology"])
                    except:
                        raise ValueError(qid)
                if row["answer"] == "Biden":
                    pending[qid].addDpct(float(row["pct"]))
                elif row["answer"] == "Trump":
                    pending[qid].addRpct(float(row["pct"]))
                try:
                    if pending[qid].getDpct() != 0 and pending[qid].getRpct() != 0:
                        polls[row['state']].append(pending[qid])
                        del pending[qid]
                except:
                    pass
    return polls

def getAS(polls, states):
    """
    Uses a list of polls to get an average and standard deviation for each state
    Where output[state] = (average, standard deviation) or (None, None) if no polls are available
    """
    ans = {} #average, standard deviation
    rates = {"A+":1, "A": 0.9, "A-": 0.8, "B+": 0.7, "B": 0.6, "B-": 0.5, "C+": 0.45, "C": 0.4, "C-": 0.35, "D+": 0.3, "D": 0.25, "D-": 0.2, "F": 0.1, 'A/B': 0.6, 'B/C': 0.4, 'C/D': 0.25}
    pops = {"lv": 1, "v": 0.9, "rv": 0.8, "a": 0.75}
    methods = {'Online': 0.5, 'Automated Phone': 1, 'IVR/Online': 0.6, 'Online/IVR': 0.6, 'Live Phone': 1.2, 
               'IVR/Text': 0.75, 'Online/Text': 0.6, 'IVR/Live Phone': 1, 'Live Phone/Online/Text': 0.75, 
               'Text': 0.8, 'Live Phone/Online': 0.8, 'Live Phone/Text': 1}
    for state in states:
        p = polls[state]
        average = 0
        size = 0
        count = 0
        for poll in p:
            average += poll.getMargin()
            size += poll.getSample() * rates[poll.getGrade()] * pops[poll.getPop()] * methods[poll.getMethod()]
            count += 1
        try:
            ans[states[state]] = (round(average/count,3), round(100/math.sqrt(size/count)/1.96, 3))
        except ZeroDivisionError:
            ans[states[state]] = (None, None)
    return ans