import pymysql


# -*- coding: utf-8 -*


class ToMySql():

    def __init__(self,list):
        self.list = list



    def Insert(self):
        # 插入操作

        db = pymysql.connect('localhost', 'root', 'lsgogroup14', 'py_mysql')

        for i in range(len(self.list) // 9):
            sql = "INSERT IGNORE INTO stock (Date, Open_price, Top_price, Floor_price, Close_price, Change_price, " \
                  "Change_percent, Trade_vol,Trade_amount ) VALUES ('" + self.list[i * 9] + "','" + \
                  self.list[i * 9 + 1].replace(',', '') + "','" + \
                  self.list[i * 9 + 2].replace(',', '') + "','" + self.list[i * 9 + 3].replace(',', '') + "','" + \
                  self.list[i * 9 + 4].replace(',', '') + "','" + self.list[i * 9 + 5].replace(',', '') + "','" + \
                  self.list[i * 9 + 6].replace(',', '') + "','" + self.list[i * 9 + 7].replace(',', '') + "','" + \
                  self.list[i * 9 + 8].replace(',', '') + "');"

            cursor = db.cursor()
            cursor.execute(sql)
            db.commit()

        db.close()




