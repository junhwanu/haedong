﻿# -*- coding: utf-8 -*-
import screen


info = {      
            "GCJ17":{
                "종목명":"GOLD",
                "시간단위":60,
                "단위":0.1,
                "자릿수": 1,
                "틱가치": 10,
                "화면번호":screen.S9998,
                "상태":"매매완료",
                "매매구간누적캔들": 0,
                "최소연속틱":50,
                "이동평균선":[60, 150],
                "마감시간": '0700',
                "시작시간": '0800',
                "주문내용": {},
                "청산내용": {},
                "sar":0,
                "ep":0,
                "init_af":0.0008,
                "af":0.0008,
                "maxaf":0.002,
                "flow":"",
                "전략":"풀파라",
                "누적수익": 0,
                "신규매매수량":2,
                "반전시현재가":0,
                "이상신호":False,
                "익절틱":50,
                "손절틱":50,
                "매매틱간격":0,
                "sar매매틱간격":9999, #7
                "매매시일목현재가최소차이":99999, #3
                "일목이탈로인한손절틱":99999, #6
                "리버스드리블틱":0, #3
                "현재가변동횟수":0,
                }
            }

'''
"CL":{
    "종목명":"CRUDEOIL",
    "시간단위":30,
    "단위":0.01,
    "자릿수": 2,
    "틱가치": 10,
    "화면번호":screen.S9999,
    "상태":"중립대기",
    "매매구간누적캔들": 0,
    "최소연속틱":50,
    "이동평균선":[30, 120],
    "마감시간": '0700',
    "시작시간": '0800',
    "주문내용": {},
    "sar":0,
    "ep":0,
    "init_af":0.0009,
    "af":0.0009,
    "maxaf":0.02,
    "flow":"",
    "전략":"파라",
    "누적수익": 0,
    "신규매매수량":2,
    "반전시현재가":0,
    "이상신호":False,
    "익절틱":10,
    "손절틱":10,
    "sar매매틱간격":7, #7
    "매매시일목현재가최소차이":3, #3
    "일목이탈로인한손절틱":6, #6
    "리버스드리블틱":3, #3
    "현재가변동횟수":0
    },
"NG":{
    "종목명":"NATURALGAS",
    "시간단위":30,
    "단위":0.001,
    "자릿수": 3,
    "틱가치": 10,
    "화면번호":screen.S9995,
    "상태":"중립대기",
    "매매구간누적캔들": 0,
    "최소연속틱":50,
    "이동평균선":[30, 120],
    "마감시간": '0700',
    "시작시간": '0800',
    "주문내용": {},
    "sar":0,
    "ep":0,
    "init_af":0.0009,
    "af":0.0009,
    "maxaf":0.02,
    "flow":"",
    "전략":"파라",
    "누적수익": 0,
    "신규매매수량":2,
    "반전시현재가":0,
    "이상신호":False,
    "익절틱":10,
    "손절틱":10,
    "sar매매틱간격":7, #7
    "매매시일목현재가최소차이":3, #3
    "일목이탈로인한손절틱":6, #6
    "리버스드리블틱":3, #3
    "현재가변동횟수":0
    },
"6E":{
    "종목명":"EUROFX",
    "시간단위":30,
    "단위":0.00005,
    "자릿수": 5,
    "틱가치": 6.250,
    "화면번호":screen.S9996,
    "상태":"중립대기",
    "매매구간누적캔들": 0,
    "최소연속틱":50,
    "이동평균선":[30, 120],
    "마감시간": '0700',
    "시작시간": '0800',
    "sar":0,
    "ep":0,
    "init_af":0.0009,
    "af":0.0009,
    "maxaf":0.02,
    "flow":"",
    "전략":"파라",
    "누적수익": 0,
    "신규매매수량":2,
    "반전시현재가":0,
    "이상신호":False,
    "익절틱":10,
    "손절틱":10,
    "sar매매틱간격":7, #7
    "매매시일목현재가최소차이":3, #3
    "일목이탈로인한손절틱":6, #6
    "리버스드리블틱":3, #3
    "현재가변동횟수":0
    },
"6A":{
    "종목명":"AUSTRALIANDOLLAR",
    "시간단위":30,
    "단위":0.0001,
    "자릿수": 4,
    "틱가치": 10,
    "화면번호":screen.S9993,
    "상태":"중립대기",
    "매매구간누적캔들": 0,
    "최소연속틱":50,
    "이동평균선":[30, 120],
    "마감시간": '0700',
    "시작시간": '0800',
    "sar":0,
    "ep":0,
    "init_af":0.0009,
    "af":0.0009,
    "maxaf":0.02,
    "flow":"",
    "전략":"파라",
    "누적수익": 0,
    "신규매매수량":2,
    "반전시현재가":0,
    "이상신호":False,
    "익절틱":10,
    "손절틱":10,
    "sar매매틱간격":7, #7
    "매매시일목현재가최소차이":3, #3
    "일목이탈로인한손절틱":6, #6
    "리버스드리블틱":3, #3
    "현재가변동횟수":0
    },
"HG":{
    "종목명":"COPPER",
    "시간단위":30,
    "단위":0.0005,
    "자릿수": 4,
    "틱가치": 12.5,
    "화면번호":screen.S9997,
    "상태":"중립대기",
    "매매구간누적캔들": 0,
    "최소연속틱":50,
    "이동평균선":[30, 120],
    "마감시간": '0700',
    "시작시간": '0800',
    "sar":0,
    "ep":0,
    "init_af":0.0009,
    "af":0.0009,
    "maxaf":0.02,
    "flow":"",
    "전략":"파라",
    "누적수익": 0,
    "신규매매수량":2,
    "반전시현재가":0,
    "이상신호":False,
    "익절틱":10,
    "손절틱":10,
    "sar매매틱간격":7, #7
    "매매시일목현재가최소차이":3, #3
    "일목이탈로인한손절틱":6, #6
    "리버스드리블틱":3, #3
    "현재가변동횟수":0
    },
"ZC":{
    "종목명":"CORN",
    "시간단위":30,
    "단위":0.25,
    "자릿수": 2,
    "틱가치": 12.5,
    "화면번호":screen.S9994,
    "상태":"중립대기",
    "매매구간누적캔들": 0,
    "최소연속틱":50,
    "이동평균선":[30, 120],
    "마감시간": '1000',
    "시작시간": '0420',
    "sar":0,
    "ep":0,
    "init_af":0.0009,
    "af":0.0009,
    "maxaf":0.02,
    "flow":"",
    "전략":"파라",
    "누적수익": 0,
    "신규매매수량":2,
    "반전시현재가":0,
    "이상신호":False,
    "익절틱":10,
    "손절틱":10,
    "sar매매틱간격":7, #7
    "매매시일목현재가최소차이":3, #3
    "일목이탈로인한손절틱":6, #6
    "리버스드리블틱":3, #3
    "현재가변동횟수":0
    }

}
'''
        
        
        




'''
중립대기 
매매선터치 
매매구간진입 
매매시도중
매수가능
매도가능
매매중
청산시도중
매매중
매매완료 or 중립대기
'''