# -*- coding: utf-8 -*-
import pymysql, subject, shutil, time, sys, os, log

conn = None
curs = None

def insert(data, start_date, subject_code):
    init()
    
    for idx in data:
        if int(data[0]) != int(start_date):
            del data[:7]
        else: break

    for date in range(int(start_date), int(get_today_date())): # start_date부터 어제 날짜꺼까지 저장.
        table_name = subject_code + '_' + start_date
        insert_data = []
        print('현재일자 :', start_date)
        log.info('table_name' + table_name)

#        if date != int(data[0]) :
#            log.info('휴장일 : ' + str(date))
#            continue
        if int(date) == int (data[0]) or int(date) == int(start_date) :
            # table_name으로 테이블이 있는지 확인한다.
            if exist_table(table_name) == False:
              log.info('테이블 생성')
              create_table(table_name, False)
        
            # 있으면 삭제 후 재생성
            else:
                log.info('테이블 삭제 후 재생성.')
                create_table(table_name, True)
        
        for idx in range(0, len(data), 7):
            _data = data[idx:idx+7]
            insert_data.append(tuple(_data))

            if int(_data[0]) != date:
                if len(data)==7:
                    del data
                else : del data[:idx-7]
                break
            

        _query = "insert into " + table_name + "(working_day,min_price,max_price,market_price,date,volume,now_price) values (%s, %s, %s, %s, %s, %s, %s)" 
        curs.executemany(_query, tuple(insert_data))
        conn.commit()
def init():
    global conn
    global curs
    conn = pymysql.connect(host='211.253.28.132', user='root', password='goehddl', db='haedong', charset='utf8')
    curs = conn.cursor()

def execute(_query):
    global conn
    global curs
    curs.execute(_query)
    conn.commit()

    rows = curs.fetchall()

    return rows

def close():
    conn.close()

def exist_table(table_name):
    global conn
    global curs
    temp = []

    query = "show tables in haedong like '%s'"%table_name
    curs.execute(query)
    conn.commit()

    #temp =curs.fetchone()
    #row = curs.fetchall()
    tt = curs._rows
    
    if len(tt) !=0 and tt[0][0] == table_name:
        return True
    else: return False

def create_table(table_name, need_delete):
#     무조건 root_table은 있어야함!!
    if need_delete == True:
        # 기존 테이블 삭제
        global conn
        global curs
        query = "drop table %s" %table_name
        curs.execute(query)
        conn.commit()
        curs.close()
        conn.close()

    # 테이블 생성
    conn = pymysql.connect(host='211.253.28.132', user='root', password='goehddl', db='haedong', charset='utf8')
    curs = conn.cursor()
    query = "create table %s select * from root_table" %table_name
    curs.execute(query)
    conn.commit()

def get_tick_from_data(data):
    ret = data[0:7]
    del data[0:7]
    return ret
    
def get_today_date():
    ret = ''
    ret += str(time.localtime().tm_year)
    if time.localtime().tm_mon < 10:
        ret += '0'
    ret += str(time.localtime().tm_mon)
    if time.localtime().tm_mday < 10:
        ret += '0'
    ret += str(time.localtime().tm_mday)

    return ret

def get_next_date(date):
    ret = ''
    tomorrow = time.localtime(time.time() + 86400)
    ret += str(tomorrow.tm_year)
    if time.localtime().tm_mon < 10:
        ret += '0'
    ret += str(tomorrow.tm_mon)
    if time.localtime().tm_mday < 10:
        ret += '0'
    ret += str(tomorrow.tm_mday)
    return ret