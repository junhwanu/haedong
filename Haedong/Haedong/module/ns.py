# -*- coding: utf-8 -*-
import contract, subject, log, calc, time, my_util
import log_result as res
import define as d


def is_it_OK(subject_code, current_price):
    print("is_it_OK")
    return order_contents

def is_it_sell(subject_code, current_price):
    print("is_it_sell")
    return {'신규주문':False}

def get_time(add_min,subject_code):
    # 현재 시간 정수형으로 return
    if d.get_mode() == d.REAL: #실제투자
        current_hour = time.localtime().tm_hour
        current_min = time.localtime().tm_min
        current_min += add_min
        if current_min >= 60:
            current_hour += 1
            current_min -= 60
    
        current_time = current_hour*100 + current_min
    
    elif d.get_mode() == d.TEST: #테스트
        current_hour = int(str(calc.data[subject_code]['체결시간'][-1])[8:10])
        current_min = int(str(calc.data[subject_code]['체결시간'][-1])[10:12])
        current_min += add_min
        if current_min >= 60:
            current_hour += 1
            current_min -= 60

        current_time = current_hour*100 + current_min
        
        current_time = int(str(calc.data[subject_code]['체결시간'][-1])[8:12])
        
    return current_time   
