#!/usr/bin/env python
#-*- coding:utf8 -*-


import os
import json


topics_satisfied_file = './doubanzufang.spider.topics.satisfied'

topics_satisfied_file_md = topics_satisfied_file + '.md'

F = open(topics_satisfied_file_md, 'a')

with open(topics_satisfied_file, 'r') as fin:
    for line in fin:
        if line.endswith('\n'):
            line = line[:-1]
        topic_item = json.loads(line)
        url = topic_item.get('url')
        title = topic_item.get('title')
        md_line = '[{0}]({1})\n\n'.format(title, url)
        F.write(md_line)
    F.close()
