import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

def downloadData(name, start_date, end_date):
    stock1 = yf.download(name, start=start_date, end=end_date)
    return stock1

def standardise_series(data):
    return (data - data.mean())/data.std()


stock1Name = 'LULU'
stock2Name = 'GPN'
startDate = "2020-01-01"
endDate = "2025-01-01"

stock1 = downloadData(stock1Name, startDate, endDate)
stock2 = downloadData(stock2Name, startDate, endDate)
m, c = np.polyfit(stock1['Adj Close'], stock2['Adj Close'], 1)

predictedStock2 = stock1['Adj Close'] * m + c


def calculate_mean(lst):
    return sum(lst)/len(lst)

def calculate_std(lst):
    mean = calculate_mean(lst)
    squared_diffs = [(x - mean) ** 2 for x in lst]
    variance = sum(squared_diffs)/len(lst)
    return variance

residuals = predictedStock2 - stock2['Adj Close']

residualStandardDeviation = residuals.std()

residualMean = residuals.mean()


standardisedResiduals = standardise_series(residuals)

print(residuals)


# plt.axhline(y=2, color='black', linestyle='-')
# plt.axhline(y=-2, color='black', linestyle='-')
# plt.plot(residuals)

# plt.plot(stock2.index, stock2['Adj Close'], label='GS')
# plt.plot(stock2.index, predictedStock2, label='JPM')
plt.show()

newStock1Data = downloadData(stock1Name, "2024-01-01", "2025-01-01")
newStock2Data = downloadData(stock2Name, "2024-01-01", "2025-01-01")

index = 0
inBuy = False
inSell = False
totalStock1Purchased = {'numBought': 0, 'Value': 0}
totalProfit = 0
totalStock2Purchased = {'numBought': 0, 'Value': 0}
totalStock1Shorted = {'numBought': 0, 'Value': 0}
totalStock2Shorted = {'numBought': 0, 'Value': 0}

stock1List = []
stock2List = []
for i in newStock1Data['Adj Close']:
    stock1List.append(i)

for i in newStock2Data['Adj Close']:
    stock2List.append(i)


z_barrier = 0.5

index = 0
for i in range(min(len(stock1List), len(stock2List))):
    stock1Price = stock1List[i]
    stock2Price = stock2List[i]
    predictedStock2Price = float(m) * stock1Price + float(c)
    currentResidual = (predictedStock2Price) - (stock2Price)
    # print("residual mean: " + str(residualMean))

    if (((currentResidual - residualMean) / residualStandardDeviation) >= z_barrier) and not inBuy:
        print("Bought Fifty Shares of " + str(stock2Name) + "for " + str(stock2Price))
        inBuy = True
        totalStock2Purchased['numBought'] += 50
        totalStock2Purchased['Value'] += 50*stock2Price

        print("Shorted Fifty Shares of " + str(stock1Name) + "for " + str(stock1Price))
        totalStock1Shorted['numBought'] += 50
        totalStock1Shorted['Value'] += 50*stock1Price
    
    elif inBuy and ((currentResidual - residualMean)/residualStandardDeviation <= 0):
        inBuy = False
        print("Sold " + str(totalStock2Purchased['numBought']) + " at" + str(stock2Price))
        totalProfit += totalStock2Purchased['numBought']*stock2Price - totalStock2Purchased['Value']
        print("Sold " + str(totalStock1Shorted['numBought']) + " at" + str(totalStock1Shorted['Value']))
        totalProfit += totalStock1Shorted['Value'] - totalStock1Shorted['numBought']*stock1Price 
        totalStock2Purchased['numBought'] = 0
        totalStock2Purchased['Value'] = 0
        totalStock1Shorted['numBought'] = 0
        totalStock1Shorted['Value'] = 0

    elif (((currentResidual - residualMean) / residualStandardDeviation) >= -1 * z_barrier) and not inSell:
        print("Bought Fifty Shares of " + str(stock1Name) + "for " + str(stock1Price))
        inSell = True
        totalStock1Purchased['numBought'] += 50
        totalStock1Purchased['Value'] += 50*stock1Price
        
        print("Shorted Fifty Shares of " + str(stock2Name) + "for " + str(stock2Price))
        totalStock2Shorted['numBought'] += 50
        totalStock2Shorted['Value'] += 50*stock2Price
    
    elif inSell and ((currentResidual - residualMean)/residualStandardDeviation <= 0):
        inSell = False
        print("Sold " + str(totalStock1Purchased['numBought']) + " at" + str(stock1Price))
        print("Sold " + str(totalStock2Shorted['numBought']) + " at" + str(totalStock2Shorted['Value']))
        totalProfit += totalStock1Purchased['numBought']*stock1Price - totalStock1Purchased['Value']
        totalProfit += totalStock2Shorted['Value'] - totalStock2Shorted['numBought']*stock2Price 
        totalStock1Purchased['numBought'] = 0
        totalStock1Purchased['Value'] = 0
        totalStock2Shorted['numBought'] = 0
        totalStock2Shorted['Value'] = 0
    index += 1



# print("Unclosed Positions purchased for Stock 1: " + str(totalStock1Purchased))
# totalProfit += totalStock1Purchased['numBought']*stock1Price - totalStock1Purchased['Value']

# print("Unclosed Positions purchased for Stock 2" + str(totalStock2Purchased))
# totalProfit += totalStock2Purchased['numBought']*stock2Price - totalStock2Purchased['Value']

# print("Unclosed Positions shorted for Stock 1:" + str(totalStock1Shorted))
# totalProfit += totalStock1Shorted['Value'] - totalStock1Shorted['numBought']*stock1Price 

# print("Unclosed Positiosn shorted for Stock 2:" + str(totalStock2Shorted))
# totalProfit += totalStock2Shorted['Value'] - totalStock2Shorted['numBought']*stock2Price 


print("Total Profit" + str(totalProfit))


    



