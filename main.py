import datetime
import pytz
from time import sleep
from bot import Bot
from kraken import Kraken

gmt = pytz.timezone('GMT') # don't edit this is the twitter timezone of tweets

########################################################
##                       CONFIG                       ##
########################################################

local = pytz.timezone('America/Vancouver') # you local timezone
buy_ammount = 50 # how much doge to buy per tweet(doubtful there would be two tweets in a row)
sleep_time = 15 # time between tweet checks in seconds
timer_minutes = 1 #time from buy until sell in minutes
test_run = True # set to False to use real money(BTC)


########################################################
##          Shouldn't Need to Edit Below              ##
########################################################

def mySleep(time):
    timer = 0
    while timer < time:
        timer += 1
        sleep(1)
        print(' --==',timer,end=' ==--\r')
    print("")
    return
if __name__ == "__main__":
    Bot = Bot()
    # if test_run = True wont actually buy or sell anything just makes a fake run with real prices etc.
    # timer_minutes sets how long to wait until intiating the sell default = 25m
    k = Kraken(timer_minutes=timer_minutes, test_run=test_run)
    while True:
        skip_sleep = False
        print("\nGetting Last Tweet... ",end="")
        result = Bot.get_user_last_tweet("elonmusk")
        if not result:
            print("Something went wrong grabbing tweets... sleeping 2 seconds")
            skip_sleep = True
        elif type(result) is not str:
            fmt = '%Y-%m-%d %H:%M:%S'
            tweet_time = gmt.localize(result.created_at)
            local_time = tweet_time.astimezone(local)
            print("\n{} - {}".format(local_time.strftime(fmt), result.full_text))
            if Bot.is_sequence_in_text("doge",result.full_text):
                k.buy_doge(buy_ammount)
        else: 
            print(result)
        k.check_sell_doge()
        
        #time to sleep before checking tweets again
        if not skip_sleep:
            mySleep(sleep_time)
        else:
            mySleep(2)