import events
import telegram
import re
import logging
import random
from beard_functions import *
from dota_functions import *

from dota2py import api
import sys
from os.path import abspath, join, dirname
import os
from datetime import date, timedelta
import msg_texts


sys.path.append(abspath(join(abspath(dirname(__file__)), "..")))

key = os.environ.get('DOTA2_API_KEY')
if not key:
    raise NameError('Please set the DOTA2_API_KEY environment variable')
api.set_api_key(key)
            
LAST_UPDATE_ID = None

def main():
    global LAST_UPDATE_ID

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Telegram Bot Authorization Token
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
    gainz_words = ['gainz',]
    
    #long polling skybeard bot
    while True:

        #Does a dota event exist?
        try:
            dotes
        except NameError:
            dota_exists = False
        else:
            dota_exists = True
        
        #Get updates from bot. 10s timeout
        for update in bot.getUpdates(offset=LAST_UPDATE_ID, timeout=10):
            chat_id = update.message.chat_id
            message = update.message
            text = update.message.text.encode('utf-8')
            user = update.message.from_user
           
            
            #Commands and keywords
            #Todo: See if this is less horrible with decorators
            if command('/help',text):
                sendText(bot,chat_id,msg_texts.help())

            if command('/topfeeds',text):
                feeding(bot,message)
            
            if command('/lastmatch',text):
                last_match(bot,message)

            if command('/dota',text):
                time = events.get_time(bot,message)
                dotes = events.dota(bot,message,time)
            
            if command('/delete dota',text): 
                if (dota_exists):
                    sendText(bot,chat_id,'Dota event deleted')
                    del dotes
                else:
                    events.nodota(bot,message)

            if command('shotgun!',text):
                if (dota_exists):
                    dotes.shotgun(message)
                else:
                    events.nodota(bot,message)
            
            if command('unshotgun!',text):
                if (dota_exists):
                    dotes.unshotgun(message,'shotgun')
                else:
                    events.nodota(bot,message)
            
            if command('unrdry!',text):
                if (dota_exists):
                    dotes.unshotgun(message,'rdry')
                else:
                    events.nodota(bot,message)

            if command('rdry!',text):
                if (dota_exists):
                    dotes.rdry_up(message)
                else:
                    events.nodota(bot,message)
            
            if keywords(gainz_words,text.lower()):
                gainz(bot,chat_id,message)

            if keywords(greetings,text.lower()) and  ('skybeard' in text.lower()):
                greet(bot,chat_id,message)
            
            if (keywords(goodbyes,text.lower())) and ('skybeard' in text.lower()):
                goodbye(bot,chat_id,message)
                 
            if (keywords(stack_queries,text.lower())):
                if (dota_exists):
                    dotes.stack(message)
                else:
                    events.nodota(bot,message)
                    
            if keywords(dota_queries,text.lower()) and ('dota' in text.lower()):
                if (dota_exists):
                    dotes.time_info(message)
                else:
                    events.nodota(bot,message)

        #Get new updates
        LAST_UPDATE_ID = update.update_id + 1

if __name__ == '__main__':
    main()

