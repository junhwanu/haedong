﻿# -*- coding: utf-8 -*-
import screen


info = {        
            "GC":{
                "종목명":"GOLD",
                "시간단위":30,
                "단위":0.1,
                "자릿수": 1,
                "틱가치": 10,
                "화면번호":screen.S9998,
                "상태":"중립대기",
                "매매구간누적캔들": 0,
                "최소연속틱":50,
                "이동평균선":[30, 120],
                "마감시간": '0700',
                "시작시간": '0800',
                "주문내용": {},
                "sar":0,
                "ep":0,
                "init_af":0.0008,
                "af":0.0008,
                "maxaf":0.02,
                "flow":"",
                "전략":"파라",
                "누적수익": 0,
                "신규매매수량":2,
                "sar매매틱간격":6,
                "이상신호":False
                },
            "CL":{
                "종목명":"CRUDEOIL",
                "시간단위":30,
                "단위":0.01,
                "자릿수": 2,
                "틱가치": 10,
                "화면번호":screen.S9999,
                "상태":"매매완료",
                "매매구간누적캔들": 0,
                "최소연속틱":50,
                "이동평균선":[30, 120],
                "마감시간": '0700',
                "시작시간": '0800',
                "주문내용": {},
                "sar":0,
                "ep":0,
                "init_af":0.0008,
                "af":0.0008,
                "maxaf":0.02,
                "flow":"",
                "전략":"파라",
                "누적수익": 0,
                "신규매매수량":2,
                "sar매매틱간격":6,
                "이상신호":False
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
                "init_af":0.0008,
                "af":0.0008,
                "maxaf":0.02,
                "flow":"",
                "전략":"파라",
                "누적수익": 0,
                "신규매매수량":2,
                "sar매매틱간격":6,
                "이상신호":False
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
                "init_af":0.0008,
                "af":0.0008,
                "maxaf":0.02,
                "flow":"",
                "전략":"파라",
                "누적수익": 0,
                "신규매매수량":2,
                "sar매매틱간격":6,
                "이상신호":False
                }

        }
        
        




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