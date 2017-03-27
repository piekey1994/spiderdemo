from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3
import re

conn = sqlite3.connect('test.db')
cursor = conn.cursor()

for i in page:
    html = urlopen("http://www.meishij.net/shiliao.php?st=3&cid=250&sortby=update&page="+str(i)) 
    bsObj = BeautifulSoup(html,'lxml')
    for sibling in bsObj.find_all("div",{"class":"listtyle1"}): 
        aobj=sibling.a
        name=aobj.attrs['title']
        href=aobj.attrs['href']
        print(href)
        img=aobj.img.attrs['src']
        while True:
            try:
                newhtml=urlopen(href)
                newbs=BeautifulSoup(newhtml,'lxml')
                lis=newbs.find("ul",{"class":"clearfix"}).find_all("li")
                break
            except:
                webbrowser.open(href)
                input()
        technology=lis[0].a.get_text()
        try:
            level=int(re.findall("\d",lis[1].div.find_all("span")[1].attrs["class"][1])[0])
        except:
            level=-1
        try:
            weight=int(re.findall("\d",lis[2].div.a.get_text())[0])
        except:
            weight=-1
        try:
            taste=lis[3].a.get_text()
        except:
            taste="未知"
        try:
            pretime=lis[4].div.a.get_text()
        except:
            pretime="未知"
        try:
            usetime=lis[5].div.a.get_text()
        except:
            usetime="未知"
        cursor.executemany("INSERT INTO food (name,href,img,technology,level,weight,taste,pretime,usetime) \
            VALUES (?,?,?,?,?,?,?,?,?)",[(name,href,img,technology,level,weight,taste,pretime,usetime)])
        conn.commit()
        p=p+1
        print("finish:"+str(p)+" ->"+name)
        #time.sleep(3)
cursor.close()
conn.close()