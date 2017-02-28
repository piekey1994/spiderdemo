from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import sqlite3



conn = sqlite3.connect('test.db')
cursor = conn.cursor()
p=0

htmls=['http://www.meishij.net/yaoshanshiliao/jibingtiaoli/',
        'http://www.meishij.net/yaoshanshiliao/gongnengxing/',
        'http://www.meishij.net/yaoshanshiliao/zangfu/']

for html in htmls:
    urlhtml=urlopen(html)
    bsObj = BeautifulSoup(urlhtml,'lxml')
    dds=bsObj.find("dl",{"class":"listnav_dl_style1 w990 clearfix"}).find_all("dd")
    for dd in dds:
        tlhref=dd.a.attrs['href']
        label=dd.a.get_text()
        tlhtml=urlopen(tlhref)
        tlbsObj=BeautifulSoup(tlhtml,'lxml')
        print(tlhref)
        flag=0
        try:
            nowlink=tlbsObj.find("div",{"class":"listtyle1_page_w"}).a.attrs["href"][:-1]
            if nowlink.find("www.meishij.net")==-1:
                nowlink="http://www.meishij.net"+nowlink
            number=int(re.findall("\d+",tlbsObj.find("span",{"class":"gopage"}).get_text())[0])
        except:
            flag=1
            number=1
        for i in range(1,number+1):
            if flag==0:
                h=urlopen(nowlink+str(i))
            else:
                h=urlopen(tlhref)
            hbsobj=BeautifulSoup(h,"lxml")
            for sibling in hbsobj.find_all("div",{"class":"listtyle1"}): 
                try:
                    aobj=sibling.a
                    name=aobj.attrs['title']
                    href=aobj.attrs['href']
                    uid=href[href.rfind('/')+1:href.find('.html')]
                    img=aobj.img.attrs['src']
                    other=aobj.div.div
                    hot=int(re.findall('\d+',other.find("div",{"class":"c1"}).span.get_text())[1])
                    try:
                        li1=other.find("div",{"class":"c2"}).ul.find("li",{"class":"li1"}).get_text()
                        steps=int(re.findall('\d+',li1)[0])
                        usetime=li1[li1.find('/')+2:]
                    except:
                        steps=-1
                        usetime="未知"
                    try:
                        li2=other.find("div",{"class":"c2"}).ul.find("li",{"class":"li2"}).get_text()
                        technology=li2[:li2.find('/')-1]
                        taste=li2[li2.find('/')+2:]
                    except:
                        technology="未知"
                        taste="未知"
                    try:
                        cursor.executemany("INSERT INTO food (id,name,href,img,technology,steps,taste,usetime,hot) \
                        VALUES (?,?,?,?,?,?,?,?,?)",[(uid,name,href,img,technology,steps,taste,usetime,hot)])
                    except:
                        pass
                    cursor.executemany("insert into label (fid,label) values (?,?)",[(uid,label)])
                    conn.commit()
                    p=p+1
                    print("finish:"+str(p)+" ->"+name)
                except:
                    pass
cursor.close()
conn.close()  
print("正常退出")       