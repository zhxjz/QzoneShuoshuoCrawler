#导入selenium2中的webdriver库
from selenium import webdriver
# 为了点击头像图标引入
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from pyquery import PyQuery as pq
# 正则库
import re
# mongodb连接
import pymongo
# json引入好友列表
import json
import codecs

# 浏览器配置
options = webdriver.ChromeOptions()
# 浏览器隐藏
options.add_argument('--headless')
options.add_argument('--disable-gpu')
#设置无图模式
prefs = {
    'profile.default_content_setting_values': {
        'images': 2
    }
}
options.add_experimental_option('prefs', prefs)
# 实例化浏览器
driver = webdriver.Chrome(options=options)
# # 设置浏览器窗口的位置和大小
# driver.set_window_position(20, 40)
# driver.set_window_size(1100,700)

# 数据库连接
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["shuoshuo"]
mycol = mydb["friends"]
# 正则
regex = re.compile(r'[0-9]+')

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
        except Exception:
            raise
    except Exception:
        raise

# 得到说说页数
def get_pagetot(qq):
    try:
        url = f'https://user.qzone.qq.com/{qq}/311'
        driver.get(url)
        # 来到说说内容页
        time.sleep(10)
        driver.switch_to.frame('app_canvas_frame')
        # 拿到页尾参数
        try:
            page_last = WebDriverWait(driver,30,0.5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '#pager_last_0'))).text
            return page_last
        except Exception:
            return 0
    except Exception:
        return 0

# 有yield的函数在实例化之后才执行
def get_shuoshuo(now_id,qq,name):
    try:
        #
        doc = pq(driver.page_source)
        items = doc('#msgList > li.feed').items()
        for item in items:
            # 转赞评数量提取
            ping = '0'
            zhuan = '0'
            # zan = '0'
            # 评论数
            str = item.find('div.box.bgr3 > div.ft > div.op > .comment_btn').text()
            match = regex.search(str)
            if match:
                ping = match.group(0)
            # 转发数
            match = regex.search(item.find('div.box.bgr3 > div.ft > div.op > .forward_btn').text())
            if match:
                zhuan = match.group(0)
            # 点赞数
            # str = item.find('div.box.bgr3 > div.box_extra.bor3 > div.feed_like ').text()
            # print('点赞',str)
            # match = regex.search(str)
            # if match:
            #     zan = match.group(0)

            yield {
                'name':name,
                'qq':qq,
                'time': item.find('div.box.bgr3 > div.ft > div.info > span.c_tx3 > a.c_tx').text(),
                'text': item.find('.content').text(),
                'ping': ping,
                'zhuan':zhuan,
                # 'zan':zan
            }
            # 跳转下一页，采用输入方式，点击可能跳不动。
        try:
            text = WebDriverWait(driver,10,0.5).until(
                EC.presence_of_element_located(
                    (By.ID, f'pager_go_{now_id - 1}')))  # 获取跳转页的输入框
            text.send_keys(now_id + 1)  # 输入下一页
            text.send_keys(Keys.ENTER)  # 进行确定
            driver.implicitly_wait(10)  # 隐式等待5秒
        except Exception:
            raise
    except Exception:
        raise

# 保存一页的数据至mongodb
def save_shuoshuo(page_id,qq,name):
        res = get_shuoshuo(page_id,qq,name)
        lis = list(res)
        if len(lis)>0:
            mycol.insert_many(lis)
        return len(lis)

def oneqq(qq,name):
    page_tot = int(get_pagetot(qq))
    print(page_tot)
    if page_tot == 0 :
        with open('suliao_friends.txt', 'a') as f:
            f.write(str(qq)+'-'+str(name)+'\n')
    else:
        for i in range(1, min(50,page_tot) ):
            res = save_shuoshuo(i,qq,name)
            if res == 0:
                break

def see_friends():
    with open('friends.txt', 'r', encoding='utf-8') as f:
        friend_list = json.load(f)
    cnt = 0
    for friend in friend_list:
        cnt = cnt + 1
        if cnt>100 :
            break
        print('begin-----')
        oneqq(friend['uin'] , friend['name'])
        print(cnt,friend['name'],friend['uin'],' finished')
    driver.close()

def main():
    login('454515228')
    see_friends()
# oneqq('','')
main()