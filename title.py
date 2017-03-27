from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3
import re

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

htmls=['http://www.meishij.net/yaoshanshiliao/renqunshanshi/',
    'http://www.meishij.net/yaoshanshiliao/jibingtiaoli/',
        'http://www.meishij.net/yaoshanshiliao/gongnengxing/',
        'http://www.meishij.net/yaoshanshiliao/zangfu/']
for html in htmls:
    htm = urlopen(html) 
    bsObj = BeautifulSoup(htm,'lxml')
    title=bsObj.find("dl",{"class":"listnav_dl_style1 w990 clearfix"}).dt.get_text()
    for dd in bsObj.find("dl",{"class":"listnav_dl_style1 w990 clearfix"}).find_all("dd"):
        label=dd.a.get_text()
        cursor.executemany("insert into title (type,label) values (?,?)",[(title,label)])
        conn.commit()
    print("finish"+html)
cursor.close()
conn.close() 