import pymongo
import imageio
import jieba
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
# 数据库连接
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["shuoshuo"]
mycol = mydb["friends"]
# 词云模版图片
mask = imageio.imread(r"img\timg-7.jpeg")

# 读文件生成数据或者读数据库
# 1.读文件版本
# f = open("b.txt", "r")
# data = f.read()
# f.close()
# print(type(data))

# 2.读数据库版本
res = mycol.find({"name": "XXX"})

data = ""
for dict in res:
    data+=dict['text']

ls = jieba.lcut(data)
txt = " ".join(ls)
stopwords = set(STOPWORDS)
stopwords.add('url')
stopwords.add('http')
stopwords.add('cn')

wc = WordCloud(
    background_color='white',
    mask=mask,
    font_path = r'C:\Windows\Fonts\STZHONGS.TTF',
	# 改成中文字体路径
    max_words = 2000,
    max_font_size=40,
    min_font_size=10,
    stopwords=stopwords,
    random_state=1,
    scale=1
    )
wc.generate(txt)

image_colors = ImageColorGenerator(mask)
plt.imshow(wc.recolor(color_func=image_colors))

wc.to_file("res\XXX.png")