# -*- coding: utf-8 -*-
import subject

list = {}

SAFE = '목표달성청산'
DRIBBLE = '드리블'

def add_contract(order_info): # 계약타입(목표달성 청산 또는 달성 후 드리블)
    """
    신규계약을 관리리스트에 추가한다.
      
    :param subject_code: 종목코드
    :param chegyul_price: 체결가
    :param goal_price: 목표가
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
        pass
    else:
        list[subject_code] = {}
        
    safe_num = int(order_info['체결수량']/2)
    dribble_num = order_info['체결수량'] - safe_num
    
    list[subject_code]['계약타입'] = {}
    list[subject_code]['계약타입'][SAFE] = safe_num
    list[subject_code]['계약타입'][DRIBBLE] = dribble_num
    list[subject_code]['체결가']
    list[subject_code]['익절가']
    list[subject_code]['손절가']
    
    return order_info
    
def remove_contract(order_info, type):
    subject_code = order_info['종목코드']
    if type == '익절':
        list[subject_code]['계약타입'][SAFE] = list[subject_code]['계약타입'][SAFE] - order_info['체결수량']
    elif type == '손절':
        del list[subject_code]
        pass
