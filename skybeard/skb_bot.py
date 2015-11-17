import events
import telegram
import re
import logging
import random
import beard_functions as bf
import dota_functions as df
import pdb
from dota2py import api
import sys
from os.path import abspath, join, dirname
import os
from datetime import date, timedelta
import msg_texts
import register as reg

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
    thanks = ['thanks','cheers','nice one']
    gainz_words = ['gainz']
    dota_checked = False
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
          


            if (dota_exists and not dota_checked):
                dota_t_check = dotes.tcheck(message)
                print "checked",LAST_UPDATE_ID
                if (dota_t_check):
                    dota_checked = True

            ############ MESSAGE HANDLING ############
            ##########################################           
            
            #test photo sending is working
            if bf.command('/phototest',text):
               bf.postImage(text.split('/phototest ',1)[1],chat_id,BASE_URL) 
           
            #post space cat pics
            if bf.command('give me spacecats',text) or bf.command('show me spacecats',text):
                bf.postCats(bot,message)

            #send help text
            if bf.command('/help',text):
                bf.sendText(bot,chat_id,msg_texts.help())
            
            if bf.command('/weather',text):  #does not work in python2.6
                bf.forecast(bot,message)

            if bf.command('/movie',text):
                try:
                    title = text.split('/movie ',1)[1]
                except:
                    bf.sendText(bot,chat_id,'Please specify a film title')
                else:
                    bf.movies(bot,message,title)
                
            if bf.command('/register',text):
                reg.regCats(bot,message)
            
            if bf.command('/catabase',text):
                reg.printCats(bot,message)

            if bf.command('/catdump',text):
                reg.dumpCats(bot,message)
            
            if bf.command('/delete cat',text):
                reg.deleteCat(bot,message)
            
            if bf.command('/echo',text):
                bf.echocats(bot,message)

            #send top dota feeders table and graph
            if bf.command('/topfeeds',text):
                if 'update' in text.lower():
                    update_feeds = True
                else:
                    update_feeds = False
                print update_feeds
                imgPath = bf.feeding(bot,message,update_feeds)
                bf.postImage(imgPath,chat_id,BASE_URL) 
            
            #post last dota match details of user  
            if bf.command('/lastmatch',text):
                bf.last_match(bot,message)
            
            #create or modify time of dota event
            if bf.command('/dota',text):
                dota_checked = False
                time = events.get_time(bot,message)
                if (dota_exists):
                    dotes.set_time(time)
                    sendText(bot,chat_id,'Dota time modified')
                    dotes.time_info(message)
                else:    
                    shotguns = events.get_str_list(bot,message,'with')
                    dotes = events.dota(bot,message,time)
                    print shotguns
                    if shotguns:
                        for cat in shotguns:
                            dotes.shotgun(message,cat)


            
            #delete dota event
            if bf.command('/delete dota',text): 
                if (dota_exists):
                    bf.sendText(bot,chat_id,'Dota event deleted')
                    del dotes
                else:
                    events.nodota(bot,message)
            
            #shotgun a place in dota
            if bf.command('shotgun!',text):
                if (dota_exists):
                    dotes.shotgun(message)
                else:
                    events.nodota(bot,message)
            
            #unshotgun your place in dota
            if bf.command('unshotgun!',text):
                if (dota_exists):
                    dotes.unshotgun(message,'shotgun')
                else:
                    events.nodota(bot,message)
            
            #ready up for dota
            if bf.command('unrdry!',text):
                if (dota_exists):
                    dotes.unshotgun(message,'rdry')
                else:
                    events.nodota(bot,message)
            #un-ready up for dota
            if bf.command('rdry!',text):
                if (dota_exists):
                    dotes.rdry_up(message)
                else:
                    events.nodota(bot,message)
            
            #post motivational lifting pics
            if bf.keywords(gainz_words,text.lower()):
                bf.gainz(bot,chat_id,message)
            
            #reply to thank you messages
            if bf.keywords(thanks,text.lower()) and  ('skybeard' in text.lower()):
                bf.thank(bot,chat_id,message)
            
            #reply to greetings messages
            if bf.keywords(greetings,text.lower()) and  ('skybeard' in text.lower()):
                bf.greet(bot,chat_id,message)
            
            #reply to farewell messages
            if (bf.keywords(goodbyes,text.lower())) and ('skybeard' in text.lower()):
                bf.goodbye(bot,chat_id,message)
            
            #respond to queries on wif dota is 5 stacked or not
            if (bf.keywords(stack_queries,text.lower())):
                if (dota_exists):
                    dotes.stack(message)
                else:
                    events.nodota(bot,message)
            
            #respond to queries about dota event details        
            if bf.keywords(dota_queries,text.lower()) and ('dota' in text.lower()):
                if (dota_exists):
                    dotes.time_info(message)
                else:
                    events.nodota(bot,message)

        #Get new updates
        LAST_UPDATE_ID = update.update_id + 1

if __name__ == '__main__':
    main()

