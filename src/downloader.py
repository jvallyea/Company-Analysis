import numpy as np
import pandas as pd
import yfinance as yf
import requests, sys
from bs4 import BeautifulSoup

'''
This class is used to download any relevant datasets for use.
Datasets are typically downloaded from the web and stored in sub-folders within
the webresource folder in the current directory.
'''
class Downloader:
    def __init__(self):
        self.saveFilePath = os.getcwd()

    '''
    Method that extracts SPX data from the Wikipedia page on the list of S&P 500 companies
    and saves it in ./tickers/spx_tickers.pckl.
        @param: None
        @return: None
    '''
    def getSPXTickers():
        URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
        res = requests.get(URL).text
        soup = BeautifulSoup(res, 'lxml')

        # Generates a CIK set to only add unique companies with a unique CIK ID
        # This is important since several companies might have different share classes
        CIKS = set()

        # Sets up the SPX dictionary to store the values from each company
        spx_dict = {}
        spx_dict['ticker'] = [] ; spx_dict['security'] = []
        spx_dict['sector'] = [] ; spx_dict['cik'] = []

        # Loops through the first 506 (505) table rows on the Wikipedia page
        # 5 companies have different share classes available to investors
        for items in soup.find('table', class_='wikitable').find_all('tr')[1:506]:
            data = items.find_all(['td'])
            if data[7] not in CIKS:
                CIKS.add(data[7])

                # This little bit of trickery accounts for the edge-case of the security 'BF.B'
                # which should be 'BF-B'
                if '.' in data[0].text:
                    spx_dict['ticker'].append(data[0].text.strip('\n').replace('.','-'))
                else:
                    spx_dict['ticker'].append(data[0].text.strip('\n'))

                spx_dict['security'].append(data[1].text.strip('\n'))
                spx_dict['sector'].append(data[3].text.strip('\n'))
                spx_dict['cik'].append(data[7].text.strip('\n'))

        spx_tickers = pd.DataFrame.from_dict(spx_dict)
        spx_tickers.to_pickle(self.saveFilePath + '/tickers/spx_tickers.pkl')
