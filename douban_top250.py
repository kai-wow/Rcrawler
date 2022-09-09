
# coding: utf-8

# #  crawler the website data from jwc.dufe

# @author: chen xue
# 
# @affilication: DUFE
# 
# 
# @version: 0.1

# 245]:

# import the modules
import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup
import random
import time
# import json


# 246]:

# define the my http header
myHttpheader = {  
  "User-Agent": r"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
  "Accept": r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
  "Accept-Language": r"zh-CN,zh;q=0.8",
  "Connection": r"keep-alive",
  "Accept-Encoding": r"gzip, deflate, sdch"  
}


# Define the function to get all top 250 movies urls.

# 
def get_top250_urls(url):
    # url = start_urls[0]
    try: 
        web = requests.get(url, headers = myHttpheader)
        web.encoding = 'utf-8' # important
        soup = BeautifulSoup(web.text, 'lxml')
        pattern = r'https://movie.douban.com/subject/'
        urls = [x['href'] for x in soup.find_all('a', href = re.compile(pattern, re.I))]
        urls = list(set(urls))
    except:
        print(web.status_code)
        print('%s is not found' %(url))
        urls = []
        return urls


# Define the function to get the information of a movie.

# 248]:

# info_all_name = [x.text for x in soup.find_all('span', class_ = 'pl') if x.find_parents('div', id = 'info') != []]
def get_movie_info(url):
    info = {}
    try:
        # url = urls[0]
        web = requests.get(url, headers = myHttpheader)
        web.encoding = 'utf-8' # important
        soup = BeautifulSoup(web.text, 'lxml') 
        title_year = re.split(re.compile('[\(\)]'),re.sub('\n','',soup.findAll('h3')[0].text))
        info['title'] = title_year[0]
        info['time'] = title_year[1]
        info_all = soup.findAll('div', id = "info")[0].text
        info_all = [re.split("[:：]",x.strip(), maxsplit=1) for x in re.split('\n', info_all) if x != '']
        info.update(dict(info_all))
        info['rate'] = soup.find(class_="ll rating_num").text
        info['people'] = soup.find('span',property="v:votes").text
        rate_star = dict(zip(['5星','4星','3星','2星','1星'],[x.text for x in soup.find_all('span',class_="rating_per")]))
        info.update(rate_star)        
    except:
        print(web.status_code)
        print('%s is not found' %(url))
        return info


# 249]:

if __name__ == '__main__':
    # set the work file directory
    path =  r'D:\pc' # r'F:\Fintech\Rcrawler'
    if not os.path.exists(path):
        os.mkdir(path)
    os.chdir(path)
    
    # Get the start urls.
    start_urls = [r'https://movie.douban.com/top250?start=' + str(x * 25) + r'&filter=' for x in range(10) ]
    
    top250_urls = []
    for url in start_urls:
        top250_urls = top250_urls + get_top250_urls(url)
    info_all = []    
    for url in top250_urls:
        time.sleep(random.randint(1,5)/10)
        info = get_movie_info(url)
        info_all = info_all + [info]
        
    info_all = pd.DataFrame(info_all)
    
    print(info_all)

# 250]:

# info_all


#  ]:



