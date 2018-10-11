from pyecharts import Kline , Line , Overlap
import pymysql
import datetime
from Message import Messsge
import math


# -*- coding: utf-8 -*



class Chart:


    def __init__(self):
        self.time = datetime.date.today()
        self.text = Messsge().GetData()
        # self.newtext = '最新消息  : 开盘价：' + str(self.text[1]) + ' ; 最高价：' + str(self.text[2]) + ' ; 最底价：' \
        #        + str(self.text[3]) + ' ; 收盘价：' + str(self.text[4]) + ' ; 平均价：' + str(self.text[9]) + ' ; 当前分位数：' + str(self.text[16])

        # print(self.newtext
    def Kline(self,datestart, dateend):
        db = pymysql.connect('localhost', 'root', 'lsgogroup14', 'py_mysql')
        cursor = db.cursor()

        sql = "SELECT Open_price ,Close_price ,Floor_price ,Top_price FROM stock WHERE Date BETWEEN DATE_SUB('" +datestart + "' ,INTERVAL 30 DAY) AND '" + dateend +"' ORDER BY DATE ASC;"
        sql1 = "SELECT Date FROM stock WHERE Date BETWEEN DATE_SUB('" +datestart + "' ,INTERVAL 30 DAY) AND '" + dateend +"' ORDER BY DATE ASC;"
        cursor.execute(sql)
        list = cursor.fetchall()
        cursor.execute(sql1)
        date = cursor.fetchall()

        # print (str(date[-1][0]))
        sql_40 = "SELECT Fractile_40 FROM stock WHERE Date ='" + str(date[-1][0]) + "';"
        cursor.execute(sql_40)
        a = cursor.fetchone()

        list2 = [a[0] for i in range(len(date))]
        kline = Kline("沪深300-日K线(日期："+str(self.text[10:21])+')')
        # kline.use_theme('dark')
        kline.add("日K", date, list, )#is_datazoom_show=True)

        temp = []
        for i in date:
            temp.append(i[0])

        line = Line()
        line.add("40分位数", temp, list2, )  # is_datazoom_show=True)
        overlap = Overlap()
        overlap.use_theme("dark")
        overlap.add(kline)
        overlap.add(line)
        overlap.render(path='/home/lsgo14/图片/img/KLine.png')
        # kline.render(path='/home/lsgo25/图片/img/KLine.png')


    def FraLine(self):
        db = pymysql.connect('localhost', 'root', 'lsgogroup14', 'py_mysql')
        cursor = db.cursor()
        sql = "SELECT Fractile_Now FROM stock WHERE Date BETWEEN  DATE_SUB('" +str(self.time) + "' ,INTERVAL 2 YEAR)  AND '" + str(self.time) + "' ORDER BY DATE ASC;"
        sql1 = "SELECT Date FROM stock WHERE Date BETWEEN  DATE_SUB('" +str(self.time) + "' ,INTERVAL 2 YEAR)  AND '" + str(self.time) + "' ORDER BY DATE ASC;"
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.execute(sql1)
        date = cursor.fetchall()

        temp = []
        for i in date:
            temp.append(i[0])
        line = Line("沪深300分位数曲线(日期："+str(self.text[10:21])+')')
        line.use_theme("dark")
        line.add("一周期(2年)", temp,data,)
        line.render(path='/home/lsgo14/图片/img/FraLine.png')

    def NKline(self,datestart, dateend):
        db = pymysql.connect('localhost', 'root', 'lsgogroup14', 'py_mysql')
        cursor = db.cursor()

        sql = "SELECT Open_price ,Close_price ,Floor_price ,Top_price FROM stock WHERE Date BETWEEN "\
              + "DATE_SUB('" +str(datestart) + "' ,INTERVAL 90 DAY)  AND '" +  dateend +"' ORDER BY DATE ASC;"
        sql1 = "SELECT Date FROM stock WHERE Date BETWEEN "\
               + "DATE_SUB('" +str(datestart) + "' ,INTERVAL 90 DAY) AND '" + dateend +"' ORDER BY DATE ASC;"
        cursor.execute(sql)
        list = cursor.fetchall()
        cursor.execute(sql1)
        date = cursor.fetchall()
        kline = Kline("沪深300-日K线("+str(self.text[10:21])+')')
        kline.use_theme('dark')
        kline.add("近三个月日K线", date, list, )#is_datazoom_show=True)
        kline.render(path='/home/lsgo14/图片/img/NKLine.png')

    def Trade(self):
        db = pymysql.connect('localhost', 'root', 'lsgogroup14', 'py_mysql')
        cursor = db.cursor()
        sql_75 = "SELECT Fractile_75 FROM stock WHERE Date BETWEEN  DATE_SUB('" +str(self.time) + "' ,INTERVAL 2 YEAR)  AND '" + str(self.time) + "' ORDER BY DATE ASC;"
        sql_40 = "SELECT Fractile_40 FROM stock WHERE Date BETWEEN  DATE_SUB('" +str(self.time) + "' ,INTERVAL 2 YEAR)  AND '" + str(self.time) + "' ORDER BY DATE ASC;"
        sql_average = "SELECT Average_one FROM stock WHERE Date BETWEEN  DATE_SUB('" +str(self.time) + "' ,INTERVAL 2 YEAR)  AND '" + str(self.time) + "' ORDER BY DATE ASC;"

        sql1 = "SELECT Date FROM stock WHERE Date BETWEEN  DATE_SUB('" +str(self.time) + "' ,INTERVAL 2 YEAR)  AND '" + str(self.time) + "' ORDER BY DATE ASC;"
        cursor.execute(sql_75)
        data_75 = cursor.fetchall()
        cursor.execute(sql_40)
        data_40 = cursor.fetchall()
        cursor.execute(sql_average)
        data_average = cursor.fetchall()
        top = math.ceil(max(data_average)[0]/100+3)*100
        floor = math.floor(min(data_average)[0]/100-3)*100
        cursor.execute(sql1)
        date = cursor.fetchall()

        temp = []
        for i in date:
            temp.append(i[0])
        # line = Line("沪深300分位线走势")
        # line.use_theme("dark")
        # line.add("1周期（2年）", temp,data,)

        line1 = Line("沪深300历史交易曲线-日期"+str(self.text[10:21]), self.text ,title_text_size=12 ,subtitle_text_size=10)
        line1.use_theme("dark")
        line1.add("平均价", temp, data_average,yaxis_min=floor, yaxis_max=top)
        line1.add("分位数40", temp, data_40 ,yaxis_min=floor, yaxis_max=top)
        line1.add("分位数75", temp, data_75,yaxis_min=floor, yaxis_max=top)

        line1.render(path='/home/lsgo14/图片/img/TraLine.png')