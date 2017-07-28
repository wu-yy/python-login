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


# 构造 Request headers
agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
headers = {

    "Host": "www.douban.com",
    "Referer": "https://www.douban.com/",
    'User-Agent': agent,
}

#使用cookie登录信息
session=requests.session()
session.cookies=cookielib.LWPCookieJar(filename='cookies')

try:
    session.cookies.load(ignore_discard=True)
    print('成功加载cookie')
except:
    print("cookie 未能加载")

# 获取验证码
def get_captcha(url):
    #获取验证码
    print('获取验证码',url)
    captcha_url = url
    r = session.get(captcha_url, headers=headers)
    print('test')
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha

def isLogin():
    #登录个人主页，查看是否登录成功
    url='https://www.douban.com/people/151607908/'
    login_code=session.get(url,headers=headers,allow_redirects=False).status_code
    if login_code==200:
        return True
    else:
        return False


def login(acount,secret):
    douban="https://www.douban.com/"
    htmlcha=session.get(douban,headers=headers).text
    patterncha=r'id="captcha_image" src="(.*?)" alt="captcha"'
    httpcha=re.findall(patterncha,htmlcha)
    post_data = {
        "source": "index_nav",
        'form_email': acount,
        'form_password': secret
    }
    if len(httpcha)>0:
        print('验证码连接',httpcha)
        capcha=get_captcha(httpcha[0])
        post_data['captcha-solution']=capcha

    print (post_data)
    post_url='https://www.douban.com/accounts/login'
    login_page=session.post(post_url,data=post_data,headers=headers)
    login_code=login_page.status_code
    if login_code== 200:
        print('登录成功')
        #print(login_page.text)
    else:
        print('登录失败')

    #保存成绩
    session.cookies.save()
    if isLogin():
        print('登录成功2')

def get_movie_sort():
    time.sleep(1)
    movie_url='https://movie.douban.com/chart'
    html=session.get(movie_url,headers=headers)
    soup=BeautifulSoup(html.text,'html.parser')
    result=soup.find_all('a',{'class':'nbg'})
    print(result)
if __name__=='__main__':
    if isLogin():
        print('您已经登录')
    else:
        login('2384172887@qq.com','w1155435642')

    get_movie_sort()