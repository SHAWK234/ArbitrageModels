import yfinance as yf
import pandas as pd
import statistics
from scipy.spatial.distance import euclidean
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import math
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import scipy.spatial
from sklearn.cluster import DBSCAN
from sklearn.cluster import OPTICS
import seaborn as sns

assets = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "TSLA", "UNH",
    "LLY", "JPM", "XOM", "JNJ", "V", "PG", "AVGO", "MA", "HD", "CVX",
    "MRK", "ABBV", "PEP", "COST", "ADBE", "KO", "CSCO", "WMT", "TMO", "MCD",
    "PFE", "CRM", "BAC", "ACN", "CMCSA", "LIN", "NFLX", "ABT", "ORCL", "DHR",
    "AMD", "WFC", "DIS", "TXN", "PM", "VZ", "INTU", "COP", "CAT", "AMGN",
    "NEE", "INTC", "UNP", "LOW", "IBM", "BMY", "SPGI", "RTX", "HON", "BA",
    "UPS", "GE", "QCOM", "AMAT", "NKE", "PLD", "NOW", "BKNG", "SBUX", "MS",
    "ELV", "MDT", "GS", "DE", "ADP", "LMT", "TJX", "T", "BLK", "ISRG",
    "MDLZ", "GILD", "MMC", "AXP", "SYK", "REGN", "VRTX", "ETN", "LRCX", "ADI",
    "SCHW", "CVS", "ZTS", "CI", "CB", "AMT", "SLB", "C", "BDX", "MO",
    "PGR", "TMUS", "FI","EOG", "BSX", "CME", "EQIX", "MU",
    "PANW", "PYPL", "AON", "SNPS", "ITW", "KLAC", "LULU", "ICE", "APD", "SHW",
    "CDNS", "CSX", "NOC", "CL", "MPC", "HUM", "FDX", "WM", "MCK", "TGT",
    "ORLY", "HCA", "FCX", "EMR", "MMM", "MCO", "ROP", "CMG", "PSX",
    "MAR", "PH", "APH", "GD", "USB", "NXPI", "AJG", "NSC", "PNC", "VLO",
    "F", "MSI", "GM", "TT", "EW", "CARR", "AZO", "ADSK", "TDG", "ANET",
     "ECL", "OXY", "PCAR", "ADM", "MNST", "KMB", "PSA", "CCI", "CHTR",
    "MCHP", "MSCI", "CTAS", "WMB", "AIG", "STZ", "HES", "NUE", "ROST", "AFL",
    "KVUE", "IDXX", "D", "TEL", "JCI", "MET", "GIS", "IQV",
    "WELL", "DXCM", "HLT", "ON", "COF", "PAYX", "TFC", "BIIB", "O", "FTNT",
    "DOW", "TRV", "DLR", "MRNA", "CPRT", "ODFL", "DHI", "YUM", "SPG", "CTSH",
    "AME", "BKR", "SYY", "A", "CTVA", "CNC", "EL", "AMP", "CEG", "HAL",
    "OTIS", "ROK", "PRU", "DD", "KMI", "VRSK", "LHX", "DG", "FIS", "CMI",
    "CSGP", "FAST", "PPG", "GPN", "GWW", "HSY", "BK", "DVN", "EA",
    "NEM", "ED", "URI", "VICI", "KR", "RSG", "LEN", "PWR", "WST",
    "COR", "OKE", "VMC", "KDP", "WBA", "MTD", "EFX", "EQR", "APTV", "DLTR",
    "ALB", "AVB", "MAA", "ARE", "ZBH", "BXP", "ESS", "UDR", "VTR",
    "AMCR", "ATO", "AWK", "CNP", "ES", 
    "WEC", "AES", "AEP", "EIX",
    "ETR", "EXC", "NRG", "PEG", "PPL", "SO",
     "AEE", "CMS", "DTE", "DUK",
    "EVRG", "FE", "LNT", "NI", "PNW", "SRE"
]


start_date = "2024-01-01"
end_date = "2025-01-01"


def downloadData(name, start_date, end_date):
    stock1 = yf.download(name, start=start_date, end=end_date)
    return stock1


def calculateSSD(stock1, stock2):
    meanStock1 = sum(stock1['Adj Close'])/len(stock1['Adj Close'])
    meanStock2 = sum(stock2['Adj Close'])/len(stock2['Adj Close'])

    stdStock1 = statistics.stdev(stock1['Adj Close'])
    stdStock2 = statistics.stdev(stock2['Adj Close'])

    ssd = 0
    for i in range(min(len(stock1), len(stock2))):
        first = (stock1['Adj Close'].iloc[i] - meanStock1)/stdStock1
        second = (stock2['Adj Close'].iloc[i] - meanStock2)/stdStock2
        ssd += (first - second)**2
    return ssd

def doReturns(stock1):
    returns = []
    for i in range(len(stock1['Adj Close']) - 1):  
        simple_return = stock1['Adj Close'].iloc[i + 1] - stock1['Adj Close'].iloc[i]
        percent_return = (simple_return / stock1['Adj Close'].iloc[i]) * 100
        returns.append(percent_return)  
    return returns


def golden_section_search(f, a, b, tol=1e-5):
    gr = (math.sqrt(5) + 1) / 2  # Golden ratio
    c = b - (b - a) / gr
    d = a + (b - a) / gr
    while abs(c - d) > tol:
        if f(c) > f(d):
            b = d
        else:
            a = c
        c = b - (b - a) / gr
        d = a + (b - a) / gr
    return (b + a) / 2

def trim_data(array1, array2):
    min_length = min(len(array1), len(array2))
    return array1[:min_length], array2[:min_length]



def calculatePCADistance(stock1Returns, stock2Returns):
    meanStock1 = np.mean(stock1Returns)
    meanStock2 = np.mean(stock2Returns)

    transformedStock1Returns = np.array(stock1Returns) - meanStock1
    transformedStock2Returns = np.array(stock2Returns) - meanStock2
    transformedStock1Returns, transformedStock2Returns = trim_data(transformedStock1Returns, transformedStock2Returns)

    def total_distance(theta):
        cos_theta = math.cos(math.radians(theta))
        sin_theta = math.sin(math.radians(theta))
        distances = ((transformedStock1Returns * cos_theta + transformedStock2Returns * sin_theta) ** 2)
        return -np.sum(distances)

    max_theta = golden_section_search(total_distance, 0, 180, tol=1e-5)

    theta_rad = math.radians(max_theta)
    R = np.array([[math.cos(theta_rad), -math.sin(theta_rad)],
                  [math.sin(theta_rad), math.cos(theta_rad)]])
    
    data_matrix = np.vstack([transformedStock1Returns, transformedStock2Returns])
    rotated_data = R @ data_matrix

    return secondCalculatePCADistance(rotated_data[0], rotated_data[1])

def secondCalculatePCADistance(rotatedTransformedStock1Returns, rotatedTransformedStock2Returns):
    return np.linalg.norm(rotatedTransformedStock1Returns - rotatedTransformedStock2Returns)



distance_matrix = np.zeros((len(assets), len(assets)))

assetsDataFrame = []
for name in assets:
    assetsDataFrame.append(downloadData(name, start_date, end_date))

n = len(assetsDataFrame)

for first_index in range(n):
    #stock1Returns = doReturns(assetsDataFrame[first_index])
    for second_index in range(first_index, n):
        #stock2Returns = doReturns(assetsDataFrame[second_index])
        pca_distance = calculateSSD(assetsDataFrame[first_index], assetsDataFrame[second_index])
        #pca_distance = calculatePCADistance(stock1Returns, stock2Returns)
        distance_matrix[first_index][second_index] = pca_distance
        distance_matrix[second_index][first_index] = pca_distance

# distance_matrix_int = np.round(distance_matrix).astype(int)
# sns.heatmap(distance_matrix_int, annot=False, fmt="d", cmap="YlGnBu")
# plt.title("Heatmap with Seaborn")
# plt.show()


# dbscan = DBSCAN(eps=25, min_samples=2, metric='precomputed')
# # clusters = dbscan.fit_predict(distance_matrix)

# # print("Cluster labels:", clusters)

from collections import defaultdict

optics_model = OPTICS(metric='precomputed', min_samples=2)
optics_model.fit(distance_matrix)

clusters = optics_model.labels_

cluster_dict = defaultdict(list)
for idx, cluster in enumerate(clusters):
    cluster_dict[cluster].append(assets[idx])

for cluster, assets_in_cluster in cluster_dict.items():
    if cluster == -1:
        print(f"Noise points: {assets_in_cluster}")
    else:
        print(f"Cluster {cluster}: {assets_in_cluster}")








#eps = 10
# Cluster 0: ['GOOGL', 'GOOG']
# Cluster 1: ['PM', 'MSI', 'WELL', 'ATO', 'WEC', 'PPL', 'AEE', 'EVRG', 'LNT', 'NI', 'PNW']
# Cluster 2: ['ADP', 'PAYX']
# Cluster 3: ['T', 'BK']
# Cluster 4: ['SRE', 'SRE']
# Cluster 5: ['WMB', 'KMI', 'OKE']
# Cluster 6: ['D', 'D']
# Cluster 7: ['EQR', 'AVB', 'MAA', 'ESS', 'UDR']
# Cluster 8: ['AEP', 'AEP']
# Cluster 9: ['EIX', 'SO', 'DUK']
# Cluster 10: ['CMS', 'DTE']

# Cluster 0: ['GOOGL', 'GOOG']
# Cluster 1: ['ADP', 'PAYX']
# Cluster 2: ['SRE', 'SRE']
# Cluster 3: ['WMB', 'KMI']
# Cluster 4: ['D', 'D']
# Cluster 5: ['EQR', 'AVB', 'ESS', 'UDR']
# Cluster 6: ['ATO', 'AEE']
# Cluster 7: ['AEP', 'AEP']
# Cluster 8: ['PPL', 'EVRG', 'NI']
# Cluster 9: ['SO', 'DUK']
# Cluster 10: ['CMS', 'DTE']


# Cluster 0: ['JPM', 'COST', 'BSX', 'APH', 'TT', 'HLT', 'NRG']
# Cluster 9: ['PFE', 'UPS', 'NKE', 'HUM', 'ADM', 'BIIB', 'MRNA', 'EL', 'DG', 'WBA', 'APTV', 'DLTR', 'ALB']
# Cluster 2: ['WFC', 'COF', 'AMP']
# Cluster 3: ['PM', 'MO', 'ATO', 'ETR', 'NI']
# Cluster 10: ['INTC', 'LULU', 'MNST', 'PPG', 'GPN']
# Cluster 6: ['AMAT', 'LRCX', 'KLAC', 'NXPI']
# Cluster 1: ['TDG', 'ECL', 'RSG']
# Cluster 8: ['GIS', 'HSY', 'ES']
# Cluster 4: ['EQR', 'AVB', 'ESS']
# Cluster 7: ['MAA', 'UDR', 'WEC', 'AEE', 'EVRG']
# Cluster 5: ['AEP', 'PPL', 'CMS', 'DTE', 'FE']