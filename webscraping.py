# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 14:52:19 2024

@author: tiakd
"""

# Webscraping 

import requests
import pandas as pd
from bs4 import BeautifulSoup
year = "2024"
r = requests.get('https://emersonlions.com/sports/mens-soccer/roster/' + year)

table_dict = {'year':[],'transfer':[],'home_town':[],'position':[],'first_name':[],'last_name':[],'class':[],'height':[],'weight':[],'high_school':[]}

if r.status_code==200:
    soup = BeautifulSoup(r.content,'html.parser')
    
    s = soup.find('main',id='main-content')
    
    #position
    positions = s.find_all('div',class_='sidearm-roster-player-position')
    for line in positions:
        test = line.text.strip()
        pos = test.split()
        
        
        if len (pos) < 1:
            table_dict['position'].append('N/A')
            table_dict['year'].append(year)
        else: 
            table_dict['position'].append(pos[0])
            table_dict['year'].append(year)
        if len(pos) > 1:
            tmp = ''
            for x in range(1,len(pos)):
                tmp += pos[x] + " "
            metrics = tmp.split()
            
            table_dict['height'].append(metrics[0])
            if len(metrics)<2:
                table_dict['weight'].append('N/A')
            else:
                table_dict['weight'].append(metrics[1])
        else:
            table_dict['height'].append("N/A")
            table_dict['weight'].append('N/A')
    
    #player name
    first_names = s.find_all('span',class_='sidearm-roster-player-first-name')
    
    last_names = s.find_all('span',class_='sidearm-roster-player-last-name')
    
    count = 0
    
    for line in first_names:
        table_dict['first_name'].append(line.text)
        count+= 1
        if count == len(table_dict['position']):
            break
        
    count = 0
    
    for line in last_names:
        table_dict['last_name'].append(line.text)
        count+= 1
        if count == len(table_dict['position']):
            break
    
    
    home_towns = s.find_all('span',class_='sidearm-roster-player-hometown')
    
    count = 1
    
    for line in home_towns:
        if count%2==0:
            table_dict['home_town'].append(line.text)
        count+=1
        if len(table_dict['home_town'])==len(table_dict['position']):
            break
    
    
    ac_year = s.find_all('span',class_='sidearm-roster-player-academic-year')
    
    count = 0
    for line in ac_year:
        if count == len(table_dict['position']):
            break
        if '.' in line.string:
            count += 1
            table_dict['class'].append(line.text)
    
    hs = s.find_all('div',class_='sidearm-roster-player-class-hometown')
    
    count = 1
    for line in hs:
        tmp = line.text.strip()
        lst = tmp.split('\n')
        count+= 1
        if len(lst) > 2:
            if count % 2 ==0:
                if '/' in lst[2]:
                    table_dict['transfer'].append('Y')
                    
                    preSlash = lst[2].split('/')
                    table_dict['high_school'].append(preSlash[0].strip())
                else:
                    table_dict['transfer'].append('N')
                    table_dict['high_school'].append(lst[2])
        elif count % 2 ==0:
            table_dict['high_school'].append('N/A')
        
        if len(table_dict['high_school']) == len(table_dict['position']):
            break
    
    player_sheet = pd.DataFrame(table_dict)
    
    player_sheet.to_csv('C:/Users/tiakd/Desktop/soccerProject/emerson'+year+'.csv')
    
else:
    print('failure')