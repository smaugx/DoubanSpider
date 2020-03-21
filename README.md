# DoubanSpider
a spider for douban groups of renting a house.
豆瓣租房小组爬虫。

# How to use?
config file is sconfig.py, put your own needs in this file.

## cookies
usually not need to modify, using default is good enough.

or you can change it to your own cookie after login-in .

## groups
change this value to some douban groups which you want to spider.

```
groups = ['145219', 'HZhome', '467221']
```

## locations
change this value to some locations of your house.

```
locations = ['支付宝', '网易']
```

## house
change this value to some house type.

```
house = ['一室']
```

# Something Else
if you want to use markdown file, you can use command:

```
python convert_to_markdown.py
```

but first, make sure **doubanzufang.spider.topics.satisfied** in current dir.
