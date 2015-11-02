#functions called directly by the bot

import events
import telegram
import re
import random
from dota_functions import *
from msg_texts import *

#Request, format and send dota last match info
def last_match(bot, message):
    sendText(bot,message.chat_id,msgs['getmatch'])
    dota_id = get_dota_id_from_telegram(message.from_user.id)
    match_id = getLastMatch(dota_id)
    bot.sendMessage(chat_id=message.chat_id,
            text="[Requested DotaBuff page for match "
            +str(match_id)+"](http://dotabuff.com/matches/"+str(match_id)+").",
            parse_mode=telegram.ParseMode.MARKDOWN)

#Request, format and send dota feeding info.
#Todo: Cache results and update weekly or when requested
def feeding(bot,message):
    sendText(bot,message.chat_id,msgs['getfeed'])
    sendText(bot,message.chat_id,msgs['serverpoll'])
    
    table = msgs['feedtable']
    feeds = feedRank()
    i=0;
    for rank in feeds:
        i+=1
        table+=str(i)+"....."+str(rank['dota_name'])+"...."+str(rank['total_deaths'])+"\n"    
    sendText(bot,message.chat_id,table)
    
    footer = "Congratulations to "+str(feeds[0]['dota_name'])+"! \nCheck out the match where he fed the most ("+str(feeds[0]['top_deaths'])+" times!)"

    sendText(bot,message.chat_id,footer)

    bot.sendMessage(chat_id=message.chat_id,
            text="["+str(feeds[0]['dota_name'])+"'s DotaBuff Match](http://dotabuff.com/matches/"+str(feeds[0]['top_match'])+").",
            parse_mode=telegram.ParseMode.MARKDOWN)

#Wrapper for telegram.bot.sendMessage() function
def sendText(bot,chat_id,text):
    bot.sendMessage(chat_id=chat_id,text=text,parse_mode="Markdown")

#Searches for commands sent to bot
def command(cmd,text):
    if re.match(cmd,text,re.IGNORECASE):
        return True
    else:
        return False

#Searches for keywords sent to bot
def keywords(words,text):
    if any(word in text for word  in words):
#        pdb.set_trace()
        return True
    else:
        return False

#for printing to terminal. Switching to logging module instead
def infoprint(bot,message,text):
    print("\nSKYBEARD ACTION\n["+text+"]")
    print ("USER: "),message.from_user.id,message.from_user.first_name 
    print ("USER MESSAGE:")
    print '"'+message.text+'"\n'

#Show chat members why they should go lift
def gainz(bot,chat_id,message):
    gain_photos= [
            'http://i.imgur.com/QrdcYCP.jpg',
            'http://i.imgur.com/zopXdvc.jpg',
            'http://i.imgur.com/jEi18ha.jpg'
            ]
    i = random.randint(0, len(gain_photos)-1)
    print i
    bot.sendPhoto(chat_id=chat_id, photo=gain_photos[i])


def greet(bot,chat_id,message):

    sendText(
            bot,chat_id,
            ''.join([msgs['welcome1'],
                str(message.from_user.id),
                msgs['welcome2'],
                message.from_user.first_name]))
    

def goodbye(bot,chat_id,message):
    
    sendText(bot,chat_id,"Daisy...daisy...") 

