# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   date：          1/10/2021
-------------------------------------------------
   Change Activity:
                   1/10/2021:
-------------------------------------------------
"""
import requests
import pickle
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
import numpy as np
from selenium import webdriver


def getMarketList():
    market_listing_game_name = []
    market_listing_item_name = []
    market_listing_num_listings_qty = []
    market_listing_their_price = []
    Url = []
    bw = webdriver.Chrome()
    header = {'Cache-Control': 'no-cache',
              "User - Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
              "Host": "steamcommunity.com",
              "Pragma": "no-cache",
              "Cookie": "sessionid=cbda28383d2784566a9c4b4b; timezoneOffset=28800,0; _ga=GA1.2.1542797174.1606639175; _gid=GA1.2.1361929752.1606639175; steamCountry=TW%7C23107ad4a89584883d8f40270a540fb7"
              }
    for page in range(1, 3330 + 1):
        print(page)
        bw.get("https://steamcommunity.com/market/search?appid=570#p" + str(page) + "_popular_desc")
        HTML = bw.page_source
        soup = BeautifulSoup(HTML, features="lxml")
        samples = soup.find_all("a", "market_listing_row_link")
        for i in range(samples.__len__()):
            Item = samples[i]
            market_listing_their_price.append(
                {"normal_price": Item.find("span", {"class": "normal_price", "data-currency": "1"}).text,
                 "sale_price": Item.find("span", {"class": "sale_price"}).text})
            market_listing_num_listings_qty.append(Item.find("span", {"class": "market_listing_num_listings_qty"}).text)
            market_listing_item_name.append(Item.find("span", {"class": "market_listing_item_name"}).text)
            market_listing_game_name.append(Item.find("span", {"class": "market_listing_game_name"}).text)
            Url.append(Item.attrs['href'])
        data = pd.DataFrame({"market_listing_their_price": market_listing_their_price,
                             "market_listing_num_listings_qty": market_listing_num_listings_qty,
                             "market_listing_item_name": market_listing_item_name,
                             "market_listing_game_name": market_listing_game_name,
                             "detail_url": Url})
        data.to_excel("MarketList.xlsx", index=False)

        time.sleep(random.randint(0, 5))


def getTradeInfo():
    List = pd.read_excel("MarketList.xlsx")
    trend = []
    with open('TradeDetail.pickle', 'rb') as handle:
        trend = pickle.load(handle)

    for n, url in enumerate(List['detail_url']):
        if n <= 89:
            continue
        print(n)
        # get my entrnal ip
        # ip = requests.get('https://api.ipify.org').text
        # add ip into white list
        # requests.post(
        #     " http://api.ipidea.net/index/index/save_white?neek=173865&appkey=66cf98828abf470e63c5b2660460bcb2&white=" + ip)
        # get the proxy
        # proxy = requests.get("http://tiqu.linksocket.com:81/abroad?num=1&type=1&lb=6&sb=0&flow=1&regions=us&n=0")
        # data = requests.get(url, proxies={"http": 'http://' + proxy.text})
        data = requests.get(url)
        soup = BeautifulSoup(data.content, features="lxml")
        StringText = ''
        samples = soup.find_all('script', {'type': 'text/javascript'})
        for s in samples:
            if s.string is not None:
                if 'Market_LoadOrderSpread' in s.string:
                    StringText = s.string.split("Market_LoadOrderSpread(")[1]
                    StringText = int(StringText.split(")")[0])
                    break
        # data = requests.get(
        #     "https://steamcommunity.com/market/itemordershistogram?language=english&currency=1&item_nameid=" + str(
        #         StringText) + "&two_factor=0", proxies={"http": 'http://' + proxy.text})
        data = requests.get(
            "https://steamcommunity.com/market/itemordershistogram?language=english&currency=1&item_nameid=" + str(
                StringText) + "&two_factor=0")
        trend.append(data.json())
        with open('TradeDetail.pickle', 'wb') as handle:
            pickle.dump(trend, handle, protocol=pickle.HIGHEST_PROTOCOL)


def getMedian():
    List = pd.read_excel("MarketList.xlsx")
    trend = []
    # with open('TradeDetail.pickle', 'rb') as handle:
    #     trend = pickle.load(handle)

    for n, url in enumerate(List['detail_url']):
        proxyMeta = requests.get("http://tiqu.linksocket.com:81/abroad?num=1&type=1&lb=1&sb=,&flow=1&regions=&n=0").text
        proxies = {

            "http": "http://"+proxyMeta[0:-2],
            "https": "http://"+proxyMeta[0:-2],
        }
        print(n)
        data = requests.get(url, proxies=proxies)
        soup = BeautifulSoup(data.content, features="html.parser")
        samples = soup.find_all('script', {'type': 'text/javascript'})
        for s in samples:
            if s.string is not None and 'var line1' in s.string:
                tmpLine1 = s.string.split("var line1=[")[1]
                tmpLine1 = tmpLine1.split("];")[0]

        MedianSalePrices = np.zeros((tmpLine1.split("[").__len__() - 1, 2), dtype=np.float)

        TimeList = []
        for i, MedianString in enumerate(tmpLine1.split("[")):
            if i == 0:
                continue
            TimeList.append(MedianString.split(",")[0][1:-1])
            MedianSalePrices[i - 1, 0] = float(MedianString.split(",")[1])
            MedianSalePrices[i - 1, 1] = int(MedianString.split(",")[2][1:-2])

        trend.append(MedianSalePrices)
        with open('TradeDetail.pickle', 'wb') as handle:
            pickle.dump(trend, handle, protocol=pickle.HIGHEST_PROTOCOL)

    time.sleep(random.randint(5, 10))
if __name__ == '__main__':
    