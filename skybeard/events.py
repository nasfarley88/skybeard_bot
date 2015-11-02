import telegram
import re
import telegram
import datetime 
import logging
import pdb
import random
from beard_functions import *
from msg_texts import *

class dota:
    
    def __init__(self,bot,message,time):
       

        self.bot = bot
        self.creator = message.from_user
        
        self.time = time
        self.hour = time[:2]
        self.minute = time[2:]
        self.date_create = datetime.datetime.now()
        self.date_dota = self.date_create.replace(hour=int(self.hour),minute=int(self.minute))
        self.rdrys = []
        self.people =[]
        self.people.append(self.creator.first_name)

        sendText(bot,message.chat_id,
                ' '.join([msgs['makedota'],
                    tformat(self.date_dota),
                    msgs['w'],
                    self.creator.first_name])
                )
   
        self.dtime = self.date_dota-self.date_create

        infoprint(self.bot,message,"dota event")

    def shotgun(self,message):
        infoprint(self.bot,message,"shotgun request")
        if message.from_user.first_name not in self.people:
            self.people.append(message.from_user.first_name)
            sendText(self.bot,
                    message.chat_id,
                    ' '.join([message.from_user.first_name,
                        msgs['shotgun'],
                    self.time+" with: \n",
                    ', '.join(self.people)])
                    )
        else:
            sendText(self.bot,message.chat_id,
                    ''.join([message.from_user.first_name,
                    ", you already shotgunned"])
                    )
        
    def unshotgun(self,message,case):

        if (case == 'shotgun'):
            self.people = remove_list_val(self.people,message.from_user.first_name)
        if (case == 'shotgun' or 'rdry'):
            self.rdrys = remove_list_val(self.rdrys,message.from_user.first_name)
        sendText(self.bot,message.chat_id,
                message.from_user.first_name
                +', your '+case+' has been cancelled!')

    def rdry_up(self,message):

        infoprint(self.bot,message,"ready up request")
        
        if message.from_user.first_name not in self.rdrys:
            self.rdrys.append(message.from_user.first_name)
            sendText(self.bot,message.chat_id,
                    ''.join([message.from_user.first_name,
                    ", you have readied up! \nCurrent rdry's: \n",
                    ', '.join(self.rdrys)])
                    )
        else:
            sendText(self.bot,message.chat_id,
                    message.from_user.first_name+", you are already readied up!")
        if message.from_user.first_name not in self.people:
            self.people.append(message.from_user.first_name)
            sendText(self.bot,message.chat_id,'(...and I\'ve also shotgunned you)')

    def get_rdrys(self):
        return self.rdrys
    
    def stack(self,message):
        infoprint(self.bot,message,"stack status request")
        num_rdry = len(self.rdrys)
        num_shot = len(self.people)
        
        if (num_shot == 5):
            sendText(self.bot,message.chat_id,
                    "There is currently a 5 stack with: \n"
                    +', '.join(self.people)
                    +'\nCurrent rdry\'s:\n'
                    +', '.join(self.rdrys))

        elif(num_shot<5):

            sendText(self.bot,message.chat_id,
                    'No stack yet. \nCurrent shotguns: \n'
                    +', '.join(self.people)
                    +'\nCurrent rdry\'s: \n'
                    +', '.join(self.rdrys))
        else:

            sendText(self.bot,
                    message.chat_id,msgs['overstack']+', '.join(self.people))

    def info(self,message):
        infoprint(self.bot,message,"dota info request")
        sendText(self.bot,message.chat_id,
                "Dota is happening tonight at "
                +self.time+" with: \n"
                +', '.join(self.people))

    def time_info(self,message):
        infoprint(self.bot,message,"dota time info request")
        dtime = self.date_dota-datetime.datetime.now()
        sendText(self.bot,message.chat_id,
                "Dota will begin at "
                +tformat(self.date_dota)
                +", in "+str(self.dtime)
                +"\n*Shotguns:*\n"+', '.join(self.people))

def nodota(bot, message):
    
    sendText(bot,message.chat_id,msgs['nodota'])


#For unshotgunning, unrdry-ing 
def remove_list_val(the_list, val):
       return [value for value in the_list if value != val]

#zero pad time format
def tformat(date):
    return str(date.hour).zfill(2)+":"+str(date.minute).zfill(2)

#Find if the time was specified for an event and what it is
def get_time(bot,message):
    text = re.sub(':', '', message.text)
    match = re.search(r'at\s*(\w+)', text)
    if match:
        print match.group(1)
        time = str(match.group(1))
    else:    
        sendText(bot,message.chat_id,msgs['notime'])
        time = "1930"
    return time

#DEPRECATED
#Find out what kind of event it is 
def get_event(message):

    for pattern in message.text.split():
        if "dota" in pattern.lower():
            event = "dota"
        else:
          event = "event"
