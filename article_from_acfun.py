#!/usr/bin/env python
# encoding: utf-8

# @version: 0.1
# @file: article_from_acfun.py
# @author: oldestcrab
# @license: MIT Licence
# @software: PyCharm
# @time: 2019/12/9 17:14
# @description： 获取A站两天之内评论数超过100的文章

import os
import time
from multiprocessing import Pool

import requests

def article_from_acfun(url, limit, comment=100, page=5):
    """
    获取2天之内发布的评论数超过100的文章
    :params url: 文章api链接
    :params limit: 2天前的时间(s)
    :params comment: 文章评论总数
    :params page: 文章爬取页数
    """
    # 循环爬取所有页码
    for i in range(1, page+1):
        # 参数
        params = {
            'pageNo':str(i),
        }
        # headers
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36 QIHU 360EE',
        }
        # 访问api接口
        try:
            response = requests.get(url, headers=headers, params=params)
            # 判断访问是否成功
            if response.status_code == 200:
                try:
                    # 解析json
                    response_dict = response.json()
                    # 获取文章列表
                    articleList = response_dict.get('data', {}).get('articleList', [])
                    for article in articleList:
                        # 获取文章发布时间
                        contribute_time = int(article.get('contribute_time')/1000)
                        article_time = str(time.localtime(contribute_time).tm_year) + '-' + str(time.localtime(contribute_time).tm_mon)+ '-' + str(time.localtime(contribute_time).tm_mday)
                        # 评论数
                        comment_count = article.get('comment_count')
                        # 判断是否为2天之内发布的文章,且评论总数超过100
                        if contribute_time >= limit and comment_count >= comment:
                            # 标题
                            title = article.get('title')
                            # 描述
                            description = article.get('description')
                            # 用户
                            username = article.get('username')
                            # id
                            id = article.get('id')
                            article_url = 'https://www.acfun.cn/a/ac' + str(id)

                            print('='*50)
                            print('进程', os.getpid(), title, '(用户:', username, ')')
                            # print('描述\t', description)
                            print('评论:', comment_count, '\t发布时间:', article_time)
                            print('链接:', article_url)
                            print('='*50)


                except Exception as e:
                    print('api数据解析失败', e.args)

        except Exception as e:
                    print('api接口访问失败', e.args)

if __name__ == '__main__':
    print('start', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    start = time.time()

    # 2天之内发布的文章
    limit_contribute_time = start - 3*24*60*60

    start_urls = [
        'https://webapi.acfun.cn/query/article/list?size=100&realmIds=25%2C34%2C7%2C6%2C17%2C1%2C2&originalOnly=false&orderType=2&periodType=-1&filterTitleImage=true',
        'https://webapi.acfun.cn/query/article/list?size=100&realmIds=5,22,3,4&originalOnly=false&orderType=2&periodType=-1&filterTitleImage=true',
    ]
    # 创建进程池
    po = Pool(2)
    for url in start_urls:
        # 取2天之内发布的评论数超过100的文章
        # article_from_acfun(url, limit_contribute_time)
        po.apply_async(article_from_acfun, (url, limit_contribute_time))

    # 闭合进程池
    po.close()
    # 阻塞主进程，等待子进程完成
    po.join()
    print('stop', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print('all', time.time()-start)