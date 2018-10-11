import pymysql


class GetData():
    def __init__(self,start, end):
        self.start = start
        self.end = end


    def Get(self):
        db = pymysql.connect('localhost', 'root', 'lsgogroup14', 'py_mysql')
        cursor = db.cursor()
        sql = "SELECT Date Fractile_Now FROM stock WHERE Date BETWEEN '" \
              + datestart+"' AND '" + dateend +"' ORDER BY DATE ASC;"
        # sql1 = "SELECT Date FROM stock WHERE Date BETWEEN '"\
        #        + datestart+"' AND '" + dateend +"' ORDER BY DATE ASC;"
        cursor.execute(sql)
        list = cursor.fetchall()
        print(list)
        # cursor.execute(sql1)
        # date = cursor.fetchall()