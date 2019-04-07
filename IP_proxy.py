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
   # return proxy

def Check_proxy(proxy):
    url="http://www.baidu.com"
    code1=requests.get(url,proxies=proxy).status_code
    time.sleep(3)
    code2=requests.get(url,proxies=proxy).status_code
    if code1 != 200 and code2 != 200:
        print('ok')
        Get_proxy_list()
    else:
        print(proxy)
        return proxy
if __name__ == '__main__':
	Get_proxy()
