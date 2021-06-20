
import requests
import re
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt
import numpy as np

def scrape(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="lxml")
   
    #this only takes tables that werent collapsed at the bottom of the page
    tables = soup.find_all("table", class_="sortable wikitable")
    #initailize it to be able to append wars from different tables
    wars = []
    for t in tables:
        #append the list of table elements to teh current list
        #tr is a table element 
        wars.extend(t.find_all("tr"))

    return wars

def createPairs(wars):
    #format of table element: 
    #0
    #1   Name of war
    #2
    #3   deaths "#-#"
    #4
    #5   year "#-#"

    #final return variables loaded with pairs of deaths and years
    pairs = []          
    #loop through each table element of wars
    for war in wars:
        #split based on new line
        lines = war.text.split("\n")
        #get deaths, there are sometimes two numbers based on high and low estimates
        if len(lines[3].split("–")) > 1:
            deathsFull = lines[3].split("–")
        elif len(lines[3].split("-")) > 1:
            deathsFull = lines[3].split("-")
        else:
            deathsFull = lines[3].split("–")
        #if theres two, choose the high estimate
        if len(deathsFull) > 1:
            deaths = deathsFull[1]
        else:
            deaths = deathsFull[0]
        #take the starting year
        year = lines[5].split("–")[0]
        deathsDigit = re.findall(r'\d+', deaths)
        if len(deathsDigit) > 0 and len(yearDigit) > 0:
            deathsDigit[0] = int(deathsDigit[0]) * pow(1000, len(re.findall(",", deaths)))
        yearDigit = re.findall(r'\d+', year)
        #create a temporary pair using a tuple
        if len(deathsDigit) > 0 and len(yearDigit) > 0:
            pair = (deathsDigit[0], yearDigit[0])
            #add to final list
            pairs.append(pair)
    return pairs

#split into sets by 50 year periods
def aggregateByPeriod(deathsAndYear):
    
    periodSize = 41  #2050 AD/50 = 41 periods
    periodTotals = [0] * periodSize
    for pair in deathsAndYear:
        year = int(pair[1])
        index = int(year / 50)
        deaths = int(pair[0])
        periodTotals[index] = deaths + periodTotals[index]


    for i in range(41):
        period = str(i*50)
        print(str(periodTotals[i]) + " in " + period + "\n")
    
    return periodTotals
#aggregate to 1 total
def finalizeData(periodTotals):
    yearAndTotal = []
    years = []
    for i in range(len(periodTotals)):
        years.append(i*50)
        pair = (i*50, periodTotals[i])
        yearAndTotal.append(pair)
    #index = np.arange(len(yearAndTotal))
    #plt.bar(index, periodTotals) #add color=''
    #plt.xticks(index, years, rotation='vertical')
    #plt.tight_layout()
    #plt.show()
    #ax = plt.subplots()
    #ax.bar(years, periodTotals, .35)
    #ax.set_ylabel('Deaths')
    #ax.set_title('Deaths by War')
    
    return years, periodTotals

#create histogram

URL = "https://en.wikipedia.org/wiki/List_of_wars_by_death_toll"

wars = scrape(URL)
deathsAndYear = createPairs(wars)
years, periodTotals = finalizeData(aggregateByPeriod(deathsAndYear))
periodTotals = [int(i) for i in periodTotals]
print(periodTotals)
fig, ax = plt.subplots()
ax.bar(years, periodTotals, len(years))
ax.set_ylabel('Deaths')
ax.set_title('Deaths by War')
ax.legend()
plt.show()
#for war in deathsAndYear:
    #print(war[0] + " " + war[1])
