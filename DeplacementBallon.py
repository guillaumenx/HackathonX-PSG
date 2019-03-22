# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 10:54:11 2019

@author: guill
"""

import pymongo
from pymongo import MongoClient
from lxml import etree
import numpy as np

def GetDataToMongodb(gameNumber,file):
    tree = etree.parse(file+"/f24-24-2016-853"+str(gameNumber)+"-eventdetails.xml")
    filmMatch=[]
    equipe1={}
    equipe2={}
    for gam in tree.xpath("/Games/Game"):
        teamH=gam.get("home_team_id")
        teamA=gam.get("away_team_id")
        NameTeamH=gam.get("home_team_name")
        NameTeamA=gam.get("away_team_name")

    for event in tree.xpath("/Games/Game/Event"):
        typeId=int(event.get("type_id"))
        if(typeId<17 or (typeId>40 and typeId<64 and typeId!=43 and typeId!=47) or typeId==74):
            posX=float(event.get("x"))
            posY=float(event.get("y"))
            teamId=event.get("team_id")
            if(teamId==teamH):
                evenement=[posX, posY, teamId]
            else:
                evenement=[100-posX, 100-posY, teamId]
            if(len(filmMatch)==0 or evenement[:-1]!=filmMatch[-1][:-1]):
                filmMatch=filmMatch+[evenement]
            
    test=np.asarray(np.asarray(filmMatch)[:,:-1],dtype=float)
    np.clip(test, 0, 100, out=test)
    return test

data=GetDataToMongodb(139)
#np.savetxt('trajMatch139.csv',data, delimiter=',')

'''
for i in range(139,519): #519
    if(i!=376 and i!=407 and i!=428 and i!=279 and i!=462 ):
        print(i)
        GetDataToMongodb(i)

n_test=10
train , test = data[:-n_test,0] , data[-n_test:,0]

from random import gauss
from random import seed
from matplotlib import pyplot
from statsmodels.graphics.tsaplots import plot_acf
# square the dataset
squared_data = [x**2 for x in train]
# create acf plot
plot_acf(squared_data)
pyplot.plot.axis([0,20,0,1])
pyplot.show()
'''