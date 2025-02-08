cfrom datetime import datetime
import yfinance as yf
import numpy as np
from monteCarloOptionsPricer import OptionPricer
ticker = "AAPL"
stock = yf.Ticker(ticker)

treasury_data = yf.Ticker("^TNX") 
risk_free_rate = treasury_data.history(period="1d")["Close"].iloc[-1] / 100  


first_date = stock.options[0]

options_data = stock.option_chain(first_date)
calls = options_data.calls

today = datetime.today()
current_price = stock.history(period="1d")["Close"].iloc[-1]


puts = options_data.puts
# callPutPairs = []
# for i in range(len(calls['volume'])):
#     strike = calls['strike'][i]
#     for j in range(len(puts['volume'])):
#         if abs(strike - puts['strike'][j]) < 0.01:
#             callPutPairs.append([i, j])

# for pair in callPutPairs:
#     strike = calls['strike'][pair[0]]
#     callPrice = calls['lastPrice'][pair[0]]
#     putPrice = puts['lastPrice'][pair[1]]
#     expiration_date_str = first_date
#     expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d")
#     time_to_expiry_days = (expiration_date - today).days
#     syntheticPrice = callPrice - putPrice 
#     realPrice = current_price - strike * np.exp(-risk_free_rate*(time_to_expiry_days/365)) 
#     if ((realPrice - syntheticPrice)/realPrice > 0.1):
#         if realPrice > syntheticPrice:
#             print("Buy the call option: " + str(calls['contractSymbol'][pair[0]]))
#             print("Sell the put option: " + str(puts['contractSymbol'][pair[0]]))
#             print("Sell AAPL")
#         else:
#             print("Sell the call option: " + str(calls['contractSymbol'][pair[0]]))
#             print("Buy the put option: " + str(puts['contractSymbol'][pair[0]]))
#             print("Buy AAPL") 


callPutPairs = []
for i in range(len(calls['volume'])):
    strike = calls['strike'][i]
    for j in range(len(puts['volume'])):
        if abs(strike - puts['strike'][j]) < 0.01:
            callPutPairs.append([i, j, strike])

for pair1 in callPutPairs:
    for pair2 in callPutPairs:
        strike1 = pair1[-1]
        strike2 = pair2[-1]
        if pair1 == pair2 or strike1 > strike2:
            continue
        c1 = (calls['bid'][pair1[0]] + calls['ask'][pair1[0]])/2
        c2 = (calls['bid'][pair2[0]] + calls['ask'][pair2[0]])/2
        p1 = (puts['bid'][pair1[1]] + puts['ask'][pair1[1]])/2
        p2 = (puts['bid'][pair2[1]] + puts['ask'][pair2[1]]) / 2
        netCost = (c1 - c2) + (p1 - p2)
        payOff = strike2 - strike1
        callIV1 = calls['impliedVolatility'][pair1[0]]
        callIV2 = calls['impliedVolatility'][pair2[0]]
        putIV1 = puts['impliedVolatility'][pair1[1]]
        putIV2 = puts['impliedVolatility'][pair2[1]]
        ivSkew1 = (putIV1 - callIV1)/callIV1
        ivSkew2 = (putIV2 - callIV2)/callIV2
        if ivSkew1 > 0.2 and ivSkew2 > 0.2 and payOff > netCost:
            print(c1, c2, p1, p2, strike1, strike2)

callPutPairs = []
for i in range(len(calls['volume'])):
    strike_i = calls['strike'][i]
    expiration_i = calls['expiration'][i]
    for j in range(len(puts['volume'])):
        strike_j = puts['strike'][j]
        expiration_j = puts['expiration'][j]
        if abs(strike_i - strike_j) < 0.01 and expiration_i != expiration_j:
            callPutPairs.append([i, j, strike_i, expiration_i, expiration_j])

for pair1 in callPutPairs:
    for pair2 in callPutPairs:
        if pair1[2] != pair2[2] or pair1 == pair2:
            continue
        c1 = (calls['bid'][pair1[0]] + calls['ask'][pair1[0]]) / 2
        p1 = (puts['bid'][pair1[1]] + puts['ask'][pair1[1]]) / 2
        c2 = (calls['bid'][pair2[0]] + calls['ask'][pair2[0]]) / 2
        p2 = (puts['bid'][pair2[1]] + puts['ask'][pair2[1]]) / 2
        if pair1[3] < pair2[3]:
            netCost = (c1 - p1) - (c2 - p2)
        else:
            netCost = (c2 - p2) - (c1 - p1)
        print(f"Strike: {pair1[2]}, Roll from {pair1[3]} to {pair2[3]}, Net cost: {netCost:.2f}")
