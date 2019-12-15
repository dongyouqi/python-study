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

def get_pic_list(html):
    '''
    获取每个页面的套图列表,之后循环调用get_pic函数获取图片
    '''
    soup = BeautifulSoup(html, 'html.parser')
    pic_list = soup.find_all('li', class_='xiaoquListItem')

    for i in pic_list:
        
        # name = i.find('.info').get_text()
        name = i.find('div', class_='info').find('div', class_='title').get_text().strip()
        print(name)
        price = i.find('div', class_='totalPrice').get_text().strip()
        rent = i.find('div', class_='houseInfo').get_text().strip()
        rent = rent.replace("\n",'')
        dirPath = time.strftime("%Y%m%d", time.localtime())
        fileName = time.strftime("%Y%m%d%H", time.localtime())
        fileName = 'log/' + dirPath + '/' + fileName + '-binhuxinqu.log'

        f = open(fileName, 'a+')
        f.write(name + "\n")
        # f.write(name + ' | ' + price  + ' | ' + rent  + '\n')
        # get_pic(link, text)

def get_pic(link, text):
    '''
    获取当前页面的图片,并保存
    '''
    html = download_page(link)  # 下载界面
    soup = BeautifulSoup(html, 'html.parser')

    pic_list = soup.find('div', class_="swiper-wrapper").find_all('img')  # 找到界面所有图片

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"}
    create_dir('bdz/{}'.format(text))
    for i in pic_list:
        pic_link = i.get('src')  # 拿到图片的具体 url
        # print(pic_link)

        if(pic_link == '/style/images/grey.gif'):
        	pic_link = i.get('_src')
       		print(pic_link)


        r = requests.get(pic_link, headers=headers)  # 下载图片，之后保存到文件
        
        # print(r.content)

        fileName = pic_link.split('-')[0].split('/')[-1]

        # print(fileName)

        with open('bdz/{}/{}'.format(text, fileName), 'wb') as f:
            f.write(r.content)
            time.sleep(1)   # 休息一下，不要给网站太大压力，避免被封


def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

def execute(url):
    page_html = download_page(url)
    get_pic_list(page_html)


def main():

    dirPath = time.strftime("%Y%m%d", time.localtime())
    create_dir('log/' + dirPath)

    queue = [i for i in range(1, 19)]   # 构造 url 链接 页码。
    threads = []
    while len(queue) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 3 and len(queue) > 0:   # 最大线程数设置为 5
            cur_page = queue.pop(0)
            
            #url = 'https://meizitu.com/a/more_{}.html'.format(cur_page)
            url = 'https://hf.lianjia.com/xiaoqu/binhuxinqu/pg{}/'.format(cur_page)

            thread = threading.Thread(target=execute, args=(url,))
            thread.setDaemon(True)
            thread.start()
            print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))
            threads.append(thread)


if __name__ == '__main__':
    main()