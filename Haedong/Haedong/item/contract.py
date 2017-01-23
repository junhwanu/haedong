﻿# -*- coding: utf-8 -*-
import subject

list = {}

SAFE = '목표달성청산'
DRIBBLE = '드리블'
ALL = '전체'

def add_contract(order_info, order_contents): # 계약타입(목표달성 청산 또는 달성 후 드리블)
    """
    신규계약을 관리리스트에 추가한다.
      
    :param subject_code: 종목코드
    :param chegyul_current_price: 체결가
    :param goal_current_price: 목표가
    :param sonjul_prcie: 손절가
    :param contract_type: 계약타입(contract.SAFE | contract.DRIBBLE)
    
    dic = {} 
    dic['주문번호'] = order_info['주문번호']  
    dic['원주문번호'] = order_info['원주문번호'] 
    dic['주문유형'] = order_info['주문유형'] 
    dic['종목코드'] = order_info['종목코드']   
    dic['매도수구분'] = order_info['매도수구분']       
    dic['체결표시가격'] = order_info['체결표시가격'] 
    dic['신규수량'] = order_info['신규수량']     
    dic['청산수량'] = order_info['청산수량']     
    dic['체결수량'] = order_info['체결수량']  
    """
    
    subject_code = order_info['종목코드']
    if subject_code in list:
        logger.error("%s 종목은 이미 %s계약 보유 중 입니다" % (list[subject_code]['보유수량'],subject_code))
        return False
    else:
        list[subject_code] = {}
        
        safe_num = int(order_info['체결수량']/2)
        dribble_num = order_info['체결수량'] - safe_num
        
        list[subject_code]['계약타입'] = {}
        list[subject_code]['계약타입'][SAFE] = safe_num
        list[subject_code]['계약타입'][DRIBBLE] = dribble_num
        list[subject_code]['체결가'] = order_info['체결가']
        list[subject_code]['매도수구분'] = order_contents['매도수구분']

        list[subject_code]['익절가'] = list[subject_code]['체결가'] + order_contents['목표틱'] * subject.info[subject_code]['단위']
        list[subject_code]['손절가'] = list[subject_code]['체결가'] - order_contents['목표틱'] * subject.info[subject_code]['단위']
        list[subject_code]['보유수량'] = order_info['체결수량'] 
    
    return True
    
def remove_contract(order_info):
    subject_code = order_info['종목코드']
    remove_cnt = order_info['체결수량']
    
    if subject_code in list:
        if list[subject_code]['계약타입'][SAFE] >= remove_cnt:
            log.info("%s 종목 보유 중인 SAFE Type 계약 수 변경, 계약수 %s -> %s" % (subject_code,list[subject_code]['계약타입'][SAFE],
                                                                      list[subject_code]['계약타입'][SAFE]-remove_cnt))
            list[subject_code]['계약타입'][SAFE] -= remove_cnt
        
        else:
            remove_cnt -= list[subject_code]['계약타입'][SAFE]
            list[subject_code]['계약타입'][SAFE] = 0
            list[subject_code]['계약타입'][DRIBBLE] -= remove_cnt
            del list[subject_code]
            log.info("%s 종목 모든 계약 청산 합니다." % subject_code)

        return True
        
    else:
        logger.error("%s 종목은 가지고 있는 계약이 없습니다." % subject_code)
        return False

def get_contract_count(subject_code):
    if subject_code in list:
        count = list[subject_code][SAFE] + list[subject_code][DRIBBLE]
        return count
    else:
        return 0