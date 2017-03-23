#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Yan Chen (cheny.gary@gmail.com)


from bs4 import BeautifulSoup
from webopener import getHtml
import re
import zlib
from writeexcel import writeexcel



class fang(object):
    """房信息类"""

    def __init__(self):

        __slots__ = ('fname','xiaoqu', 'huxing', 'pingmi', 'jiage')

class Pagesoup(object):
    """解析网页内容的类"""

    def __init__(self, htmlcontent):

        self.htmlcontent = htmlcontent
        self.soupdata = BeautifulSoup(self.htmlcontent, 'html.parser')

    def yeshu(self):
    	div= self.soupdata.find_all(attrs={"class":"fanye"})
    	return int(re.sub('\D','',(div[0].span.contents[0])))



if __name__ == "__main__":
    # with open('creditpage.html') as html:
    # 	soup = Pagesoup(html)
    # 	print(soup.mcreditbad())
    total = []
    total.append(['小区','小区主页','户型','平米','价格','描述'])
    with open('arealist.txt', 'r') as list:
        try:
            line =list.readline()
            
            while line:
                # print(line)                              
                # time.sleep(random.uniform(15, 17))
                stype, sline, sstop = (line.split(","))
                url = 'http://esf.fang.com/'+stype+'-'+sline+'-'+sstop+'/h316'
                # print(url)
                html = getHtml(url)
                html = zlib.decompress(html ,16+zlib.MAX_WBITS)
                html = html.decode('gb2312','ignore')
                soup = Pagesoup(html)
                pagen = soup.yeshu()
                for j in range(0,pagen+1):
                	urli = 'http://esf.fang.com/'+stype+'-'+sline+'-'+sstop+'/h316-i3'+str(j)
                	html = getHtml(urli)
	                html = zlib.decompress(html ,16+zlib.MAX_WBITS)
	                html = html.decode('gb2312','ignore')
	                soup = Pagesoup(html)               
	                for i in soup.soupdata.find_all(attrs={"class": "info rel floatr"}):
	                	fangtitle = i.find_all(attrs = {"class": "title"})[0].a.contents[0]
	                	fangtype = i.find(attrs = {"class": "mt12"}).contents[0].strip()
	                	fangjiage = i.find(attrs = {"class":"price"}).contents[0]
	                	fangpingmi = i.find(attrs = {"class": "area alignR"}).p.contents[0]
	                	fangxiaoqu = i.find(attrs ={"class": "mt10"}).span.contents[0]
	                	xiaoquurl = i.find(attrs ={"class": "mt10"}).a.get("href")
	                	fanglist = [fangxiaoqu,xiaoquurl,fangtype,fangpingmi,fangjiage,fangtitle,xiaoquurl]
	                	total.append(fanglist)


                line =list.readline() 
        except IndexError as e:
            print(e)
            print('抓了%d个' %(len(total)-1))
    if len(total) > 1:
        writeexcel('房子列表.xlsx', total)
    else:
        print('什么都抓不到')
