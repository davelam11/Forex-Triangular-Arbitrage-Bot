# Forex-Triangular-Arbitrage-Bot

This repo use Oanda's api to place traingular arbitrage trades on the example forex pairs group "EUR_USD", "USD_JPY" and "EUR_GBP", which is 
a rare approach for most retail forex traders who focus mainly on directional trades. More forex pairs can be added simply by changing
the "instruments" list under the def main() into a list of lists or list of tuples and amend a bit the for loop to loop over the new 
list of lists or list of tuples for multiple instances of forex pairs group.
