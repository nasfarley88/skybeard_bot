# help message info
def help():

    msg = '''

    With the powers invested in me by Lord Gaben, I respond to the following commands and actions:
    
    *Commands:*
    
    */dota* - creates a new dota event and precedes the specifed time after "at". E.g:
        "*/dota at 18:45*"
        "*/dota at 1845*"
        "*/dota*" - will create dota event with default time (19:30)
    
    */delete dota* - will remove the current dota event
    
    */settime dota <HH:MM>* - will change the time of the current dota event
    
    *shotgun!* - Skybeard will know you wish to participate in the feeding

    *unshotgun!* - Remove yourself from the shotgun (and rdry) list.
    
    *rdry!* - Skybeard will know you are ready to feed imminently

    *unrdry!* - Remove yourself from the rdrys

    */topfeeds* - Poll the Dota 2 API for everyone's last 25 matches, giving rankings by total deaths

    */lastmatch* - Poll the Dota 2 API for your last played match and link the DotaBuff page
    
    *Keywords*:
        I can be asked if there is a five stack in multiple ways, as well as if/when Dota is happening

    '''
    return msg


# dict of strings for bot messages. Nice than concatenation in functions but still could be better
msgs ={ 
        #skybeard messages
        'welcome1':      'Hello spacecat No. ',
        'welcome2':      ', human name ',

        #dota2 api requests
        'getmatch':     '*RETRIEVING MATCH*',
        'getfeed':      '*RETRIEVING FEEDING DATA*\nOne moment please.',
        'serverpoll':   'Contacting Steam servers. This may take a while...\n',
        'feedtable':    '*TOP FEEDERS OF THE WEEK* (25 Matches)\n\nRANK....NAME....DEATHS\n',
        
        #dota event messages
        'w'     :       'with',
        'notime':       'No Time specified. Defaulting to 19:30',
        'nodota':       'I don\'t know about any dota happening today',
        'makedota':     'Dota event created for',
        'shotgun':      'you have shotgunned for Dota at',
        'overstack':    'Oh dear, too many people have shotgunned. It must be resolved with a fight to the death. \nShotguns are: \n'
        }
