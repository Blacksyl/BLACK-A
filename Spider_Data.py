import urllib.request as ur
from bs4 import BeautifulSoup
# import urllib3


# -*- coding: utf-8 -*


class GetData():


    def __init__(self, year, season):

        self.year = year
        self.season  = season
        self.soup = None

    def SpiderData(self):

        url = 'http://quotes.money.163.com/trade/lsjysj_zhishu_399300.html?year='
        list = []
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/2010010 Firefox/62.0'}
        temp = url + str(self.year) + '&season=' + str(self.season)
        req = ur.Request(url=temp, headers=headers)
        html = ur.urlopen(req).read()
        self.soup = BeautifulSoup(html, 'lxml')
        self.Spider(list)
        return list


    def Spider(self,list):

        tag = self.soup.find('table', {'class': "table_bg001 border_box limit_sale"})
        data = tag.find_all('td')
        for i in data:
            list.append(i.text)

