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
    pic_list = soup.find('div',class_='listmain').find_all('dd')

    for i in pic_list:

        name = i.find('a').get_text().strip()
        href = i.find('a').get('href')
        url = 'https://www.biqukan.com' + href

        # print(url)
        # print(name)
        downloadText(url)

        # get_pic(link, text)

def downloadText(url):
    html = download_page(url)
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.find('div', id="content").get_text().strip()
    title = soup.find('div',class_="content").find('h1').get_text().strip()

    f = open('novel.log', 'a+')
    f.write('\n\n' + title + '\n\n')
    f.write(text  + '\n')
    

def create_dir(name):
    if not os.path.exists(name):
        os.makedirs(name)

def execute(url):
    page_html = download_page(url)
    get_pic_list(page_html)


def main():

    create_dir('novel')
    url = 'https://www.biqukan.com/21_21395/'
    execute(url)

    '''
    queue = [i for i in range(1, 19)]   # 构造 url 链接 页码。
    threads = []
    
    while len(queue) > 0:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < 2 and len(queue) > 0:   # 最大线程数设置为 5
            cur_page = queue.pop(0)
            
            #url = 'https://meizitu.com/a/more_{}.html'.format(cur_page)
            url = 'https://hf.lianjia.com/xiaoqu/binhuxinqu/pg{}/'.format(cur_page)

            thread = threading.Thread(target=execute, args=(url,))
            thread.setDaemon(True)
            thread.start()
            print('{}正在下载{}页'.format(threading.current_thread().name, cur_page))
            threads.append(thread)

    '''

if __name__ == '__main__':
    main()