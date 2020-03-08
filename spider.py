#!/usr/bin/env python
#-*- coding:utf8 -*-

import requests
from requests.adapters import HTTPAdapter
import time
import os
from bs4 import BeautifulSoup
import sconfig
import json

import pdb



class DouBan(object):
    def __init__(self, cookies, groups, locations, house, date = 7,  filters = []):
        self.cookies_       = cookies
        self.groups_        = groups
        self.locations_     = locations
        self.house_         = house
        self.date_          = date
        self.filters_       = filters
        self.headers_       = {
                'Host': 'www.douban.com',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
                'Sec-Fetch-Dest': 'document',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-User': '?1',
                'Referer': 'https://www.douban.com/group/',
                #'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Encoding': '',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Cookie': self.cookies_
                }
        self.ss_ = requests.Session()
        self.ss_.mount('http://', HTTPAdapter(max_retries=3))
        self.ss_.mount('https://', HTTPAdapter(max_retries=3))

        return

    def spider_topic(self, topic):
        results = []
        topic_url = topic.get('url')
        if not topic_url:
            print("topic_url(empty) invalid")
            return False 

        r = self.ss_.get(topic_url, headers = self.headers_)
        title, content = '', ''
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'lxml')
            sp_title = soup.find('table', 'infobox')
            if sp_title:
                sp_title = sp_title.find('td', 'tablecc')
                if len(sp_title) >= 2:
                    title = sp_title.contents[1]

            if not title:
                title = topic.get('title')
            sp_content = soup.find('div', 'topic-richtext')
            if sp_content:
                if sp_content.p:
                    if (len(sp_content.p.contents) > 0):
                        content = sp_content.p.contents[0]

            location_flag = False
            house_flag = False
            for loc in self.locations_:
                if title.find(loc) != -1 or content.find(loc) != -1:
                    location_flag = True
                    break

            if not location_flag:
                return False

            for h in self.house_:
                if title.find(h) != -1 or content.find(h) != -1:
                    house_flag = True
                    break
            if house_flag:
                print("spider topic satisfied: {0}".format(topic_url))
                print('title: {0}'.format(title))
                print('content: {0}\n'.format(content))
                return True

        return False
 

    def spider_group(self, group):
        results = []
        if not group:
            print("group(empty) invalid")
            return results
        start = 0
        time_step = 0.5
        while True:
            topic_list = []
            url = 'https://www.douban.com/group/{0}/discussion?start={1}'.format(group, start)
            r = self.ss_.get(url, headers = self.headers_)
            now_time = int(time.time())
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'lxml')
                trs = soup.find_all('tr')
                for item in trs:
                    if (len(item) < 4):
                        continue
                    tds = item.find_all('td')
                    if len(tds) != 4:
                        continue
                    if not tds[0].find('a'):
                        continue
                    topic_url   = tds[0].a['href']
                    title       = tds[0].a['title']
                    reply_time  = tds[3].contents[0]   # 03-08 18:05
                    reply_time  = '2020-{0}'.format(reply_time)

                    timeArray = time.strptime(reply_time, "%Y-%m-%d %H:%M")
                    timestamp = int(time.mktime(timeArray))

                    if (now_time - timestamp) > 7 * 24 * 60 * 60: # 7 days
                        break
                    topic = {
                            'url': topic_url,
                            'title': title,
                            'time': reply_time
                            }
                    topic_list.append(topic)
            if not topic_list:
                print("found topic error for url:{0}".format(url))
                time_step += 0.2
            else:
                print("found {0} topics for url:{1}".format(len(topic_list), url))
                time_step = 0.5

            for topic_item in topic_list:
                if not self.spider_topic(topic_item):
                    continue
                results.append(topic_item)

            time.sleep(time_step)
            if start > 10000:
                break
            start += 25
            
            if len(results) > 50:
                break

        return results





def run():
    #def __init__(self, cookies, groups, locations, house, date = 7,  filters = []):
    cookies     = sconfig.cookies
    groups      = sconfig.groups 
    locations   = sconfig.locations
    house       = sconfig.house 

    douban = DouBan(cookies, groups, locations, house)
    results = douban.spider_group(145219)
    print(json.dumps(results, indent = 4))


if __name__ == '__main__':
    run()
