# -*- coding: utf-8 -*-

import requests
import os
import time
import threading
from bs4 import BeautifulSoup
import sys

reload(sys)

sys.setdefaultencoding('utf8')

def download_page(url):
    
    '''
    用于下载页面
    '''

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    r = requests.get(url, headers=headers)
    r.encoding = 'UTF-8'
    return r.text


def detail(url ,fileName):
    html = download_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    src = soup.find('div',class_="pics")
    if(src):
        imageList = src.find_all('img')
        for image in imageList:
            imageUrl = image.get('src')
            print(imageUrl)
            downloadImage(imageUrl,fileName,url)



def getList(url):
    """
    取得图片链接
    """
    baseUrl = "https://3332v.com"
    html = download_page(url)
    soup = BeautifulSoup(html, 'html.parser')

    src = soup.find('div',class_="tu_list")
    if(src):
        
        imageList = src.find_all('a')
        for image in imageList:
                pageHref = baseUrl + image.get('href')
                title = image.get('title')
                print(pageHref)
                print(title)
                detail(pageHref, title)




def downloadImage(link, text, refererUrl):
    """
    下载图片
    """
    create_dir('imagesBak/{}'.format(text))

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    headers['Referer'] = refererUrl

    r = requests.get(link, headers=headers)
    fileName = link.split('/')[-1]

    with open('imagesBak/{}/{}'.format(text, fileName), 'wb') as f:
        f.write(r.content)
        time.sleep(1)   # 休息一下，不要给网站太大压力，避免被封

def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

def main():

    create_dir('imagesBak')
    # getList('https://3332v.com/htm/Picture1/18.htm')
    getList('https://3332v.com/htm/Picture33/')
    

if __name__ == '__main__':
    main()