#导入selenium2中的webdriver库
from selenium import webdriver
# 为了点击头像图标引入
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
# 正则库
import re
# json
import codecs
import json
# requests库
import requests
from urllib import parse

# 实例化浏览器
driver = webdriver.Chrome()

# here qq: your qq number, make sure that your qq has been logged
def login(qq):
    try:
        url = f'https://i.qq.com/'
        driver.get(url)
        try:
            # switch to the frame
            driver.switch_to.frame('login_frame')
            # click your avatar
            login = WebDriverWait(driver,20,0.5).until(
            EC.element_to_be_clickable(
                    (By.ID, f'img_out_{qq}')))
            login.click()
            time.sleep(5)
            # save your cookie
            cookies = driver.get_cookies()
            print(cookies)
            cookie_dic = {}
            for cookie in cookies:
                if 'name' in cookie and 'value' in cookie:
                    cookie_dic[cookie['name']] = cookie['value']
            with open('cookie_dict.txt', 'w',encoding='utf-8') as f:
                json.dump(cookie_dic, f,ensure_ascii=False)
        except Exception:
            raise
    except Exception:
        raise


class Qzone:
    def doit(self,qqnum):
        with open('cookie_dict.txt', 'r') as f:
            coo = json.load(f)
        header = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36',
                'accept-language':'zh-CN,zh;q=0.9'
            }
        friend_list = self.get_friend(header,coo,qqnum)
        with codecs.open('friends.txt', 'w', encoding='utf-8') as f:
            json.dump(friend_list, f, ensure_ascii=False)

    # hash参数
    def get_gtk(self, cookie=None):
        p_skey = cookie['p_skey']
        h = 5381
        for i in p_skey:
            h += (h << 5) + ord(i)
        g_tk = h & 2147483647
        return g_tk

    # 找出好友qq和备注列表
    def get_friend(self,header,cookie,qqnum):
        url_friend = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?'
        g_tk = self.get_gtk(cookie)
        data = {
            'uin': qqnum,
            'do': 1,
            'g_tk': g_tk
        }
        data_encode =parse.urlencode(data)
        url_friend += data_encode
        res = requests.get(url_friend, headers=header, cookies=cookie)
        # 正则匹配出_Callback()里面的内容
        friend_json = re.findall('\((.*)\)', res.text, re.S)[0]
        # 变成字典类型
        friend_dict = json.loads(friend_json)
        friend_result_list = []
        # 循环将好友的姓名qq号存入list中
        for friend in friend_dict['data']['items_list']:
            friend_result_list.append({
                'name':friend['name'],
                'uin':friend['uin'],
                'img':friend['img'],
                'score':friend['score']
            })
        return friend_result_list

def main():
	# 替换为自己的qq号
    login('454515228')
    qzone=Qzone()
	# 替换为自己的qq号
    qzone.doit('454515228')

main()