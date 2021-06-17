import wikipedia
import requests
from bs4 import BeautifulSoup

def Scrape(url):
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
    #for war in wars:
        #print(war.text)
        #print("*******************************************************************")
    #print(wars[2])
    #print(len(wars))
        #print(t.text)
        #print("--------------------------------------------------------------------")
    return wars


URL = "https://en.wikipedia.org/wiki/List_of_wars_by_death_toll"
wars = Scrape(URL)
