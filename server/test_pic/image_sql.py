# -*- coding=utf-8 -*-
import pymysql
import sys
from io import BytesIO
from PIL import Image
#读取图片文件
#blob最大只能存65K的文件
 
#fp = open("test.jpg",'rb',encoding='utf-8')
fp = open("/home/tarena/test/middle_work/xiaohan_new2019/test_pic/test.jpg",'rb')
img = fp.read()
fp.close()
# 创建连接
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='123456',
                       db='chat',
                       charset='utf8',
                       use_unicode=True,)
# 创建游标
cursor = conn.cursor()
 
#注意使用Binary()函数来指定存储的是二进制
#cursor.execute("INSERT INTO demo_pic_repo SET touxiang_data= %s" % pymysql.Binary(img))
find_binary=pymysql.Binary(img)
# find_binary = '1'
# sql="INSERT INTO demo_pic_repo (touxiang_data_blob) VALUES  (%s)"
sql = "insert into user_logo(logo_pic) values(%s)"

# sql = "update user_logo set logo_pic = %s"
# sql = "select logo_pic from user_logo where id =2"
cursor.execute(sql,find_binary)
# 提交，不然无法保存新建或者修改的数据
conn.commit()
# result = cursor.fetchone()
# data = result[0]
# buf = BytesIO(data)
# img_obj =Image.open(buf)
# img_obj.show()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()
