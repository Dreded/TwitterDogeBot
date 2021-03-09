# TwitterDogeBot
![Example_Screenshot](screencap.png?raw=true "Example")
This is a work in progress... but done for now, there is minimal error checking... shouldn't be an issue though iv had it running for weeks.

This bot buys and sells DOGE coin(or really easily changeable to any crypto) using BTC in Kraken Exchange using their API.

It buys each time the target user such as elonmusk tweets anything containing doge so the following would initiate a buy.
* doge
* DOGE
* Doge
* dogeCoin
* dogeCosajflajkhgsf
* aklsfhalsfjghbDOGEaklshjfl;ashf

it ignores replies and re-tweets by default, it then sells the dogecoin x minutes later(defaults to 25).

## Install
```
git clone https://github.com/Dreded/TwitterDogeBot.git
cd TwitterDogeBot
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
Edit credentials.py.example and save as credentials.py\
Edit main.py as needed to change target and timers.\
By default the bot will not actually do any real trading for that you would need to set test_run to False in main.py\

## Run
```
python main.py
```