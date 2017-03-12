# -*- coding: utf-8 -*-
import contract, subject, log, calc, time, my_util
import log_result as res
import define as d

def is_it_OK(subject_code, current_price):

    profit_tick = subject.info[subject_code]['익절틱']
    sonjal_tick = subject.info[subject_code]['손절틱']
    mesu_medo_type = None
    false = {'신규주문': False}

    if calc.data[subject_code]['idx'] < 1200:
        return false
    
    if subject.info[subject_code]['상태'] == '매수중' or subject.info[subject_code]['상태'] == '매도중' or subject.info[subject_code]['상태'] == '청산시도중' or subject.info[subject_code]['상태'] == '매매시도중':
        log.debug('신규 주문 가능상태가 아니므로 매매 불가. 상태 : ' + subject.info[subject_code]['상태'])
        return false
    
    log.debug("종목코드(" + subject_code + ")  현재 Flow : " + subject.info[subject_code]['flow'] + " / SAR : " + str(subject.info[subject_code]['sar']) + " / 추세 : " + my_util.is_sorted(subject_code))
    if subject.info[subject_code]['flow'] == '상향': 
        if current_price < subject.info[subject_code]['sar'] and my_util.is_sorted(subject_code) == '하락세':
            mesu_medo_type = '신규매도'
            log.debug("종목코드(" + subject_code + ") 하향 반전.")
        elif calc.data[subject_code]['플로우'][-2] =='하향' and my_util.is_sorted(subject_code) == '상승세':
            mesu_medo_type = '신규매수'
            log.debug("종목코드(" + subject_code + ") 상향 반전.")
            #return false #임시코드
        else: return false
    elif subject.info[subject_code]['flow'] == '하향':
        if current_price > subject.info[subject_code]['sar'] and my_util.is_sorted(subject_code) == '상승세':
            mesu_medo_type = '신규매수'
            log.debug("종목코드(" + subject_code + ") 상향 반전.")
            #return false #임시코드
        elif calc.data[subject_code]['플로우'][-2] =='상향' and my_util.is_sorted(subject_code) == '하락세':
            mesu_medo_type = '신규매도'
            log.debug("종목코드(" + subject_code + ") 하향 반전.")
        else: return false
    else: return false

    
    if d.get_mode() == d.REAL:
        contract_cnt = int(contract.my_deposit / subject.info[subject_code]['위탁증거금'])
    else:
        contract_cnt = 2
    
    #contract_cnt = 2
    log.debug("종목코드(" + subject_code + ") 신규 매매 계약 수 " + str(contract_cnt))
    
    if contract_cnt == 0: return false
    #if contract_cnt < 4: contract_cnt = 4 #임시코드

    subject.info[subject_code]['반전시현재가'] = current_price
    
    order_contents = {'신규주문':True, '매도수구분':mesu_medo_type, '익절틱':profit_tick, '손절틱':sonjal_tick, '수량':contract_cnt}
    subject.info[subject_code]['주문내용'] = order_contents
    log.debug('para.is_it_OK() : 모든 구매조건 통과.')
    log.debug(order_contents)
    return order_contents

def is_it_sell(subject_code, current_price):
    index = calc.data[subject_code]['idx']
    first_chungsan = 120
    
    log.debug("종목코드(" + subject_code + ") is_it_sell() 진입.")
    log.debug("종목코드(" + subject_code + ") 현재 Flow : " + subject.info[subject_code]['flow'] + " / SAR : " + str(subject.info[subject_code]['sar']))
    if contract.get_contract_count(subject_code) > 0:
        # 계약 보유중
        log.debug("종목코드(" + subject_code + ") is_it_sell() / 보유 계약 : " + str(contract.get_contract_count(subject_code)))
        if contract.list[subject_code]['매도수구분'] == '신규매수':
            # 매수일때
            if current_price <= contract.list[subject_code]['손절가']:
                res.info("손절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                return {'신규주문':True, '매도수구분':'신규매도', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
            elif calc.data[subject_code]['플로우'][-1] == '상향' and subject.info[subject_code]['sar'] > current_price:
                res.info("하향 반전되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                return {'신규주문':True, '매도수구분':'신규매도', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
            elif current_price > contract.list[subject_code]['익절가']:
                contract.list[subject_code]['익절가'] = current_price + subject.info[subject_code]['익절틱'] * subject.info[subject_code]['단위']
                contract.list[subject_code]['손절가'] = current_price - subject.info[subject_code]['익절틱'] * subject.info[subject_code]['단위']
                log.debug("종목코드(" + subject_code + ") 익절가 갱신.")
            elif current_price - subject.info[subject_code]['반전시현재가'] >= first_chungsan * subject.info[subject_code]['단위'] and subject.info[subject_code]['반전시현재가'] != 0 and int(contract.get_contract_count(subject_code) / 2) > 0:
                return {'신규주문':True, '매도수구분':'신규매도', '수량':int((contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])/2)}
        elif contract.list[subject_code]['매도수구분'] == '신규매도':
            # 매도일때
            if current_price >= contract.list[subject_code]['손절가']:
                res.info("손절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                return {'신규주문':True, '매도수구분':'신규매수', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
            elif calc.data[subject_code]['플로우'][-1] == '하향' and subject.info[subject_code]['sar'] < current_price:
                res.info("상향 반전되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                return {'신규주문':True, '매도수구분':'신규매수', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
            elif current_price < contract.list[subject_code]['익절가']:
                contract.list[subject_code]['익절가'] = current_price - subject.info[subject_code]['익절틱'] * subject.info[subject_code]['단위']
                contract.list[subject_code]['손절가'] = current_price + subject.info[subject_code]['익절틱'] * subject.info[subject_code]['단위']
                log.debug("종목코드(" + subject_code + ") 익절가 갱신.")
            elif (subject.info[subject_code]['반전시현재가'] - current_price) >= first_chungsan * subject.info[subject_code]['단위'] and subject.info[subject_code]['반전시현재가'] != 0 and int(contract.get_contract_count(subject_code) / 2) > 0:
                return {'신규주문':True, '매도수구분':'신규매수', '수량':int((contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])/2)}
            
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
        
    return current_time   
