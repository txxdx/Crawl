# -*- coding: utf-8 -*-
import os
import csv
import codecs
import requests
from lxml import html

headers = {
    'Host': 'sanban.qichacha.com',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
}

def crawl(url):
    resp = requests.get(url, headers=headers)
    page = resp.content
    root = html.fromstring(page)
    items = root.xpath('//*[@id="searchlist"]/table/tbody/tr')
    for item in items:
        detailUrl = 'http://sanban.qichacha.com' + item.xpath('td[2]/a/@href')[0]
        # print(detailUrl)
        detail(detailUrl)

def detail(url):
    resp = requests.get(url, headers=headers)
    page = resp.content
    root = html.fromstring(page)
    fullName = root.xpath('//*[@id="business-content"]/div/div[2]/table/tbody/tr[1]/td[2]/a/text()')[0].strip()
    shortName = root.xpath('//*[@id="business-content"]/div/div[2]/table/tbody/tr[2]/td[2]/text()')[0].strip()
    companyCode = root.xpath('//*[@id="business-content"]/div/div[2]/table/tbody/tr[1]/td[4]/text()')[0].strip()
    phone = root.xpath('//*[@id="business-content"]/div/div[2]/table/tbody/tr[6]/td[2]/text()')[0].strip()
    address = root.xpath('//*[@id="business-content"]/div/div[2]/table/tbody/tr[8]/td[2]/text()')[0].strip()

    # print(fullName, shortName, companyCode, phone)
    item = [fullName, shortName, companyCode, phone, address]
    with open('test.csv', 'a') as csv_file:
        writer = csv.writer(csv_file, dialect='excel')
        writer.writerow(item)

if __name__ == '__main__':
    with open('test.csv', 'wb') as csv_file:
        csv_file.write(codecs.BOM_UTF8)
    for id in range(1, 29):
        url = 'http://sanban.qichacha.com/search/index.shtml?key=%E8%8B%8F%E5%B7%9E&p=' + str(id)  
        crawl(url)