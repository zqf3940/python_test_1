#-*- coding:utf-8 -*-
import sqlite3
import os
DB_FILE_PATH = 'monitor.db'
SHOW_SQL = False

def get_conn(path):
    conn = sqlite3.connect(path)
    if os.path.exists(path) and os.path.isfile(path):
        return conn
    else:
        conn = None
        return sqlite3.connect(':memory:')

def close_all(conn, cursor):
    try:
        if cursor is not None:
            cursor.close()
    finally:
        if cursor is not None:
            cursor.close()
            
def save_monitor_log_db(data):
    conn = get_conn(DB_FILE_PATH)
    sql_create_tb=(
                    " CREATE TABLE if not exists sys_monitor_data ("
                    " pk             INTEGER PRIMARY KEY ASC AUTOINCREMENT, "
                    " monitor_item   VARCHAR (100), "
                    " monitor_method VARCHAR (15), "
                    " monitor_result VARCHAR, "
                    " monitor_datime DATETIME, "
                    " monitor_remark STRING, "
                    " monitor_detail STRING "
                    " )"
                   )
                   
    conn.execute(sql_create_tb)  
    
    sql_insert = ( " INSERT INTO sys_monitor_data(monitor_item,"
                   "                                monitor_method,"
                   "                                monitor_result,"
                   "                                monitor_datime,"
                   "                                monitor_remark,"
                   "                                monitor_detail) "
                   "               values (?,?,?,?,?,?)"
                 )
                 
    if sql_insert is not None and sql_insert != '':
        if data is not None:
            if conn is not None:
                cursor = conn.cursor()
            else:
                cursor = get_conn('').cursor()
            for d in data:
                if SHOW_SQL:
                    print('execute sql:[{}],parm:[{}]'.format(sql_insert, d))
                cursor.execute(sql_insert, d)
                conn.commit()
            close_all(conn, cursor)
    else:
        print('the [{}] is empty or equal None!'.format(sql_insert))

if __name__ == '__main__':
    data = [('sys testa','login1', 'OK','2018-01-14','desc',''),
            ('sys testa','login2', 'OK', '2018-01-14','desc',''),
            ('sys testa','login3', 'OK', '2018-01-14','desc','')]
    save_monitor_log_db(data)