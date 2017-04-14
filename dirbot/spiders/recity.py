# coding=utf-8
import MySQLdb
import re

def o():
    pattern7 = re.compile(r"-(.*)\xc2\xa0")
    print pattern7.findall("位置:市中-魏家庄 经二纬一")
def cityname():
    conn = MySQLdb.connect(db='zhaogefang', host='120.27.30.221', user='root', passwd='xhgm19111010',
                                   charset="utf8")
    cursor=conn.cursor()
    sql = "SELECT jx FROM web_city"

    cursor.execute(sql)

    conn.close()
    content=cursor.fetchall()

    return content
o()