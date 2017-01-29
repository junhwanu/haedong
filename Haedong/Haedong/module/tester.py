# -*- coding: utf-8 -*-
import kiwoom, log, contract, subject, calc, time, pymysql

curs = None
conn = None
def init():
    print('테스트 시작일을 입력하세요. (ex. 20170129)')

    start_date = input()
    end_date = get_yesterday()

    print('종목코드를 입력하세요. (ex. CL)')
    subject_code = input()

    kw = kiwoom.api(2)

    connect()
    for date in range( int(start_date), int(end_date) ):
        tick_cnt = 0
        print(str(date) + '테스트 시작.')
        table_name = subject_code  +'_'+ str(date)

        if exist_table(table_name) == False:
            continue
        
        # subject_code, data 날짜에 맞는 테이블을 불러온다.

        while True:
            tick = read_tick(table_name) # 한 tick 읽어 온다.
            
            candle = {'현재가':0, '거래량':0, '체결시간':0, '시가':0, '고가':0, '저가':999999999, '영업일자':0}

            if tick != None: # tick 정보가 있으면
                tick_cnt += 1
                
                candle['현재가'] = tick[1]
                candle['거래량'] += tick[4]
                candle['체결시간'] = tick[0]
                candle['시가'] = tick[6]
                candle['고가'] = tick[3]
                candle['저가'] = tick[2]
                candle['영업일자'] = tick[5]
                
                if tick_cnt == 0:
                    candle['시가'] = tick[6]
                if candle['고가'] < tick[3]:
                    candle['고가'] = tick[3]
                if candle['저가'] > tick[2]:
                    candle['저가'] = tick[2]
                print('tick_cnt : ', tick_cnt)

                #kw.OnReceiveRealData(subject_code, None, tick)
                if tick_cnt == subject.info[subject_code]['시간단위']:
                    print('캔들추가')
                    tick_cnt = 0
                    #kw.OnReceiveTrData(subject.info[subject_code]['화면번호'], '해외선물옵션틱그래프조회', None, None, None, candle)   
            else:
                print(str(date) + ' 테스트 종료.')
                break 
    disconnect()

def get_yesterday():
    return time.localtime().tm_year * 10000 + time.localtime().tm_mon * 100 + time.localtime().tm_mday

def connect():
    global curs
    global conn
    conn = pymysql.connect(host='211.253.28.132', user='root', password='goehddl', db='test_db1', charset='utf8')
    curs = conn.cursor()

def disconnect():
    conn.close()

def read_tick(table_name):
    #conn = pymysql.connect(host='211.253.28.132', user='root', password='goehddl', db='test_db1', charset='utf8')
    #curs = conn.cursor()
    
    global curs
    global conn
    query = "select * from %s"%table_name
    curs.execute(query)
    conn.commit()   
    
#    rows = curs.fetchone()
    row =curs.fetchone()
    
    return row

def exist_table(table_name):
    global curs
    global conn
    temp = []
    #conn = pymysql.connect(host='211.253.28.132', user='root', password='goehddl', db='test_db1', charset='utf8')
    #curs = conn.cursor()
    query = "show tables in test_db1 like '%s'"%table_name
    curs.execute(query)
    conn.commit()
    
    temp = curs.fetchone()

    if temp != None and temp[0] == table_name:
        return True
    else: return False