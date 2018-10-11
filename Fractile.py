import pymysql
import numpy
import datetime as dt


# -*- coding: utf-8 -*


class FraOperation():


   def __init__(self,period):
        self.period = period
        self.listone = []
        self.listtwo = []
        self.listthree = []
        self.listfour = []
        self.listfive = []
        # self.list = []
        self.db = pymysql.connect('localhost', 'root', 'lsgogroup14', 'py_mysql')
        self.cursor = self.db.cursor()
        self.date = self.GetDate()


   def GetDate(self):
       sql = "SELECT DATE FROM stock WHERE Date >(DATE_SUB('"+ str(dt.date.today())+ "',INTERVAL 30 DAY)) ORDER BY Date ASC;"
       self.cursor.execute(sql)

       return  self.cursor.fetchall()


   def GetFra(self):
       for i in self.date:
           sql = "SELECT Average_One FROM stock WHERE Date BETWEEN DATE_SUB('" + str(
               i[0]) + "' ,INTERVAL " + str(self.period) + " YEAR) AND '" + str(i[0]) + "'ORDER BY Average_One ASC;"
           days = self.cursor.execute(sql)
           list = self.cursor.fetchall()
           sql1 = "SELECT Average_one FROM stock WHERE Date = '"+str(i[0])+"';"

           self.cursor.execute(sql1)
           temp = self.cursor.fetchone()
           sql2 = "UPDATE stock SET Fractile_Now=" + str(
               (list.index(temp)) * 100 // days) + " WHERE Date='" + str(i[0]) + "';"
           self.cursor.execute(sql2)
           self.db.commit()
           self.listone.append(numpy.percentile(list, 25))
           self.listtwo.append(numpy.percentile(list, 40))
           self.listthree.append(numpy.percentile(list, 50))
           self.listfour.append(numpy.percentile(list, 60))
           self.listfive.append(numpy.percentile(list, 75))


   def FraSql(self,):
       self.Average()
       self.GetFra()
       for i in range(len(self.date)):
           sql1 = "UPDATE stock SET Fractile_25=" + str(self.listone[i]) + "WHERE Date='" + str(self.date[i][0]) + "';"
           sql2 = "UPDATE stock SET Fractile_40=" + str(self.listtwo[i]) + "WHERE Date='" + str(self.date[i][0]) + "';"
           sql3 = "UPDATE stock SET Fractile_50=" + str(self.listthree[i]) + "WHERE Date='" + str(self.date[i][0]) + "';"
           sql4 = "UPDATE stock SET Fractile_60=" + str(self.listfour[i]) + "WHERE Date='" + str(self.date[i][0]) + "';"
           sql5 = "UPDATE stock SET Fractile_75=" + str(self.listfive[i]) + "WHERE Date='" + str(self.date[i][0]) + "';"
           self.cursor.execute(sql1)
           self.cursor.execute(sql2)
           self.cursor.execute(sql3)
           self.cursor.execute(sql4)
           self.cursor.execute(sql5)
           self.db.commit()

   def Average(self):
        sql = "UPDATE stock SET Average_One=(Open_price+Top_price+Floor_price+Close_price)*0.25;"
        sql1 = "UPDATE stock SET Average_Two=Trade_amount/Trade_vol;"
        self.cursor.execute(sql)
        self.cursor.execute(sql1)
        self.db.commit()



