#coding:utf-8

import os
import sys
import requests
from bs4 import BeautifulSoup
import re
import random
import time

def Get_proxy(url="http://haoip.cc/tiqu.htm"):
    web_data = requests.get(url)
    soup = BeautifulSoup(web_data.text,'lxml')
    ip_div_list = soup.select('body > div.container > div.row > div.col-xs-12')
    p=re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,4}')
    ip_list=p.findall(str(ip_div_list[0]))
    ip=random.choice(ip_list).strip()
    proxy={'http':ip}
    Check_proxy(proxy)

def Check_proxy(proxy):
    url="http://www.baidu.com"
    code1=requests.get(url,proxies=proxy).status_code
    time.sleep(3)
    code2=requests.get(url,proxies=proxy).status_code
    if code1 != 200 and code2 != 200:
        print('ok')
        Get_proxy_list()
    else:
        print('成功获取代理IP',proxy)
        return proxy



def Get_web_data(url):
    #获取某个网页
    proxy=Get_proxy()   
    #可以加上代理功能
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'}
    web_data=requests.get(url,headers,proxies=proxy)
   # web_data=requests.get(url,headers)
    return web_data

def Get_page_list():
    #获取专题页面链接列表
  #      print('Get_page_list函数开始执行')
        num=1
        page_list=[]
        while num < 20 :
            url="http://www.mzitu.com/page/"+str(num)
            web_data=Get_web_data(url)
   #         print(web_data.status_code)
            if web_data.status_code==200:
                page_list.append(url)
            num+=1
        if len(page_list)>0:
            print('成功获取专题页面列表')
    #        print(page_list)
        else:
            print('未能获取到专题页面列表，请检查网络')
            return sys.exit(1)
        return page_list

def Get_page_url_dict(url):
    #将单个专题页面的所有帖子链接提取出来
    #url=page_list[0]
    url_dict={}
    web_data=Get_web_data(url)
    soup=BeautifulSoup(web_data.text,'lxml')
    channel=soup.select('body > div.main > div.main-content > div.postlist > ul > li > a')
    for src in channel:
        url_dict[src.get('href')]=src.select('img')[0].get('alt')
   # print(url_dict)
    return url_dict

def Get_picture_url_dict(pageurl,pagename):
    #
    #传入某个帖子的链接，提取出所有图片链接
    '''for k,v in kwargs:
        pageurl=k
        pagename=v'''
   # print('开始执行Get_picture_url_dict函数')
    num=1
    url_list=[]

    while 1:
        pageurl_new=pageurl+'/'+str(num)
        W=Get_web_data(pageurl_new)
        if W.status_code == 200 :
            soup=BeautifulSoup(W.text,'lxml')
            channel=soup.select('body > div.main > div.content > div.main-image > p > a > img')
            if channel[0].get('src') not in url_list:
                url_list.append(channel[0].get('src'))
                num+=1
            else:
                #检查到元素重复，结束提取
                break
#            print (url_list)
        elif W.status_code==403 or 404:
            break
    url_dict={}
    url_dict[pagename]=url_list
    return url_dict
def Download_MM(**kwargs):
    #传入帖子名和资源列表为参数的字典，下载图片
    for k,v in kwargs.items():
        pic_name=k
        pic_list=v
    Download_path=''
    Download_path=os.path.split(os.path.realpath(sys.argv[0]))[0]+'//'+'Download'
    print('输出Download目录：',Download_path)
    if os.path.exists(Download_path) and os.path.isdir(Download_path):
        pass
    else:
        os.mkdir(Download_path)
    os.chdir(Download_path)
    os.mkdir(pic_name)
    os.chdir('./'+pic_name)
    for url in pic_list:
        filename=url.split('/')[-1]
        img=Get_web_data(url).content
        #多媒体文件用content方法
        with open(filename,'wb') as f:
            f.write(img)
    os.chdir(os.pardir)
    os.chdir(os.pardir)
    #返回上上层目录
def main1():
    print('开始执行主函数')
    page_list=Get_page_list()
    num=1
    choose=1
    for i in page_list:
        page_dict=Get_page_url_dict(i)
        for k,v in page_dict.items():
            pic_dict=Get_picture_url_dict(k,v)
            print('即将开始下载第{}套妹子图片:{}'.format(num,v))
            Download_MM(**pic_dict)
            num+=1
            if choose==1:
                x=input('下载完成，是否继续下载？(输入q退出，输入a下载全部，输入其他任意键则继续下一套)').strip()
                print(x)
                if x=='q' or x=='Q':
                        print('你居然选择拒绝妹子？好吧，结束本次任务')
                        sys.exit(0)
                elif x=='a' or x=='A':
                        print('少年请注意身体，不过老夫很欣赏你！')
                        choose=0
                        continue
                else:
                        print('继续就对了，不要停下')
                        choose=2
                        continue
            elif choose==0:
                pass
            elif choose==2:
                choose=1
            else:
                print('程序异常')

if __name__ == '__main__':
    main1()

