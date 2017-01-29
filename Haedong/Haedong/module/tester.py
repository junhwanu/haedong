# -*- coding: utf-8 -*-
import kiwoom, log, contract, subject, calc, time

def init():
    print('테스트 시작일을 입력하세요. (ex. 20170129)')

    start_date = input()
    end_date = get_yesterday()

    print('종목코드를 입력하세요. (ex. CL)')
    subject_code = input()

    kw = kiwoom.api(2)
    for date in range( int(start_date), int(end_date) ):
        print(str(date) + '테스트 시작.')
        
        # subject_code, data 날짜에 맞는 테이블을 불러온다.

        while True:
            tick = read_tick() # 한 tick 읽어 온다.
            tick_cnt = 0
            candle = {'현재가':0, '거래량':0, '체결시간':0, '시가':0, '고가':0, '저가':999999999, '영업일자':0}

            if tick != None: # tick 정보가 있으면
                tick_cnt += 1
                
                candle['현재가'] = tick['현재가']
                candle['거래량'] += tick['거래량']
                candle['체결시간'] = tick['체결시간']
                
                if tick_cnt == 0:
                    candle['시가'] = tick['시가']
                if candle['고가'] < tick['고가']:
                    candle['고가'] = tick['고가']
                if candle['저가'] > tick['저가']:
                    candle['저가'] = tick['저가']

                kw.OnReceiveRealData(subject_code, None, tick)
                if tick_cnt == subject.info[subject_code]['시간단위']:
                    kw.OnReceiveTrData(subject.info[subject_code]['화면번호'], '해외선물옵션틱그래프조회', None, None, None, candle)   
            else:
                print(str(date) + ' 테스트 종료.')
                break 
        

def get_yesterday():
    return time.localtime().tm_year * 10000 + time.localtime().tm_mon * 100 + time.localtime().tm_mday