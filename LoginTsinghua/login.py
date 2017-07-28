import requests
try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re
import time
import os.path
import json
from bs4 import BeautifulSoup
try:
    from PIL import Image
except:
    pass

import ssl
ssl._create_default_https_context=ssl._create_unverified_context

# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
headers = {

    "Host": "info.tsinghua.edu.cn",
    "Connection":"keep-alive",
    "Referer": "http://info.tsinghua.edu.cn/",
    "Origin":"http://info.tsinghua.edu.cn",
    "Upgrade-Insecure-Requests": "1",
    'User-Agent': agent,
    "Content-Type":"application/x-www-form-urlencoded",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.8"
}

#使用cookie登录信息
session=requests.session()
session.cookies=cookielib.LWPCookieJar(filename='cookies')

try:
    session.cookies.load(ignore_discard=True)
    print('成功加载cookie')
except:
    print("cookie 未能加载")


def isLogin():
    url='http://info.tsinghua.edu.cn/render.userLayoutRootNode.uP'
    login_code=session.get(url,headers=headers,allow_redirects=False).status_code
    if login_code==200:
        return True
    else:
        return False


def login(acount,secret):
    post_data={
        'userName':acount,
        'password':secret
    }
    print('cookies:',session.cookies)
    post_url='https://info.tsinghua.edu.cn:443/Login'
    login_page=session.post(post_url,data=post_data,headers=headers,verify=False)
    login_code=login_page.status_code
    if login_code== 200:
        print('登录成功')
    else:
        print('登录失败')

    #保存成绩
    session.cookies.save()
    get_grade()

def get_grade():
    url='http://info.tsinghua.edu.cn/render.userLayoutRootNode.uP'
    html=session.get(url,headers=headers).text
    soup=BeautifulSoup(html,'html.parser')
    result=soup.find_all('a',{'target':'_blank'})
    r1=''
    r2=''
    for i in result:
        if '全部成绩' in i:
            print (i)
            r1=i
            break
    if r1 !='':
        pattern=r'href="(.*?)"'
        r2=re.findall(pattern,r1.decode())
        print(r2)

    #保存成绩到文本文件
    with open('grade.txt','wb') as f:
        html2=session.get(r2[0],headers=headers).content
        f.write(html2)
        f.close()

    #print('成绩连接',result)

if __name__=='__main__':
    #if isLogin():
    #    print('您已经登录')
    #else:
    login('wu-yy13','wuyy17456')

    #get_grade()