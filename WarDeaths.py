import wikipedia
import requests
from bs4 import BeautifulSoup

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
    for war in wars:
        print(war.text)
        print("*******************************************************************")

    return wars

def createPairs(wars):
    pairs = []
    for war in wars:
        lines = war.text.split("\n")
        pair = (lines[3], lines[5])
        pairs.append(pair)
    return pairs

#split into sets by 50 year periods

#aggregate to 1 total

#create histogram

URL = "https://en.wikipedia.org/wiki/List_of_wars_by_death_toll"

wars = scrape(URL)
deathsAndYear = createPairs(wars)
for war in deathsAndYear:
    print(war[0] + " " + war[1])
