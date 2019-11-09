### 环境准备：

- python3.7

- 对应版本的python库：

  selenium库

  chrome浏览器/firefox浏览器及对应版本的driver

  requests库

  re库

  codecs库

  json库

  wordcloud库

  jieba库

  imageio库

- 本地mongodb数据库

  对应版本的pymongo

- 自己登录状态的QQ

### 运行说明：

1. getfriends.py——

   把main()部分替换为自己qq并且务必保证自己qq是登录状态

   运行后可以得到两个txt：

   cookie_dict.txt自己的cookie信息，可以不用文件输出，为了检查替换变量方便。

   friends.txt保存朋友的qq号、备注、头像、亲密度信息。

2. getshuoshuo.py——

   把main函数的login部分换成自己qq并保证登录状态。

   确保mongodb数据库开启。

   控制台输出当前遍历的好友说说信息，包括好友信息，总说说页数。

3. ciyun.py——

   确保mongodb数据库开启。

   将数据库查找的姓名换成你想生成的好友备注（friends.txt中）。

   替换想用的词云图片模版、以及结果图片地址。

   替换中文字体路径。

### 运行效果：(见res文件夹)

![](https://github.com/zhxjz/QzoneShuoshuoCrawler/blob/master/res/lmc.png)

![](https://github.com/zhxjz/QzoneShuoshuoCrawler/blob/master/res/self.png)

![](https://github.com/zhxjz/QzoneShuoshuoCrawler/blob/master/res/wrh.png)

#### 已上传源码至个人github（https://github.com/zhxjz/QzoneShuoshuoCrawler/

#### 有问题可发邮件至shuyepan@qq.com交流
