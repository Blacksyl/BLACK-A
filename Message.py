import pymysql




class Messsge():

    def GetData(self):
        db = pymysql.connect('localhost', 'root', 'lsgogroup14', 'py_mysql')
        sql = "select * from stock where Date in(select max(Date) from stock);"

        cursor = db.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        db.commit()
        db.close()
        # temp = '\n日期：' + str(data[0]) + '\n开盘价：' + str(data[1]) + '\n最高价：' + str(data[2]) + '\n最底价：' + str(data[3]) + '\n收盘价：' + str(data[4]) + '\n平均价：' + str(data[9]) + '\n分位数：' + str(data[16])
        temp = '最新消息 ： 日期：' + str(data[0]) + ' ; 开盘价：' + str(data[1]) + ' ; 最高价：' + str(data[2]) + ' ; 最底价：' \
               + str(data[3]) + ' ; 收盘价：' + str(data[4]) + ' ; 平均价：' + str(data[9]) + ' ; 当前分位数：' + str(data[16])
        # print(temp)
        # with open('messagesend', 'r+', encoding='utf-8') as file:
        #     file.truncate()
        #     file.write('日期：' + str(data[0]) + '\n开盘价：' + str(data[1]) + '\n最高价：' + str(data[2]) + '\n最底价：'
        #                + str(data[3]) + '\n收盘价：' + str(data[4]) + '\n平均价：' + str(data[9]) + '\n分位数：' + str(data[16]))
        return temp
