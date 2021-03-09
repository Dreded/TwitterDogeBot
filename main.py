import datetime
import pytz
from time import sleep
from bot import Bot
from kraken import Kraken

gmt = pytz.timezone('GMT')
local = pytz.timezone('America/Vancouver')

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
    k = Kraken(timer_minutes=1, test_run=True)
    while True:
        print("\nGetting Last Tweet...",end="")
        result = Bot.get_user_last_tweet("elonmusk")
        if type(result) is not str:
            fmt = '%Y-%m-%d %H:%M:%S'
            tweet_time = gmt.localize(result.created_at)
            local_time = tweet_time.astimezone(local)
            print("\n{} - {}".format(local_time.strftime(fmt), result.full_text))
            if Bot.is_sequence_in_text("doge",result.full_text):
                k.buy_doge(50)
        else: 
            print(result)
        k.check_sell_doge()
        
        #time to sleep before checking tweets again
        mySleep(30)