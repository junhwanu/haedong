# -*- coding: utf-8 -*-
import subject

list = {}

SAFE = '목표달성청산'
DRIBBLE = '드리블'

def add_contract(order_number,   # 주문번호
                 subject_code,   # 종목코드
                 chegyul_price,  # 체결가(매수가 또는 매도가)
                 goal_price,     # 목표가
                 sonjul_prcie,   # 손절가
                 contract_type): # 계약타입(목표달성 청산 또는 달성 후 드리블)
    """
    신규계약을 관리리스트에 추가한다.
      
    :param subject_code: 종목코드
    :param chegyul_price: 체결가
    :param goal_price: 목표가
    :param sonjul_prcie: 손절가
    :param contract_type: 계약타입(contract.SAFE | contract.DRIBBLE)
    """

    list[order_number] = {}
    list[order_number]['종목코드'] = subject_code
    list[order_number]['체결가'] = round(chegyul_price, subject.info[subject_code]['자릿수'])
    list[order_number]['목표가'] = round(goal_price, subject.info[subject_code]['자릿수'])
    list[order_number]['손절가'] = round(sonjul_prcie, subject.info[subject_code]['자릿수'])
    list[order_number]['계약타입'] = contract_type

def remove_contract(order_number):
    del list[order_number]

def get_order_number_list():
    rtn = []
    for keys in list:
        rtn.append(keys)
