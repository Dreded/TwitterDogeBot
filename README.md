# TwitterDogeBot

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

![Screenshot](screencap.png?raw=true "Title")
