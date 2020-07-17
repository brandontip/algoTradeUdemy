# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 12:35:44 2020

@author: Bran
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time 

temp_dir = {}
 
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_400_companies#S&P_400_MidCap_Index_Component_Stocks'
page = requests.get(url)
page_content = page.content
soup = BeautifulSoup(page_content,'html.parser')
tabl =  soup.find("table",{"class":"wikitable sortable"})

tickers=[]

for row in tabl.findAll('tr'):
    cells=row.findAll('td')
    if len(cells)==5:
        if  cells[2].find(text=True) == "Utilities":
            tickers.append(cells[1].find(text=True))
       







               
