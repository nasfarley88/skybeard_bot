#Functions for interfacting with DOTA 2 API. Uses the thin wrapper Dota2py by Andrew Snowden for requests
#This is very quick and dirty 5am code do test requesting from DOTA 2 API. 

from dota2py import api
import sys
from os.path import abspath, join, dirname
import os
from datetime import date, timedelta

#Spacecats dictionary for steam id and name lookup.
#All functions currently use first_name value from telegram message.
#All functions are agnostic of which identifier is used. message.from_user.id is safer,
#will implement method to register user with telegram id and ue config file instead of dict.
spacecats = [
        {'dota_name':'Lance Maverick'   ,'dota_id':11632278,    'first_name':'Peter'   },
        {'dota_name':'Kitt Spheromak'   ,'dota_id':17584723,    'first_name':'George'  },
        {'dota_name':'Rick Tiverick'    ,'dota_id':60362246,    'first_name':'Loz'     },
        {'dota_name':'Plato McBane'     ,'dota_id':46134077,    'first_name':'Simon'   },
        {'dota_name':'Archimedes Steel' ,'dota_id':48097133,    'first_name':'Jack'    },
        {'dota_name':'Francis Badass'   ,'dota_id':52188461,    'first_name':'Ian'     },
        {'dota_name':'Stephen Dedalus'  ,'dota_id':5805252,     'first_name':'Charles' }
     ]                                                        


#returns last 25 matches for given user
def findMatches(account_id):                                  
    return api.get_match_history(account_id=account_id)["result"]["matches"]


#returns value for given key in results such as list of players, starttime etc
#abstraction from api requests for simplicity, but currently experimenting with
#using json  
def getResults(match,key):
    result = match['result']
    vals_list = result[key]
    return vals_list


#Takes list of players from match an returns the value of an attribute
#for a given player, e.g deaths, hero healing, tower damage etc
def getPlayerVal(vals_list,account_id,val):

    for d in vals_list:
        if d['account_id'] == account_id:
            return d[val]



#returns a zipped list of match_id's with a given player's attribute for each
#of the player's last 25 matches
def getSum(account_id,days,attribute):
    
    matches = findMatches(account_id)
    
    match_ids = []
    attr_list = []
    
    for i in range (0,25):
        if matches[i].has_key("match_id"):
            print "True",i
            print  matches[i]["match_id"]
            match = api.get_match_details(matches[i]["match_id"])
            match_ids.append(matches[i]['match_id'])
            results = getResults(match,'players')
            attr_list.append(getPlayerVal(results,account_id,attribute))
    return zip(match_ids,attr_list)    


#To link telegram user with dota player. Any unique identifier from
#telegram can be used.
def get_dota_id_from_telegram(user_id):
    
    for i, spacecat in enumerate(spacecats):
        #change to user_id when I have everyone's id
        if spacecat['first_name'] == user_id:
            index = i
        else:
            return 11632278 #my id.
        return spacecats[index]['dota_id']


#Returns the last match of a given player 
def getLastMatch(dota_id):

    matches = findMatches(dota_id)
    match_id = (matches[0]["match_id"])
    return match_id


#Returns ranked dict based on deaths.
#Should be made more general for any attribute
def feedRank():

    results = []
    for spacecat in  spacecats:
        name = spacecat['dota_name']
        account_id = spacecat['dota_id']
        deaths = getSum(account_id,7,'deaths')
        death_lists = zip(*deaths)
        top_index =death_lists[1].index(max(death_lists[1]))
        top_deaths = death_lists[1][top_index]
        top_match = death_lists[0][top_index]
       
        total_deaths=sum(death_lists[1])
        
        result = {
                'dota_name':name,
                'dota_id':account_id,
                'total_deaths':total_deaths,
                'top_match':top_match,
                'top_deaths':top_deaths
                }
        results.append(result)
    
    ranked = sorted(results, key=lambda k: k['total_deaths'],reverse=True) 
    return ranked

