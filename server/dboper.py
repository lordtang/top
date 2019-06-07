import pymysql
import dbconf
#数据库访问类
class DBOper:
    def __init__(self):#构造方法
        self.host=dbconf.host
        self.user=dbconf.user
        self.passwd=dbconf.passwd     
        self.dbname=dbconf.dbname
        self.dbcharset = dbconf.dbcharset
        self.db_conn=None#数据库连接对象  
        
    def open_conn(self):#连接数据库
        try:
            self.db_conn = pymysql.connect(self.host,self.user,self.passwd,self.dbname,use_unicode=True,charset='utf8')
        except Exception as e:
            print('数据库连接错误')
            print(e)
        else:
            print('数据库连接成功')

    def close_conn(self):#关闭连接
        try:
            self.db_conn.close()
        except Exception as e:
            print('数据库关闭错误')
            print(e)
        else:
            print('数据库关闭成功')

    #执行查询，返回结果集
    def do_query(self,sql):
        if not sql:#参数合法性判断
            print('SQL语句不合法')
            return None

        if sql=='':#参数合法性判断
            print('SQL语句不合法')
            return None
        
        # try:
        cursor = self.db_conn.cursor()#获取游标
        cursor.execute(sql)#执行sql语句
        result = cursor.fetchall()#获取数据
        cursor.close()#关闭游标
        print("查询到结果")
        return result #返回查询数据集
        # except Exception as e:
        #     print('查询出错')
        #     # print(e)
        #     return None
        
    #执行增 删 改等变更操作
    def do_update(self,sql):
        if not sql:#参数合法性判断
            print('SQL语句不合法')
            return None
        if sql=='':#参数合法性判断
            print('SQL语句不合法')
            return None
        
        try:
            cursor = self.db_conn.cursor()#获取游标
            result = cursor.execute(sql)#执行SQL语句
            self.db_conn.commit()#提交事务
            cursor.close()
            print("更新完成")
            return result #返回受影响的笔数
        except Exception as e:
            # print('执行SQL语句出错')
            print(e)
            return None

    def do_sql(self,sql,flag):
        if flag == 0:
            print("执行sql语句")
            result = self.do_query(sql)
            if result == None:
                return None
            else:
                return result 
        elif flag == 1:
            print("执行更新表操作")
            result = self.do_update(sql)
            if result == None:
                return False
            else:
                return True







    
    