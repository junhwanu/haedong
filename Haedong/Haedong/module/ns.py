# -*- coding: utf-8 -*-
import contract, subject, log, calc, time, my_util
import log_result as res
import define as d


def is_it_OK(subject_code, current_price):
    print("ns.is_it_OK")
    
    siga = calc.data[subject_code]['금일']['시가'][-1]
    goga = calc.data[subject_code]['금일']['고가'][-1]
    juga = calc.data[subject_code]['금일']['저가'][-1]
    jonga = calc.data[subject_code]['금일']['현재가'][-1]   
    
    if is_yoju(subject_code) is True:
        return false
    
    contract_cnt = 1
    
    if jonga >= calc.data[subject_code]['금일']['시가'] and siga > calc.data[subject_code]['금일']['시가']: #이전캔들이 음봉, 매수 가능
        if current_price <= calc.data[subject_code]['금일']['시가']:
            mesu_medo_type = '신규매수'
            pass # 매수

    elif jonga <= calc.data[subject_code]['금일']['시가'] and siga < calc.data[subject_code]['금일']['시가']: # 이전캔들이양봉임, 매도가능
        if current_price >= calc.data[subject_code]['금일']['시가']:
            mesu_medo_type = '신규매도'
            pass # 매도

    elif jonga >= calc.data[subject_code]['금일']['중심선'] and siga > calc.data[subject_code]['금일']['시가']: #이전캔들이 음봉, 매수 가능
        if current_price <= calc.data[subject_code]['금일']['중심선']:
            mesu_medo_type = '신규매수'
            pass # 매수

    elif jonga <= calc.data[subject_code]['금일']['중심선'] and siga < calc.data[subject_code]['금일']['시가']: # 이전캔들이양봉임, 매도가능
        if current_price >= calc.data[subject_code]['금일']['중심선']:
            mesu_medo_type = '신규매도'
            pass # 매도     
    
    order_contents = {'신규주문':True, '매도수구분':mesu_medo_type, '익절틱':20, '손절틱':999, '수량':contract_cnt}
    subject.info[subject_code]['주문내용'] = order_contents
    log.debug('ns.is_it_OK() : 모든 구매조건 통과.')
    log.debug(order_contents)
    return order_contents   
    

def is_it_sell(subject_code, current_price):
    print("is_it_sell")
    
    siga = calc.data[subject_code]['금일']['시가'][-1]
    goga = calc.data[subject_code]['금일']['고가'][-1]
    juga = calc.data[subject_code]['금일']['저가'][-1]
    jonga = calc.data[subject_code]['금일']['현재가'][-1]
    
    pre_siga = calc.data[subject_code]['금일']['시가'][-2]
    pre_goga = calc.data[subject_code]['금일']['고가'][-2]
    pre_juga = calc.data[subject_code]['금일']['저가'][-2]
    pre_jonga = calc.data[subject_code]['금일']['현재가'][-2]
    
    
    goal_passed_line = 2 
    goal_tick = 10
    
    if contract.get_contract_count(subject_code) > 0:
        # 계약 보유중
        #log.debug("종목코드(" + subject_code + ") is_it_sell() / 보유 계약 : " + str(contract.get_contract_count(subject_code)))
        #if contract.list[subject_code]['매도수구분'] == '신규매수':
        
        #익절
        if get_passed_line_count(subject_code,current_price) > goal_passed_line and (current_price - contract.list[subject_code]['체결가'])/subject.info[subject_code]['단위'] > goal_tick:
            if contract.list[subject_code]['매도수구분'] == '신규매수':
                num_count = int(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])
                return {'신규주문':True, '매도수구분':'신규매도', '수량':num_count}
            elif contract.list[subject_code]['매도수구분'] == '신규매도':
                num_count = int(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])
                return {'신규주문':True, '매도수구분':'신규매수', '수량':num_count}
        
        #손절 (진입가청산)
        if contract.list[subject_code]['매도수구분'] == '신규매수':
            if abs(contract.list[subject_code]['체결가'] - calc.data[subject_code]['금일']['시가']) > abs(contract.list[subject_code]['체결가'] - calc.data[subject_code]['금일']['중심선']):
                #중심선에서 매수 삼
                if jonga < calc.data[subject_code]['금일']['중심선']:
                    if current_price >= calc.data[subject_code]['금일']['중심선']:
                        num_count = int(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])
                        return {'신규주문':True, '매도수구분':'신규매도', '수량':num_count}   
            else:
                #시가에 매수 삼
                if jonga < calc.data[subject_code]['금일']['시가']:
                    if current_price >= calc.data[subject_code]['금일']['시가']:
                        num_count = int(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])
                        return {'신규주문':True, '매도수구분':'신규매도', '수량':num_count}  
                    
        elif contract.list[subject_code]['매도수구분'] == '신규매도':   
            if abs(contract.list[subject_code]['체결가'] - calc.data[subject_code]['금일']['시가']) > abs(contract.list[subject_code]['체결가'] - calc.data[subject_code]['금일']['중심선']):
                #중심선에서 매도 삼
                if jonga > calc.data[subject_code]['금일']['중심선']:
                    if current_price<= calc.data[subject_code]['금일']['중심선']:
                        num_count = int(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])
                        return {'신규주문':True, '매도수구분':'신규매수', '수량':num_count}   
            else:
                #시가에 매도 삼
                if jonga > calc.data[subject_code]['금일']['시가']:
                    if current_price <= calc.data[subject_code]['금일']['시가']:
                        num_count = int(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])
                        return {'신규주문':True, '매도수구분':'신규매수', '수량':num_count} 
                    
        #손절(진입가 안옴)
        if contract.list[subject_code]['매도수구분'] == '신규매수':
            if abs(contract.list[subject_code]['체결가'] - calc.data[subject_code]['금일']['시가']) > abs(contract.list[subject_code]['체결가'] - calc.data[subject_code]['금일']['중심선']):
                #중심선에서 매수 삼
                if jonga < calc.data[subject_code]['금일']['중심선'] and pre_jonga < calc.data[subject_code]['금일']['중심선']:
                    if get_mang_gg(subject_code,current_price)<=current_price:
                        num_count = int(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])
                        return {'신규주문':True, '매도수구분':'신규매도', '수량':num_count}   
            else:
                #시가에 매수 삼
                if jonga < calc.data[subject_code]['금일']['시가'] and pre_jonga < calc.data[subject_code]['금일']['시가']:
                    if get_mang_gg(subject_code,current_price)<=current_price:
                        num_count = int(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])
                        return {'신규주문':True, '매도수구분':'신규매도', '수량':num_count}  
                    
        elif contract.list[subject_code]['매도수구분'] == '신규매도':   
            if abs(contract.list[subject_code]['체결가'] - calc.data[subject_code]['금일']['시가']) > abs(contract.list[subject_code]['체결가'] - calc.data[subject_code]['금일']['중심선']):
                #중심선에서 매도 삼
                if jonga > calc.data[subject_code]['금일']['중심선'] and pre_jonga > calc.data[subject_code]['금일']['중심선']:
                    if get_mang_gg(subject_code,current_price)>=current_price:
                        num_count = int(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])
                        return {'신규주문':True, '매도수구분':'신규매수', '수량':num_count}   
                #시가에 매도 삼
                if jonga > calc.data[subject_code]['금일']['시가'] and pre_jonga > calc.data[subject_code]['금일']['시가']:
                    if get_mang_gg(subject_code,current_price)>=current_price:
                        num_count = int(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])
                        return {'신규주문':True, '매도수구분':'신규매수', '수량':num_count}

    
    return {'신규주문':False}


def get_passed_line_count(subject_code,current_price):
    rt_value = 0
    start_price = contract.list[subject_code]['체결가']
    
    if current_price > start_price: # 매수일때
        current_price = current_price - subject.info[subject_code]['단위']*2
        
        if calc.data[subject_code]['금일']['중심선'] >= start_price and calc.data[subject_code]['금일']['중심선'] <= current_price:
            rt_value = rt_value + 1
        if calc.data[subject_code]['금일']['시가'] >= start_price and calc.data[subject_code]['금일']['시가'] <= current_price:
            rt_value = rt_value + 1
        for idx in range(0, 5):
            if calc.data[subject_code]['단기선'][idx] >= start_price and calc.data[subject_code]['단기선'][idx] <= current_price:
                rt_value = rt_value + 1
    
    else: # 매도일때
        current_price = current_price + subject.info[subject_code]['단위']*2
        
        if calc.data[subject_code]['금일']['중심선'] <= start_price and calc.data[subject_code]['금일']['중심선'] >= current_price:
            rt_value = rt_value + 1
        if calc.data[subject_code]['금일']['시가'] <= start_price and calc.data[subject_code]['금일']['시가'] >= current_price:
            rt_value = rt_value + 1
        for idx in range(0, 5):
            if calc.data[subject_code]['단기선'][idx] <= start_price and calc.data[subject_code]['단기선'][idx] >= current_price:
                rt_value = rt_value + 1
    
    return rt_value

def get_mang_gg(subject_code,current_price):
    start_price = contract.list[subject_code]['체결가']
    
    if current_price > start_price: # 매수일때
        for idx in range(0, 5):
            if calc.data[subject_code]['단기선'][idx] >= start_price and calc.data[subject_code]['단기선'][idx] <= current_price:
                return calc.data[subject_code]['단기선'][idx]
            
    else: # 매도일때
        current_price = current_price + subject.info[subject_code]['단위']*2            
        for idx in range(0, 5):
            if calc.data[subject_code]['단기선'][idx] <= start_price and calc.data[subject_code]['단기선'][idx] >= current_price:
               return calc.data[subject_code]['단기선'][idx]
    
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

def is_yoju(subject_code):
    body = abs(calc.data[subject_code]['현재가'][-1] - calc.data[subject_code]['시가'][-1])
    tail = abs(calc.data[subject_code]['고가'][-1] - calc.data[subject_code]['저가'][-1]) - body
    
    if tail > body * 1.5:
        return True
    return False
