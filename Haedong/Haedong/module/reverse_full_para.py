# -*- coding: utf-8 -*-
import contract, subject, log, calc, time, my_util
import log_result as res
import define as d

def is_it_OK(subject_code, current_price):
    profit_tick = subject.info[subject_code]['익절틱']
    sonjal_tick = subject.info[subject_code]['손절틱']
    mesu_medo_type = None
    false = {'신규주문': False}
    contract_cnt = 2;



    return order_contents

def is_it_sell(subject_code, current_price):

    return {'신규주문':False}