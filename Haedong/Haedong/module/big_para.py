# -*- coding: utf-8 -*-
import contract, subject, log, calc, time
import log_result as res

def is_it_OK(subject_code, current_price):
    profit_tick = 10
    loss_tick = 10
    mesu_medo_type = ''
    contract_cnt = 2
    index = calc.data[subject_code]['idx']
    false = {'신규주문':False}

    # 마감시간 임박 구매 불가
    if get_time(30) >= int(subject.info[subject_code]['마감시간']) and get_time(0) < int(subject.info[subject_code]['마감시간']):
        log.debug('마감시간 임박으로 구매 불가')
        return {'신규주문':False}

    # 매매완료, 매수가능, 매도가능 아니면 리턴
    state = subject.info[subject_code]['상태']
    if state == '매매완료' or state == '매수가능' or state == '매도가능' or state == '매수구간진입' or state == '매도구간진입':
        pass
        # 매매완료
        if stats == '매매완료':
            if calc.data[subject_code]['플로우'][-1] != calc.data[subject_code]['플로우'][-2]:
                if calc.data[subject_code]['플로우'][-1] == '상향': subject.info[subject_code]['상태'] = '매수구간진입'
                elif calc.data[subject_code]['플로우'][-1] == '하향': subject.info[subject_code]['상태'] = '매도구간진입'
                return false

        # 기울기가 0.065보다 작아야함
        max_slope = 0.065
        min_slope = 0.02
        trend_line = calc.data[subject_code]['추세선'][-1]
        stdev = calc.data[subject_code]['표준편차']
        if state == '매수구간진입':
            if calc.data[subject_code]['추세선기울기'] >= min_slope and calc.data[subject_code]['추세선기울기'] <= max_slope and calc.data[subject_code]['플로우'][-1] == '상향':
                # 매수가능
                if trend_line - 1.8 * stdev >= current_price:
                    subject.info[subject_code]['상태'] = '매수가능'
            return false
        elif stats == '매도구간진입':
            if calc.data[subject_code]['추세선기울기'] <= -min_slope and calc.data[subject_code]['추세선기울기'] >= -max_slope and calc.data[subject_code]['플로우'][-1] == '하향':
                # 매도가능
                if trend_line + 1.8 * stdev <= current_price:
                    subject.info[subject_code]['상태'] = '매도가능'
            return false

        # 매수/매도가능
        if state == '매수가능':
            if current_price >= trend_line - stdev:
                mesu_medo_type = '신규매수'
                profit_tick = 10000
                loss_tick = 10000
                contract_cnt = 2
            else: return false
        elif state == '매도가능':
            if current_price <= trend_line + stdev:
                mesu_medo_type = '신규매도'
                profit_tick = 10000
                loss_tick = 10000
                contract_cnt = 2
            else: return false
    else:
        return false

    order_contents = {'신규주문':True, '매도수구분':mesu_medo_type, '익절틱':profit_tick, '손절틱':loss_tick, '수량':contract_cnt}
    return order_contents

def is_it_sell(subject_code, current_price):
    if contract.get_contract_count(subject_code) > 0:
        # 계약 보유중
        trend_line = calc.data[subject_code]['추세선'][-1]
        stdev = calc.data[subject_code]['표준편차']
        if contract.list[subject_code]['매도수구분'] == '신규매수':
            # 매수일때
            if current_price <= trend_line - 2.5 * stdev:
                # 손절 청산
                log.info("손절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                return {'신규주문':True, '매도수구분':'신규매도', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
        
        elif contract.list[subject_code]['매도수구분'] == '신규매도':
            # 매도일때
            if current_price >= trend_line + 2.5 * stdev:
                # 손절 청산
                log.info("손절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                return {'신규주문':True, '매도수구분':'신규매수', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
        
    return {'신규주문':False}

def get_time(add_min):
    # 현재 시간 정수형으로 return
    current_hour = time.localtime().tm_hour
    current_min = time.localtime().tm_min
    if current_min + add_min >= 60:
        current_hour += 1
        current_min -= 60

    current_time = current_hour*100 + current_min

    return current_time