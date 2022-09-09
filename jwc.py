
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

path = r'F:\Fintech\Rcrawler'
if not os.path.exists(path):
    os.mkdir(path)
os.chdir(path)
 
start_urls = [r'http://jwc.dufe.edu.cn/index.php/article/notice.html?page=' + str(x) for x in range(1,24) ]

myHttpheader = {  
  "User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
  "Accept": r"text/css,*/*;q=0.1",
  "Accept-Language": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
  "Connection": r"keep-alive",
  "Accept-Encoding": r"gzip, deflate"  
}


# 
def crawl_jwc_url(url):
    # url = start_urls[0]
    urls = []
    try: 
        web = requests.get(url, headers = myHttpheader)
        web.encoding = 'utf-8' # important
        soup = BeautifulSoup(web.text, 'lxml')
        pattern = r'index.php/article/detail/id/'
        urls = [x['href'] for x in soup.find_all('a', href = re.compile(pattern, re.I))]
        urls = list(set(urls))
    except:
        print(web.status_code)
        print('%s is not found' %(url))
    return urls

jwc_urls = []
for url in start_urls:
        jwc_urls = jwc_urls + crawl_jwc_url(url)
        info_all = []    
for url in jwc_urls: 
        time.sleep(random.randint(1,5)/10)
        info = get_jwc_info(url)
        info_all = info_all + [info]
        
        info_all = pd.DataFrame(info_all):

# info_all_name = [x.text for x in soup.find_all('span', class_ = 'pl') if x.find_parents('div', id = 'info') != []]
def get_jwc_info(url):
    info = {}
    try:
        # url = urls[0]
        web = requests.get(url, headers = myHttpheader)
        web.encoding = 'utf-8' # important
        soup = BeautifulSoup(web.text, 'lxml') 
        title_year = re.split(re.compile('[\(\)]'),re.sub('\n','',soup.findAll('h1')[0].text))
        info['movie_name'] = title_year[0]
        info['year'] = title_year[1]
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


    # set the work file directory
  
    # Get the start urls.
    
    
    
    


# 250]:

info_all


#  ]:



