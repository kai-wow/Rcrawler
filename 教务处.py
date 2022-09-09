# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 16:16:28 2019
# coding: utf-8
# # download notes from dufe web
# @author: Jlr 
# @class:1702
# @student number:2017210657
# @email: 1137670964@qq.com
# @version: 3.7
# @date2019-12-7

"""
import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import time

myHttpheader = {
  "User-Agent" : r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0", 
  "Accept" : r"text/css,*/*;q=0.1",
  "Accept-Language" : r"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
  "Connection" : r"keep-alive",
  "Accept-Encoding" : r"gzip, deflate",
  "Host" : r"jwc.dufe.edu.cn"
  }



def get_note_urls(url):
    # url = start_urls[0]
    try: 
        web = requests.get(url, headers = myHttpheader)
        web.encoding = 'utf-8'
        soup = BeautifulSoup(web.text, 'lxml')
        pattern = r'index.php/article/detail/id/'
        urls = ['http://jwc.dufe.edu.cn/'+x['href'] for x in soup.find_all('a', href = re.compile(pattern,re.I))]
        urls = list(set(urls))
        
    except:
        print(web.status_code)
        print('%s is not found' %(url))
        urls = []
    return urls

def get_note_info(url):
    info = {}
    try:
        # url = urls[0]
        web = requests.get(url, headers = myHttpheader)
        web.encoding = 'utf-8'
        soup = BeautifulSoup(web.text, 'lxml') 
        info['title'] = soup.findAll('h3')[0].text
        info['time'] = soup.find(class_="data").text
            
    except:
        print(web.status_code)
        print('%s is not found' %(url))

    return info

if __name__ == '__main__':
    path = r'E:\R\Rcrawler'
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)

    start_urls = [r'http://jwc.dufe.edu.cn/index.php/article/notice.html?page=' + str(x) for x in range(1,24) ]
    
    dufenote_urls = []
    for url in start_urls:
        dufenote_urls = dufenote_urls + get_note_urls(url)
    info_all = []    
    for url in dufenote_urls:
        time.sleep(random.randint(1,5)/10)
        info = get_note_info(url)
        info_all = info_all + [info]
        
    info_all = pd.DataFrame(info_all)

info_all




