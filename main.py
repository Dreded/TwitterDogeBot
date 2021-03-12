import datetime
import pytz
import os
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
        print(' --==',timer,end=' ==--\r')
        sleep(1)
    return

def print_header():
    os.system('CLS')
    headers = {
        "Doge Tweet Found:":    "{}x".format(total_doge_tweets),
        "New Tweets:":          "{}x".format(total_new_tweets),
        "Checked Feed:":        "{}x".format(total_runs),
        "Owned Doge Coins:":    k.total_doge_qty,
    }
    for key,value in headers.items():
        print(key,value,end="    ")
    print("")
    print("Getting Last Tweet...")

if __name__ == "__main__":
    Bot = Bot()
    # if test_run = True wont actually buy or sell anything just makes a fake run with real prices etc.
    # timer_minutes sets how long to wait until intiating the sell default = 25m
    k = Kraken(timer_minutes=timer_minutes, test_run=test_run)
    total_runs = 0
    total_new_tweets = 0
    total_doge_tweets = 0
    while True:
        result = Bot.get_user_last_tweet("elonmusk")
        if not result[0]:
            print_header()
            print("Error: {}".format(result[1]))
        elif type(result) is not str:
            total_new_tweets += 1
            print_header()
            tweet = result[0]
            fmt = '%Y-%m-%d %H:%M:%S'
            tweet_time = gmt.localize(tweet.created_at)
            local_time = tweet_time.astimezone(local)
            print("\n{} - {}".format(local_time.strftime(fmt), tweet.full_text))
            if Bot.is_sequence_in_text("doge",tweet.full_text):
                total_doge_tweets += 1
                print_header()
                k.buy_doge(buy_ammount)
        else: 
            print_header()
            print(result)
        k.check_sell_doge()
        
        #time to sleep before checking tweets again
        mySleep(sleep_time)
        total_runs += 1