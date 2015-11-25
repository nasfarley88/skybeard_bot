#functions called directly by the bot
import requests
import events
import telegram
import re
import random
from dota_functions import *
from msg_texts import *
import pdb
import numpy as np
import matplotlib
matplotlib.use('Agg') #disable x-forwarding
import matplotlib.pyplot as plt
import pickle
import yaml
import pyowm
import omdb
import logging
import math
logging.basicConfig(filename='botlog.log',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logging.getLogger().addHandler(logging.StreamHandler())
#Request, format and send dota last match info
def last_match(bot, message):
    sendText(bot,message.chat_id,msgs['getmatch'])
    try:
        dota_id = get_dota_id_from_telegram(message.from_user.first_name)
        logging.info('Last match request:',dota_id,message.from_user.first_name)
        match_id = getLastMatch(dota_id)
        bot.sendMessage(chat_id=message.chat_id,
            text="[Requested DotaBuff page for match "
            +str(match_id)+"](http://dotabuff.com/matches/"+str(match_id)+").",
            parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        bot.sendMessage(chat_id=message.chat_id,text='You don\'t appear to be in the catabase. Please register using the /register command')

#Request, format and send dota feeding info.
#Todo: Cache results and update weekly or when requested
def feeding(bot,message,update=False):
    #pdb.set_trace()
    sendText(bot,message.chat_id,msgs['getfeed'])
    
    table = msgs['feedtable']
    if (update):
        sendText(bot,message.chat_id,msgs['serverpoll'])
        feeds = valRank('deaths')
        pickle.dump(feeds,open('catabase/feeds.p','wb'))
    
    else:
        try:
            feeds = pickle.load(open('catabase/feeds.p','rb')) 
        except Exception as e:
            logging.error(e)
            sendText(bot,message.chat_id,'Local feed data not found...')
            sendText(bot,message.chat_id,msgs['serverpoll'])
            feeds = valRank('deaths')
            logging.info('feeding data defaulted to:', feeds)
            pickle.dump(feeds,open('catabase/feeds.p','wb'))
    i=0;
    for rank in feeds:
        i+=1
        table+=str(i)+"....."+str(rank['dota_name'])+"...."+str(rank['total_vals'])+"\n"    
    sendText(bot,message.chat_id,table)
    
    footer = "Congratulations to "+str(feeds[0]['dota_name'])+"! \nCheck out the match where he fed the most ("+str(feeds[0]['top_vals'])+" times!)"

    sendText(bot,message.chat_id,footer)

    bot.sendMessage(chat_id=message.chat_id,
            text="["+str(feeds[0]['dota_name'])+"'s DotaBuff Match](http://dotabuff.com/matches/"+str(feeds[0]['top_match'])+").",
            parse_mode=telegram.ParseMode.MARKDOWN)

    #graphing test
    fig = plt.figure()
    ax = fig.add_subplot(111)
    feed_values = feeds[0]['val_list']
    match_ids = feeds[0]['match_list']
    N= len(feed_values)
    ind = np.arange(N)
    width =0.8
    bars = ax.bar(ind, feed_values, width,
                            color='#e2e6ed')
    ax.set_axis_bgcolor('#bcc5d4')
    ax.set_xlim(-width,len(ind)+width)
    ax.set_ylim(0,max(feed_values)+2)
    ax.set_ylabel('deaths per game')
    ax.set_title(feeds[0]['dota_name']+'\'s graph of shame')
    ax.set_xticks(ind+width)
    ax.set_xlabel('games')
    xtickNames = ax.set_xticklabels(match_ids)
    plt.setp(xtickNames, rotation=90, fontsize=6)
    imgPath = 'img/feed.png'
    plt.savefig(imgPath,facecolor='#bcc5d4')
    
    return imgPath 

#Wrapper for telegram.bot.sendMessage() function
def sendText(bot,chat_id,text,webprevoff=False):
    bot.sendMessage(chat_id=chat_id,text=text,parse_mode="Markdown",disable_web_page_preview=webprevoff)

#Searches for commands sent to bot
def command(cmd,text):
    if re.match(cmd,text,re.IGNORECASE):
        return True
    else:
        return False

#Searches for keywords sent to bot
def keywords(words,text):
    if any(word in text for word  in words):
        return True
    else:
        return False

#for printing to terminal. Switching to logging module instead
def infoprint(bot,message,text):
    logging.info(("\nDota info request:\n["+text+"]"))
    logging.info("USER: ",message.from_user.id,message.from_user.first_name) 
    logging.info("USER MESSAGE:")
    logging.info(message.text)

#Show chat members why they should go lift
def gainz(bot,chat_id,message):
    gain_photos= [
            'http://i.imgur.com/QrdcYCP.jpg',
            'http://i.imgur.com/zopXdvc.jpg',
            'http://i.imgur.com/jEi18ha.jpg'
            ]
    i = random.randint(0, len(gain_photos)-1)
    bot.sendPhoto(chat_id=chat_id, photo=gain_photos[i])


#Post cats in space
def postCats(bot,message):
    cat_photos= [
            'http://i.imgur.com/bJ043fy.jpg',
            'http://i.imgur.com/iFDXD5L.gif',
            'http://i.imgur.com/6r3cMsl.gif',
            'http://i.imgur.com/JpM5jcX.jpg',
            'http://i.imgur.com/r7swEJv.jpg',
            'http://i.imgur.com/vLVbiKu.jpg',
            'http://i.imgur.com/Yy0TCXA.jpg',
            'http://i.imgur.com/2eV7kmq.gif',
            'http://i.imgur.com/rnA769W.jpg',
            'http://i.imgur.com/08mxOAK.jpg'
            ]

    i = random.randint(0, len(cat_photos)-1)
    try:
        bot.sendPhoto(chat_id=message.chat_id, photo=cat_photos[i])
    except:
        print cat_photos[i]
        bot.sendPhoto(chat_id=message.chat_id,photo='http://cdn.meme.am/instances/500x/55452028.jpg')



#http POST request 
def postImage(imagePath,chat_id,REQUEST_URL):
#    pdb.set_trace()
    data = {'chat_id': chat_id}
    try:
        files = {'photo': open(imagePath,'rb')}
    except:
        return
    return requests.post(REQUEST_URL + '/sendPhoto', params=data, files=files)
    
#possibility of uploading pics to dropbox with this function (needs python 2.7 or greater)    
#def dropbox():
#    client = dropbox.client.DropboxClient(os.environ.get('DROPBOX_TOKEN'))
#    print 'linked account: ', client.account_info()
#    f = open('img/feed.png', 'rb')
#    response = client.put_file('/feed.png', f)
#    print 'uploaded: ', response
#    folder_metadata = client.metadata('/')
#    print 'metadata: ', folder_metadata
#
#    f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
#    out = open('magnum-opus.txt', 'wb')
#    out.write(f.read())
#    out.close()
#    print metadata

def movies(bot,message,title):
    chat_id=message.chat_id
    def buildImdbUrl(title):
        title_list = [element.strip() for element in title.split(' ')]
        url_elements = [
                'http://www.imdb.com/find?ref_=nv_sr_fn&q=',
                '+'.join(title_list),
                '&s=all'
                ]
        url = ''.join(url_elements)
        logging.info('imdb url built',url)
        return url
        
    
    try:
        result = omdb.get(title=title)
        result.title
    except:
        sendText(bot,message.chat_id,msgs['nomovie'])
        bot.sendMessage(chat_id=chat_id,text=buildImdbUrl(title),disable_web_page_preview=True)
        #sendText(bot,message.chat_id,str(buildImdbUrl(title)),True)
    else:
        logging.info('omdb result:', result)
        film = result.title
        year = result.year
        director = result.director
        metascore = result.metascore
        imdbscore = result.imdb_rating
        plot = result.plot
        
        poster = result.poster
        imdb = 'http://www.imdb.com/title/'+result.imdb_id
        reply = (
                'Title: '+film+'\n'
                'Year: '+year+'\n'
                'Director: '+director+'\n'
                'Metascore: '+metascore+'\n'
                'IMDb rating: '+imdbscore+'\n'
                'Plot:\n'+plot
                )     
        try:
            bot.sendPhoto(chat_id=chat_id,photo=poster)
        except:
            logging.error("no poster found",result)
        sendText(bot,chat_id,reply)
        sendText(bot,chat_id,imdb,True)


#python 2.7+ only
#gives current weather and forecast for given location.
def forecast(bot,message):
    
    owm = pyowm.OWM(os.environ.get('OWM_TOKEN'))
    text = message.text
    
    try:
        location = text.split('/weather',1)[1]
    except:
        location = 'Birmingham,uk'
    if not location:
        location = 'Birmingham,uk'
    try:    
        forecast = owm.daily_forecast(location,limit=7)
        tomorrow = pyowm.timeutils.tomorrow()
        weather_tmrw = forecast.get_weather_at(tomorrow)
    except:
        return sendText(bot,message.chat_id,'I\'m sorry, something went wrong.')
        
    true_location = forecast.get_forecast().get_location().get_name()
    coor_lon =  forecast.get_forecast().get_location().get_lon()
    coor_lat =  forecast.get_forecast().get_location().get_lat()

    
    lst_clouds = []
    lst_temp = []
    lst_status = []
    lst_time = []
    

    f_day = forecast.get_forecast()
    for weather in f_day:
        lst_clouds.append( weather.get_clouds())
        lst_temp.append(weather.get_temperature('celsius')['max'])
        lst_status.append(weather.get_status())
        lst_time.append(weather.get_reference_time('iso'))
    print lst_clouds,lst_temp,lst_status,lst_time,len(lst_temp)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    N= len(lst_status)
    ind = np.arange(N)
    width =0.6
    bars_temp = ax.bar(ind, lst_temp, width,
                            color='#e2e6ed')
#    bars_cloud = ax.bar(ind, lst_temp, width,
#                            color='blue')
    ax.set_axis_bgcolor('#bcc5d4')
    ax.set_xlim(-width,len(ind)+width)
    ax.set_ylim(0,max(lst_temp)+5)
    ax.set_title('Seven day forecast')
    ax.set_xticks(ind+width)
    ax.set_xlabel('Next 7 days')
    ax.set_ylabel('Max. temperature (C)')
    plt.yticks(np.arange(min(lst_temp), max(lst_temp)+1, 1.0)) 
    xtickNames = ax.set_xticklabels(lst_status)
    plt.setp(xtickNames, rotation=45, fontsize=15)
    imgPath = 'img/weather.png'
    plt.savefig(imgPath,facecolor='#bcc5d4')
    temp_tmrw = weather_tmrw.get_temperature('celsius')
    
    if forecast.will_be_sunny_at(tomorrow):
        status = 'sunny'
    elif forecast.will_be_sunny_at(tomorrow):
        status = 'cloudy'
    elif forecast.will_be_rainy_at(tomorrow):
        status = 'rainy'
    elif forecast.will_be_snowy_at(tomorrow):
        status = 'snowy'
    elif forecast.will_be_stormy_at(tomorrow):
        status = 'stormy'
    elif forecast.will_be_foggy_at(tomorrow):
        status = 'foggy'
    elif forecast.will_be_tornado_at(tomorrow):
        status = 'TORNADO!!'
    elif forecast.will_be_hurricane_at(tomorrow):
        status = 'HURRICANE!!'
    else:
        status = '<unknown status>'
    
    logging.info('forecast request:',message,forecast) 
    fore_reply = 'Tomorrow in '+true_location+', it will be *'+status+'* with a maximum temperature of *'+str(temp_tmrw['max'])+'* degrees C' 
    

    observation = owm.weather_at_place(location)
    weather = observation.get_weather()
    logging.info('weather results:',message,weather)
    obs_wind = weather.get_wind()
    obs_temp = weather.get_temperature('celsius')

    obs_reply = 'Current weather status in *'+true_location+': ' +str(weather.get_detailed_status())+'*.\nWind speed (km/h):\t*'+str(obs_wind['speed'])+'*. Temperature (C):\t*'+str(obs_temp['temp'])+'*'
    
    sendText(bot,message.chat_id,obs_reply)

    sendText(bot,message.chat_id,fore_reply)
    
    bot.sendLocation(message.chat_id,coor_lat,coor_lon)

    return imgPath

def haversine(lat1,lon1,lat2,lon2,radius):

    earth_radius = 6371
    theta1 = math.radians(lon1)
    theta2 = math.radians(lon2)
    
    phi1 = math.radians(90.- lat1)
    phi2 = math.radians(90.-lat2)
    
    c = cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1-theta2)+math.cos(phi1)*math.cos(phi2))
    d = math.acos(c)*earth_radius
    
    if d < radius:
        return True
    else:
        return False


    

def locCheck(bot,message): 

    lon = message.location.longitude
    lat = message.location.latitude
    gyms = yaml.load(open('catabase/gyms.yaml','rb'))
    name = message.from_user.first_name

    for gym in gyms:
        if haversine(gym['lat'],gym['lon'],lat,lon,0.1):
            return sendText(bot,message.chat_id,'Good job on the gains at ' +gym['name']+' '+name+', I\'m proud of you')
        else:
            return
            


def thank(bot,chat_id,message):

    sendText(
            bot,chat_id,
            ' '.join([msgs['thanks'],str(message.from_user.first_name)]))

#greet users
def greet(bot,chat_id,message):
    sendText(
            bot,chat_id,
            ''.join([msgs['welcome1'],
                str(message.from_user.id),
                msgs['welcome2'],
                message.from_user.first_name]))
    
#say goodbye to users
def goodbye(bot,chat_id,message):
    sendText(bot,chat_id,"Daisy...daisy...") 

def echocats(bot,message):
    echo = message.text.split('/echo',1)[1]
    sendText(bot,-17644459,echo)

