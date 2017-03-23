#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : Yan Chen (cheny.gary@gmail.com)

from bs4 import BeautifulSoup
from webopener import getHtml
import re
import zlib

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
   
    with open('arealist.txt', 'r') as list:
    	with open('zufanglist.txt', "w+") as output:
	        try:
	            line =list.readline().strip()
	            
	            while line:
	                # print(line)                              
	                # time.sleep(random.uniform(15, 17))
	                stype, sline, sstop = (line.split(","))
	                url = 'http://zu.fang.com/'+stype+'-'+sline+'-'+sstop+'/h316'
	                # url ='http://zu.fang.com/house1-j066-k05488/h316/'
	                # print(url)
	                html = getHtml(url)
	                html = zlib.decompress(html ,16+zlib.MAX_WBITS)
	                html = html.decode('gb2312','ignore')
	                soup = Pagesoup(html)
	                pagen = soup.yeshu()
	                # print(pagen)
	                
	                for j in range(1,pagen+1):
	                	urli = 'http://zu.fang.com/'+stype+'-'+sline+'-'+sstop+'/h316-i3'+str(j)
	                	# urli = 'http://zu.fang.com/house1-j066-k05488/'+'h316-i3'+str(j)
	                	print(urli)
	                	html = getHtml(urli)
		                html = zlib.decompress(html ,16+zlib.MAX_WBITS)
		                html = html.decode('gb2312','ignore')
		                soup = Pagesoup(html)               
		                for i in soup.soupdata.find_all(attrs={"class": "info rel"}):
		                	fangtitle = i.find_all(attrs = {"class": "title"})[0].a.contents[0]
		                	fangtype = i.find(attrs = {"class": "font16 mt20 bold"}).contents[2].strip()
		                	fangjiage = i.find(attrs = {"class":"price"}).contents[0]
		                	fangpingmi = i.find(attrs = {"class": "font16 mt20 bold"}).contents[4].strip()
		                	fangxiaoqu = i.find_all(attrs = {"target": "_blank"})[3].span.contents[0]

		                	# fangtitle = i.find_all(attrs = {"class": "title"})[0].a.contents[0]
		                	# fangtype = i.find(attrs = {"class": "mt12"}).contents[0].strip()
		                	# fangjiage = i.find(attrs = {"class":"price"}).contents[0]
		                	# fangpingmi = i.find(attrs = {"class": "area alignR"}).p.contents[0]
		                	# fangxiaoqu = i.find(attrs ={"class": "mt10"}).span.contents[0]
		                	# xiaoquurl = i.find(attrs ={"class": "mt10"}).a.get("href")
		                	fanglist = [fangxiaoqu,';',fangtype,';',fangpingmi,';',fangjiage,';',fangtitle,'\n']
		                	output.writelines(fanglist)
		                	fanglist =[0]
	        		
			                	# total.append(fanglist)


	                line =list.readline().strip()
	        except IndexError as e:
	            print(e)
	            print('抓了%d个' %(len(total)-1))

    # if len(total) > 1:
    #     writeexcel('房子列表.xlsx', total)
    # else:
    #     print('什么都抓不到')
