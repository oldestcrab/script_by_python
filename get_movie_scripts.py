#!/usr/bin/env python
# encoding: utf-8

# @version: 0.1
# @file: get_movie_scripts.py
# @author: oldestcrab
# @license: MIT Licence
# @software: PyCharm
# @time: 2019/12/9 17:17
# @description： 获取某部英文电影的对白

import time
import chardet
import os

import  requests
from lxml import etree

def search_movie():
    """
    搜索电影
    """
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 QIHU 360EE',
    }
    try:
        # 电影名字
        movie_name = input('请输入电影名(英文):')
        # 搜索url
        search_url = 'https://www.springfieldspringfield.co.uk/movie_scripts.php?search=' + movie_name
        # 获取搜索页面
        search_response = requests.get(search_url, headers=headers)
        # 获取原网页编码
        cod = chardet.detect(search_response.content)
        search_response.encoding = cod['encoding']
        # 格式化html文档
        search_html = etree.HTML(search_response.text)
        # 存储电影搜索结果
        movie_dict = {}
        search_result = search_html.xpath('//div[@class="main-content-left"]/a')
        for i in search_result:
            name = i.xpath('string(.)')
            link = i.xpath('./@href')[0]
            movie_dict[name] = 'https://www.springfieldspringfield.co.uk' + link
        for key in list(movie_dict.keys()):
            print(list(movie_dict.keys()).index(key), '\t', key)
        num = input('请输入电影编号:')
        # 获取电影url
        movie_url = movie_dict[list(movie_dict.keys())[int(num)]]

        return movie_url
    except Exception as e:
        print(e.args)

def save_script(url):
    """
    获取字幕，保存到本地文件
    :params url: 电影字幕url
    """

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 QIHU 360EE',
    }
    try:
        response = requests.get(url, headers=headers)
        # 获取原网页编码
        cod = chardet.detect(response.content)
        response.encoding = cod['encoding']
        # 格式化html文档
        doc = etree.HTML(response.text)
        name = doc.xpath('string(//h1)')
        result = doc.xpath('//div[@class="scrolling-script-container"]/text()')
        if not os.path.exists('./result/get_movie_scripts'):
            os.makedirs('./result/get_movie_scripts')
        with open('./result/get_movie_scripts/'+name+'.txt', 'w', encoding='utf-8') as f:
            for i in result:
                f.write(i.strip() + '\n')
    except Exception as e:
        print(e.args)

if __name__ == '__main__':
    print('start', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    start = time.time()

    url = search_movie()
    if url:
        save_script(url)

    print('stop', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print('all', time.time()-start)