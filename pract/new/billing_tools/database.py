import pymysql
from pymysql import converters
from pymysql import FIELD_TYPE

class Database:
    def __init__(self, host, user, passwd, dbname):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.dbname = dbname
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    passwd=self.passwd,
                                    db=self.dbname)
        if self.conn:
            return "Success"

        return "Failed"

    def _validate_query(self, query):
        if 'delete ' in query:
            return 'Delete is not allowed in queries'

        if query.startswith('update'):
            return 'Update is not allowed in queries'

        return 'Pass'

    def run_query(self, query, data):
        if self.conn == None:
            return "Database not connected"

        ret = self._validate_query(query)
        if ret != 'Pass':
            return ret

        cursor = self.conn.cursor()
        cursor.execute(query, args=data)
        results = {}
        desc = [d[0] for d in cursor.description]
        results['fields'] = desc
        results['entries'] = cursor.fetchall()
        cursor.close()
        return results
    
    def run_telnet_sql(self,query1,query2,data):
        if self.conn == None:
            return "Database not connected"
        #cursor = self.conn.cursor()
        #cursor.execute(query)
        #result=cursor.fetchall()[0][0]
        #result=int(result)
        #cursor.close()
        #return result
        cursor = self.conn.cursor()
        cursor.execute(query1)  
        result1=cursor.fetchall()[0][0]
        cursor.execute(query2,args=data)
        result2=cursor.fetchall()[0][0]
        cursor.close()
        return result1,result2

    def close(self):
        self.conn.close()
        self.conn = None
