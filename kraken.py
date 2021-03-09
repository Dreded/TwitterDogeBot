import krakenex
import datetime
import pytz
from pykrakenapi import KrakenAPI
from credentials import kraken_keys
#help(KrakenAPI)


local = pytz.timezone('America/Vancouver')

class Kraken():
    def __init__(self, timer_minutes = 25, test_run = True):
        self.test_run = test_run
        self.timer_minutes = timer_minutes

        self.api = krakenex.API(key=kraken_keys[0],secret=kraken_keys[1])
        self.k = KrakenAPI(self.api)
        self.total_qty = self.get_doge_balance()
        self.buy_time = 0
        self.buy_price = 0
        self.sell_time = datetime.datetime(year=2199, month=1, day=1, hour=2).astimezone(local)
        self.sell_price = 0

        print("Current Doge Balance: {}".format(self.total_qty))
    
    def get_balances(self):
        return self.k.get_account_balance()

    def get_doge_balance(self):
        return self.get_balances().vol['XXDG']

    def buy_doge(self,qty):
        self.buy_price = self.get_doge_price()
        print("Initiating buy of {} Doge at ${:4f} USD".format(qty,self.buy_price))
        self.total_qty += qty
        order = self.k.add_standard_order(pair="XDGXBT", type="buy", ordertype="market", volume=qty,validate=self.test_run)
        self.buy_time = datetime.datetime.now().replace(microsecond=0).astimezone(local)
        self.sell_time = self.buy_time+datetime.timedelta(minutes=self.timer_minutes)
        return order

    def check_sell_doge(self):
        if self.sell_time < datetime.datetime.now().astimezone(local):
            self.sell_doge(self.total_qty)
        elif self.sell_time-datetime.datetime.now().astimezone(local) < datetime.timedelta(days=100):
            print("Selling in:",self.sell_time-datetime.datetime.now().replace(microsecond=0).astimezone(local))
        return

    def get_doge_price(self):
        return float(self.k.get_ticker_information(pair="XDGUSD").a[0][0])

    def sell_doge(self,qty):
        self.sell_price = self.get_doge_price()
        gain_percent = ((self.sell_price - self.buy_price)/self.buy_price)*100
        return_ammount = (self.sell_price-self.buy_price)*qty
        print("Initiating sell of {} Doge at ${:4f} USD for a return of ${:.4f} USD which is a {:.4f}% gain".format(qty,self.sell_price,return_ammount,gain_percent))
        if qty > self.total_qty:
            print("Cannot sell {} Doge, we only have {} to sell.".format(qty,self.total_qty))
            return
        order = self.k.add_standard_order(pair="XDGXBT", type="sell", ordertype="market", volume=qty,validate=self.test_run)
        self.total_qty -= qty
        self.sell_time = datetime.datetime(year=2199, month=1, day=1, hour=2).astimezone(local)
        return order

if __name__ == "__main__":
    k = Kraken()
    print(k.get_balances())