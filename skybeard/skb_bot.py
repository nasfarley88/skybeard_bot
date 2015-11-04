import events
import telegram
import re
import logging
import random
from beard_functions import *
from dota_functions import *
import pdb
from dota2py import api
import sys
from os.path import abspath, join, dirname
import os
from datetime import date, timedelta
import msg_texts
from PIL import Image
import multipart

sys.path.append(abspath(join(abspath(dirname(__file__)), "..")))

app_key = os.environ.get('DB_APP_KEY')
app_secret = os.environ.get('DB_APP_SEC')
key = os.environ.get('DOTA2_API_KEY')
if not key:
    raise NameError('Please set the DOTA2_API_KEY environment variable')
api.set_api_key(key)
token = os.environ.get('TG_BOT_TOKEN')
BASE_URL = 'https://api.telegram.org/bot%s' % token
LAST_UPDATE_ID = None


def main():
    global LAST_UPDATE_ID
    global BASE_URL
    logging.basicConfig(filename='botlog.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logging.getLogger().addHandler(logging.StreamHandler())

    bot = telegram.Bot(token=os.environ.get('TG_BOT_TOKEN'))

    try:
        LAST_UPDATE_ID = bot.getUpdates()[-1].update_id
    except IndexError:
        LAST_UPDATE_ID = None

    #keywords
    dota_words = ['dota','dotes']
    dota_queries = ['when','happening']
    stack_queries = ['5 stack','5stack','stacked']
    greetings = ['hello','hi','hey']
    goodbyes = ['goodbye','bye','laters','cya']
    gainz_words = ['gainz']
    
    #long polling skybeard bot
    while True:

        #Does a dota event exist?
        try:
            dotes
        except NameError:
            dota_exists = False
        else:
            dota_exists = True
        
        #Get updates from bot. 10s timeout on poll, update on new message
        for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
            chat_id = update.message.chat_id
            message = update.message
            text = update.message.text.encode('utf-8')
            user = update.message.from_user
           
            ############ MESSAGE HANDLING ############
            ##########################################           
            
            #test photo sending is working
            if command('/phototest',text):
               postImage('feed.png',chat_id,BASE_URL) 
            
            #send help text
            if command('/help',text):
                sendText(bot,chat_id,msg_texts.help())
            
            #send top dota feeders table and graph
            if command('/topfeeds',text):
                imgPath = feeding(bot,message)
                postImage(imgPath,chat_id,BASE_URL) 
            
            #post last dota match details of user  
            if command('/lastmatch',text):
                last_match(bot,message)
            
            #create or modify time of dota event
            if command('/dota',text):
                time = events.get_time(bot,message)
                if (dota_exists):
                    dotes.set_time(time)
                    sendText(bot,chat_id,'Dota time modified')
                    dotes.time_info(message)
                else:    
                    dotes = events.dota(bot,message,time)
            
            #delete dota event
            if command('/delete dota',text): 
                if (dota_exists):
                    sendText(bot,chat_id,'Dota event deleted')
                    del dotes
                else:
                    events.nodota(bot,message)
            
            #shotgun a place in dota
            if command('shotgun!',text):
                if (dota_exists):
                    dotes.shotgun(message)
                else:
                    events.nodota(bot,message)
            
            #unshotgun your place in dota
            if command('unshotgun!',text):
                if (dota_exists):
                    dotes.unshotgun(message,'shotgun')
                else:
                    events.nodota(bot,message)
            
            #ready up for dota
            if command('unrdry!',text):
                if (dota_exists):
                    dotes.unshotgun(message,'rdry')
                else:
                    events.nodota(bot,message)
            #un-ready up for dota
            if command('rdry!',text):
                if (dota_exists):
                    dotes.rdry_up(message)
                else:
                    events.nodota(bot,message)
            
            #post motivational lifting pics
            if keywords(gainz_words,text.lower()):
                gainz(bot,chat_id,message)
            
            #reply to greetings messages
            if keywords(greetings,text.lower()) and  ('skybeard' in text.lower()):
                greet(bot,chat_id,message)
            
            #reply to farewell messages
            if (keywords(goodbyes,text.lower())) and ('skybeard' in text.lower()):
                goodbye(bot,chat_id,message)
            
            #respond to queries on wif dota is 5 stacked or not
            if (keywords(stack_queries,text.lower())):
                if (dota_exists):
                    dotes.stack(message)
                else:
                    events.nodota(bot,message)
            
            #respond to queries about dota event details        
            if keywords(dota_queries,text.lower()) and ('dota' in text.lower()):
                if (dota_exists):
                    dotes.time_info(message)
                else:
                    events.nodota(bot,message)

        #Get new updates
        LAST_UPDATE_ID = update.update_id + 1

if __name__ == '__main__':
    main()

