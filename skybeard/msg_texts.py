# help message info
def help():

    msg = '''

    With the powers invested in me by Lord Gaben, I respond to the following commands and actions:
    
    *Commands:*
    *THE DATABASE*
    */register* -  This will register you, linking your telegram and dota accounts. This allows you to use the features that involve polling the Dota 2 API and is used as shown:
        "*/register <dota first name>, <dota last name>, <dotabuff player page>*"
    */catabase* - Displays the current spacecat entries in the database (catabase)
    */delete cat <index>* - Deletes the catabase entry for the given index. The index is the first element of the database entries returned with /catabase
    
    *DOTA EVENTS*
    */dota* - creates a new dota event and precedes the specifed time after "at". E.g:
        "*/dota at 18:45*"
        "*/dota at 18.45*"
        "*/dota at 1845*"
        "*/dota at 18:45 with alice, bob*"
        "*/dota*"
        Not specifying the time will create dota event with default time (19:30).
        If a dota event already exists, the time will just be modified.
        When creating an event you can include people you know want to play to auto shotgun them
    */delete dota* - will remove the current dota event
    *shotgun!* - Skybeard will know you wish to participate in the feeding
    *unshotgun!* - Remove yourself from the shotgun (and rdry) list.
    *rdry!* - Skybeard will know you are ready to feed imminently
    *unrdry!* - Remove yourself from the rdrys

    *DOTA 2 API REQUESTS*
    */topfeeds* - Poll the Dota 2 API for everyone's last 25 matches, giving rankings by total deaths.
    Giving the option "update" will update the data from the steam servers. This will occur automatically if no local cache is found.
    */lastmatch* - Poll the Dota 2 API for your last played match and link the DotaBuff page
    
    *MISC*:
        I can be asked if there is a five stack in multiple ways, as well as if/when Dota is happening
    '''
    return msg


# dict of strings for bot messages. Nice than concatenation in functions but still could be better
msgs ={ 
        #skybeard messages
        'welcome1':     'Hello spacecat No. ',
        'welcome2':     ', human name ',
        'thanks':       'You\'re welcome', 
        'reg_help':     '''To register, please format your request comma separated like so:\n"/register <dota first name>, <dota second name>, <dotabuff page>\ne.g\n"/register Lance, Maverick, http://www.dotabuff.com/players/11632278" ''',
        'reg_check':    'There seems to already be an entry in the catabase under your account. Please check it and delete your entry if you wish to re-register. see /help for details on how to do this.',
        #dota2 api requests
        'getmatch':     '*RETRIEVING MATCH*',
        'getfeed':      '*RETRIEVING FEEDING DATA*\nOne moment please.',
        'serverpoll':   'Contacting Steam servers. This may take a while...\n',
        'feedtable':    '*TOP FEEDERS OF THE WEEK* (25 Matches)\n\nRANK....NAME....DEATHS\n',
        
        #dota event messages
        'w'     :       'with',
        't_error':       'I didn\'t understand the time you specified and defaulted to 19:30. Did you format it correctly?',
        'notime':       'No Time specified. Defaulting to 19:30',
        'nodota':       'I don\'t know about any dota happening today',
        'makedota':     'Dota event created for',
        'shotgun':      'you have shotgunned for Dota at',
        'overstack':    'Oh dear, too many people have shotgunned. It must be resolved with a fight to the death. \nShotguns are: \n',
        
        #misc
        'nomovie':      'I couldn\'t find the film you were looking for, maybe IMDb can:'
        }
