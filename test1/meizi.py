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
    # r.encoding = 'gb2312'
    return r.text

def get_pic_list(html, refererUrl):
    '''
    获取每个页面的套图列表,之后循环调用get_pic函数获取图片
    '''
    soup = BeautifulSoup(html, 'html.parser')
    
    pic_list = soup.find(id="pins").find_all('li')

    for i in pic_list:
        
        a_tag = i.find('a')

        link = a_tag.get('href').strip()
        dataoriginal = a_tag.find('img').get('data-original')

        text = i.find('span').find('a').get_text();

        imageListPage(link, text)



def imageListPage(link, text):
    
    """
        爬取图片分页列表
    """

    html = download_page(link)
    soup = BeautifulSoup(html, 'html.parser')
    
    src = soup.find('div',class_="main-image")
    if(src):

        # print(src)
        _src = src.find("a").find('img').get('src')
        # subHref = src.find("a").get('')

        # print(_src)
        if(_src):
            _t = [];
            imageList = soup.find('div', class_="pagenavi").find_all('a')
            for image in imageList:
                pageHref = image.get('href')
                _t.append(pageHref)

            end = int(_t[-2].split('/')[-1])
            start = 1
            while start <= end:
                detailImage = link + '/' + str(start)
                print(detailImage)
                start = start + 1
                print(start)
                imageDetail(detailImage, text)


def imageDetail(link, text):
    ### 取得图片
    html = download_page(link)
    soup = BeautifulSoup(html, 'html.parser')
    
    src = soup.find('div',class_="main-image")
    if(src):
        _src = src.find("a").find('img').get('src')
        if(_src):
            downloadImage(_src, text, link)


def downloadImage(link, text, refererUrl):
    """
    下载图片
    """
    create_dir('meizi/{}'.format(text))

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    headers['Referer'] = refererUrl

    r = requests.get(link, headers=headers)
    fileName = link.split('/')[-1]

    with open('meizi/{}/{}'.format(text, fileName), 'wb') as f:
        f.write(r.content)
        time.sleep(1)   # 休息一下，不要给网站太大压力，避免被封

def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

def execute(url):
    page_html = download_page(url)
    get_pic_list(page_html, url)


def main():
    create_dir('meizi')
    queue = [i for i in range(10, 20)]   # 构造 url 链接 页码。
    threads = []
    while len(queue) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 5 and len(queue) > 0:   # 最大线程数设置为 5
            cur_page = queue.pop(0)
            
            #url = 'https://meizitu.com/a/more_{}.html'.format(cur_page)
            url = 'https://www.mzitu.com/japan/page/{}/'.format(cur_page)


            thread = threading.Thread(target=execute, args=(url,))
            thread.setDaemon(True)
            thread.start()
            print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))
            threads.append(thread)


if __name__ == '__main__':
    main()