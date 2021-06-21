# Hunter Thompson
# 6/20/2021
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
        #split based on new line to break each table element into its individual lines 
        lines = war.text.split("\n")
        #get deaths, there are sometimes two numbers based on high and low estimates and theyre seperated by dashes
        if len(lines[3].split("–")) > 1:    #if this font of dash is used
            deathsFull = lines[3].split("–")
        elif len(lines[3].split("-")) > 1:  #if this font of dash is used
            deathsFull = lines[3].split("-")
        else:
            deathsFull = lines[3].split("–")    #This is usually when there isnt a dash but i split it anyways
        #if theres two, choose the high estimate
        if len(deathsFull) > 1:     #there are two numbers
            deaths = deathsFull[1]  #choose second (the highest)
        else:
            deaths = deathsFull[0]
        #take the starting year
        year = lines[5].split("–")[0]
        #use regex to find digits. Some are in the format of xxxx+ or have extra citation links that need to be taken out
        deathsDigit = re.findall(r'\d+', deaths)
        #some elements are even numbers and can fudge it
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
    #periodSize is the number of 50 year periods being accounted for
    periodSize = 41  #2050 AD/50 = 41 periods
    #creates a list of size 41 with each starting with a count of 0 deaths
    periodTotals = [0] * periodSize

    for pair in deathsAndYear:
        #takes the element containing the year for this war
        year = int(pair[1])
        #finds the index by dividing years by 50 because the list maps to 50 year periods
        index = int(year / 50)
        #takes the element containing the death count for this war
        deaths = int(pair[0])
        #adds it to teh total for this 50 year period
        periodTotals[index] = deaths + periodTotals[index]
    
    return periodTotals


#create histogram
def createHistogram(periodTotals):
    #converts periodTotals to an integer
    periodTotals = [int(i) for i in periodTotals]
    #creates a list of years to be mapped to the totals
    years = [int(i*50+25) for i in range(41)] #+25 to make the table visually fit the period because it was centering the bars
    fig, ax = plt.subplots()
    ax.bar(years, periodTotals, len(years))
    ax.set_ylabel('Deaths')
    ax.set_title('Deaths by War')
    ax.legend()
    plt.show()


URL = "https://en.wikipedia.org/wiki/List_of_wars_by_death_toll"

wars = scrape(URL)
deathsAndYear = createPairs(wars)
periodTotals = aggregateByPeriod(deathsAndYear)
createHistogram(periodTotals)

