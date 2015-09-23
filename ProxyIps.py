#!usr/bin/python
#coding:utf-8

import requests
from bs4 import BeautifulSoup
from lxml import etree
from ProxyDataBase import ProxyDataBase
'''
1、获取网页目录链接
2、抓取ip信息
3、存储到数据库
'''


BASE_URL = "http://www.xicidaili.com"
HEADER = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0",
              "Host":"www.xicidaili.com",
              "Connection":"keep-alive",
              "Accept-Language":"en-US,en;q=0.5",
              "Accept-Encoding":"gzip, deflate",
              "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
              }
PROXIES = {
           "HTTP":"218.189.26.20:8080",
           "HTTP":"180.166.112.47:8888",
           "HTTP":"182.92.156.129:80",
           }
topLinks = []
ips = {}
db = ProxyDataBase()

#请求网页
def request():
    request = requests.get(BASE_URL,proxies=PROXIES,headers=HEADER)
    #print request.content  
    doTopLink(request.content)

#获取分栏目录链接
def doTopLink(content):
    #html = BeautifulSoup(content)
    html = etree.HTML(content)
    lis = html.xpath("//div[@id='header']/ul/li")
    for li in lis[0]:
        if li.xpath("//a[@class='false']"):
            for item in li.xpath("//a[@class='false']"):
            #print li.xpath("//a[@class='false']")[3].text
                topLinks.append(item.get("href"))
    for topLink in topLinks:
        print BASE_URL+topLink
        doSingleTopLinkBasicInfo(BASE_URL+topLink,topLink)
     
     
#获取单个栏目下页面基本信息
def doSingleTopLinkBasicInfo(link,type):
    request = requests.get(link,headers=HEADER)
    #print request.content
    html = etree.HTML(request.content)
    pageTag = html.xpath("//div[@class='pagination']/a")[-2]
    maxPage = pageTag.text
    page = 1
    while page <= int(maxPage) :
        print "=======================page=",page,"===============maxpage=====",maxPage
        doHtmlIpInfo(link+"/"+str(page),type)
        page += 1
    
#获取页面所有ip信息
#国家
#IP地址
#端口
#是否匿名
#类型
#验证时间
def doHtmlIpInfo(link,iptype):
    request = requests.get(link,headers=HEADER)
    html = etree.HTML(request.content)
    ipInfos = html.xpath("//table[@id='ip_list']/tr[@class='odd']|/tr[@class='']")
    for ipInfo in ipInfos:
        ip = ipInfo.xpath(".//td")[2].text
        port = ipInfo.xpath(".//td")[3].text
        attr = ipInfo.xpath(".//td")[5].text
        type = ipInfo.xpath(".//td")[6].text
        date = ipInfo.xpath(".//td")[9].text
        db.save(iptype, ip, port, attr, type, date)
        #print iptype,ipInfo.xpath(".//td")[2].text,ipInfo.xpath(".//td")[3].text,ipInfo.xpath(".//td")[5].text,ipInfo.xpath(".//td")[6].text,ipInfo.xpath(".//td")[9].text

    
    
if __name__=="__main__":
    request()
    db.close()

'''
    <tr class="odd">
      <td></td>
      <td><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>
      <td>60.212.37.27</td>
      <td>8088</td>
      <td>
        <a href="/2015-09-08/shandong">山东烟台</a>
      </td>
      <td>高匿</td>
      <td>HTTP</td>
      <td>
        <div title="1.113秒" class="bar">
          <div class="bar_inner fast" style="width:89%">
            
          </div>
        </div>
      </td>
      <td>
        <div title="0.377秒" class="bar">
          <div class="bar_inner fast" style="width:92%">
            
          </div>
        </div>
      </td>
      <td>15-09-08 22:28</td>
    </tr>
  
    <tr class="">
      <td></td>
      <td><img src="http://fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>
      <td>120.236.148.113</td>
      <td>3128</td>
      <td>
        移动
      </td>
      <td>高匿</td>
      <td>HTTPS</td>
      <td>
        <div title="5.991秒" class="bar">
          <div class="bar_inner medium" style="width:40%">
            
          </div>
        </div>
      </td>
      <td>
        <div title="0.316秒" class="bar">
          <div class="bar_inner fast" style="width:94%">
            
          </div>
        </div>
      </td>
      <td>15-09-08 19:39</td>
    </tr>
    '''

