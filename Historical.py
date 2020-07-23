import csv
from scipy import stats

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
filename = 'Data/1976-2016-president.csv'
yton = {2000: 0, 2004: 1, 2008: 2, 2012: 3, 2016: 4}
votedata = dict() # structure: (R, D, T)


for state in abbrevs:
    votedata[state] = [[0,0,0] for i in range(5)]

with open(filename, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        year = int(row["year"])
        state = row["state"]
        writein = row["writein"]
        if year >= 2000 and row["writein"] == "FALSE":
            if row["party"] == "republican":
                votedata[state][yton[year]][0] = int(row["candidatevotes"])
            elif row["party"] == "democrat":
                votedata[state][yton[year]][1] = int(row["candidatevotes"])
            votedata[state][yton[year]][2] = int(row["totalvotes"])

percentages = dict()
for state in abbrevs:
    percentages[state] = list()
for state in votedata:
    for i in range(5):
        data = votedata[state][i]
        r = 100*data[0]/data[2]
        d = 100*data[1]/data[2]
        percentages[state].append(round(r-d,2))

lastfile = "Data/2016v.csv"
with open(lastfile, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["state", "votes"])
    for state in percentages:
        writer.writerow([abbrevs[state], percentages[state][4]])

predictions = {}
for state in percentages:
    s, i, r, p, std = stats.linregress(range(5), percentages[state])
    #print(f"{state}: Slope: {s}, Intercept:{i}")
    predictions[state] = round(5*s + i, 2)

predfile = "Data/histpredictions.csv"
with open(predfile, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["state", "votes"])
    for state in predictions:
        writer.writerow([abbrevs[state], predictions[state]])
