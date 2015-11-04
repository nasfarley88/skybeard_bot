# skybeard_bot
Telegram bot to organise events, dota nights and many other features

##Requirements
- Python 2.6
- [python-telegram-bot v2.8.7](https://github.com/leandrotoledo/python-telegram-bot)
- [dota2py](https://github.com/andrewsnowden/dota2py)


##Installation
Once you have installed the requierments, run `python setup.py` with either the install or develop option depending on what you would like to do

##Running
The bot script is `skb_bot.py` and is run as a regular python script
```python skb_bot.py```

The commands currently available are:
* `/dota` - creates a new dota event and precedes the specifed time after "at". E.g:
 * `/dota at 18:45`
 * `/dota at 1845`
 * `/dota` - will create dota event with default time (19:30)
    
* `delete dota` - will remove the current dota event
    
* `/settime dota <HH:MM>` - will change the time of the current dota event
    
* `shotgun!` - Skybeard will know you wish to participate in the feeding
* `unshotgun!` - Remove yourself from the shotgun (and rdry) list.
    
* `rdry!` - Skybeard will know you are ready to feed imminently
* `unrdry!` - Remove yourself from the rdrys
* `/topfeeds` - Poll the Dota 2 API for everyone's last 25 matches, giving rankings by total deaths
* `/lastmatch` - Poll the Dota 2 API for your last played match and link the DotaBuff page
    
**Keywords**:
    I can be asked if there is a five stack in multiple ways, as well as if/when Dota is happening
    
  





