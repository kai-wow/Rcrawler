# -*- coding: utf-8 -*-

#python 爬虫作业——东财教务处

# #  crawler the website data from jwc.dufe
# @author: chen xue
# @affilication: DUFE
# @version: 1.0


# import the modules
import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import time

#请求头
myHttpheader = {  
  "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
  "Accept": r"text/css,*/*;q=0.1",
  "Accept-Language": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
  "Connection": r"keep-alive",
  "Accept-Encoding": r"gzip, deflate"  
}

'''
path = r'F:\Fintech\pycrawler'
if not os.path.exists(path):
    os.mkdir(path)
os.chdir(path)
 
start_urls = [r'http://jwc.dufe.edu.cn/index.php/article/notice.html?page=' + str(x) for x in range(1,24) ]
'''

#通知公告每页url
def get_jwc_urls(url):
    # url = start_urls[0]
    try: 
        web = requests.get(url, headers = myHttpheader)
        web.encoding = 'utf-8'
        soup = BeautifulSoup(web.text, 'lxml')
        pattern = r'index.php/article/detail/id/'
        urls = ['http://jwc.dufe.edu.cn/'+x['href'] for x in soup.find_all('a', href = re.compile(pattern,re.I))]
        urls = list(set(urls))
        print(urls)
    except:
        print(web.status_code)
        print('error')
        urls = []
    return urls

#每页具体informations
def get_jwcmessages_info(url):
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
        print('this message not found')

    return info

if __name__ == '__main__':
    path = r'D:\pc'
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)

    start_urls = [r'http://jwc.dufe.edu.cn/index.php/article/notice.html?page=' + str(x) for x in range(1,24) ]
    
    jwc_urls = []
    for url in start_urls:
        jwc_urls = jwc_urls + get_jwc_urls(url)
    info_all = []    
    for url in jwc_urls:
        time.sleep(random.randint(1,5)/10)
        info = get_jwcmessages_info(url)
        info_all = info_all + [info]
        
    info_all = pd.DataFrame(info_all)

    print(info_all)




