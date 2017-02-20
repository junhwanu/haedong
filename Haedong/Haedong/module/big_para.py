# -*- coding: utf-8 -*-
import contract, subject, log, calc, time, chart
import define as d
import log_result as res
import datetime

min_price = 99999999
max_price = 0

def is_it_OK(subject_code, current_price):
    profit_tick = 10
    loss_tick = 10
    mesu_medo_type = ''
    contract_cnt = 2
    index = calc.data[subject_code]['idx']
    false = {'신규주문':False}

    if calc.data[subject_code]['idx'] < 1000:
        return false

    state = subject.info[subject_code]['상태']
    if state == '매매완료':
        if calc.data[subject_code]['플로우'][-1] != calc.data[subject_code]['플로우'][-2]:
            if calc.data[subject_code]['플로우'][-1] == '상향': 
                log.info('종목(' + subject_code + ') 상태 변경, ' + state + ' -> 매수구간진입.')
                subject.info[subject_code]['상태'] = '매수구간진입'
            elif calc.data[subject_code]['플로우'][-1] == '하향': 
                log.info('종목(' + subject_code + ') 상태 변경, ' + state + ' -> 매도구간진입.')
                subject.info[subject_code]['상태'] = '매도구간진입'

        return false

    elif state == '매수구간진입' or state == '매도구간진입':
        if state == '매수구간진입' and current_price < min(calc.data[subject_code]['일목균형표']['선행스팬1'][index], calc.data[subject_code]['일목균형표']['선행스팬2'][index]):
            log.info('종목(' + subject_code + ') 상태 변경, ' + state + ' -> 매수가능.')
            subject.info[subject_code]['상태'] = '매수가능'
        elif state == '매도구간진입' and current_price > max(calc.data[subject_code]['일목균형표']['선행스팬1'][index], calc.data[subject_code]['일목균형표']['선행스팬2'][index]):
            log.info('종목(' + subject_code + ') 상태 변경, ' + state + ' -> 매도가능.')
            subject.info[subject_code]['상태'] = '매도가능'
        
        return false

    elif state == '매수가능' or state == '매도가능':
        if state == '매수가능' and current_price > max(calc.data[subject_code]['일목균형표']['선행스팬1'][index], calc.data[subject_code]['일목균형표']['선행스팬2'][index]):
            # 매수
            mesu_medo_type = '신규매수'
            profit_tick = 10000
            loss_tick = 10000
            contract_cnt = 2
        elif state == '매도가능' and current_price < min(calc.data[subject_code]['일목균형표']['선행스팬1'][index], calc.data[subject_code]['일목균형표']['선행스팬2'][index]):
            # 매도
            mesu_medo_type = '신규매도'
            profit_tick = 10000
            loss_tick = 10000
            contract_cnt = 2
        else: return false
    '''
    # 매매완료, 매수가능, 매도가능 아니면 리턴
    state = subject.info[subject_code]['상태']
    log.info('현재 상태 : ' + state)
    if state == '매매완료' and calc.data[subject_code]['플로우'][-1] != calc.data[subject_code]['플로우'][-2]:
        log.info('종목(' + subject_code + ') 상태 변경, ' + state + ' -> 중립대기.')
        subject.info[subject_code]['상태'] = '중립대기'
    if state == '중립대기' or state == '매수가능' or state == '매도가능' or state == '매수구간진입' or state == '매도구간진입':
        log.info('플로우 : ' + calc.data[subject_code]['플로우'][-1])
        log.info('기울기 : ' + str(calc.data[subject_code]['추세선기울기']))
        log.info('추세선 : ' + str(calc.data[subject_code]['추세선'][index]))
        log.info('표준편차 : ' + str(calc.data[subject_code]['표준편차']))

        if calc.data[subject_code]['플로우'][-1] != calc.data[subject_code]['플로우'][-2]:
            if calc.data[subject_code]['플로우'][-1] == '상향':
                if state == '중립대기' or state == '매도구간진입' or state == '매도가능':
                    log.info('종목(' + subject_code + ') 상태 변경, ' + state + ' -> 매수구간진입.')
                    subject.info[subject_code]['상태'] = '매수구간진입'
                else: return false
            elif calc.data[subject_code]['플로우'][-1] == '하향':
                if state == '중립대기' or state == '매수구간진입' or state == '매수가능':
                    log.info('종목(' + subject_code + ') 상태 변경, ' + state + ' -> 매도구간진입.')
                    subject.info[subject_code]['상태'] = '매도구간진입'
                else: return false
            else: return false

        # 기울기가 0.065보다 작아야함
        max_slope = 0.065
        min_slope = 0.02
        trend_line = calc.data[subject_code]['추세선'][index]
        stdev = calc.data[subject_code]['표준편차']
        if state == '매수구간진입':
            if calc.data[subject_code]['추세선기울기'] >= min_slope and calc.data[subject_code]['추세선기울기'] <= max_slope and calc.data[subject_code]['플로우'][-1] == '상향':
                # 매수가능
                if trend_line - 1.8 * stdev >= current_price:
                    log.info('종목(' + subject_code + ') 상태 변경, ' + state + ' -> 매수가능.')
                    subject.info[subject_code]['상태'] = '매수가능'
            return false
        elif state == '매도구간진입':
            min_slope *= -1
            max_slope *= -1
            log.info('추세선기울기 : ' + str(calc.data[subject_code]['추세선기울기']))
            if calc.data[subject_code]['추세선기울기'] <= min_slope and calc.data[subject_code]['추세선기울기'] >= max_slope and calc.data[subject_code]['플로우'][-1] == '하향':
                # 매도가능
                if trend_line + 1.8 * stdev <= current_price:
                    log.info('종목(' + subject_code + ') 상태 변경, ' + state + ' -> 매도가능.')
                    subject.info[subject_code]['상태'] = '매도가능'
            return false

        # 매수/매도가능
        if stdev >= 7 * subject.info[subject_code]['단위']:
            if state == '매수가능':
                if current_price >= trend_line:
                    log.info('종목(' + subject_code + ') 상태 변경, ' + state + ' -> 매수구간진입.')
                    subject.info[subject_code]['상태'] = '매수구간진입'
                    return false
                elif current_price >= trend_line - 1.5 * stdev:
                    if calc.data[subject_code]['추세선기울기'] >= min_slope and calc.data[subject_code]['추세선기울기'] <= max_slope and calc.data[subject_code]['플로우'][-1] == '상향':
                        mesu_medo_type = '신규매수'
                        profit_tick = 10000
                        loss_tick = 10000
                        contract_cnt = 2
                    else: return false
                else:
                    log.info('종목(' + subject_code + ') 매수가능, current_price < trend_line - stdev로 구매 불가(' + str(current_price) + ' < ' + str(trend_line - stdev)) 
                    return false
            elif state == '매도가능':
                min_slope *= -1
                max_slope *= -1
                if current_price <= trend_line:
                    log.info('종목(' + subject_code + ') 상태 변경, ' + state + ' -> 매도구간진입.')
                    subject.info[subject_code]['상태'] = '매도구간진입'
                    return false
                elif current_price <= trend_line + 1.5 * stdev:
                    if calc.data[subject_code]['추세선기울기'] <= min_slope and calc.data[subject_code]['추세선기울기'] >= max_slope and calc.data[subject_code]['플로우'][-1] == '하향':
                        mesu_medo_type = '신규매도'
                        profit_tick = 10000
                        loss_tick = 10000
                        contract_cnt = 2
                    else: return false
                else: 
                    log.info('종목(' + subject_code + ') 매도가능, current_price > trend_line + stdev로 구매 불가(' + str(current_price) + ' > ' + str(trend_line + stdev))
                    return false

        if mesu_medo_type == '':
            return false
    else:
        return false
    '''
    
    order_contents = {'신규주문':True, '매도수구분':mesu_medo_type, '익절틱':profit_tick, '손절틱':loss_tick, '수량':contract_cnt}
    '''
    res.info('##### 주문 예정 #####')
    res.info(order_contents)
    chart.draw(subject_code)
    input()
    '''
    
    return order_contents

def is_it_sell(subject_code, current_price):
    global min_price
    global max_price
    index = calc.data[subject_code]['idx']
    if contract.get_contract_count(subject_code) > 0:
        # 계약 보유중
        trend_line = calc.data[subject_code]['추세선'][index]
        stdev = calc.data[subject_code]['표준편차']
        if contract.list[subject_code]['매도수구분'] == '신규매수':
            # 매수일때
            #if (current_price <= calc.data[subject_code]['추세선밴드']['하한선'][index] and calc.data[subject_code]['추세선'][index] - calc.data[subject_code]['추세선밴드']['하한선'][index] >= 15 * subject.info[subject_code]['단위']) or (calc.data[subject_code]['플로우'][-1] == '하향' and current_price <= contract.list[subject_code]['체결가']):
            if (calc.data[subject_code]['플로우'][-1] == '하향' and current_price > contract.list[subject_code]['체결가'] and current_price < max_price - 50 * subject.info[subject_code]['단위']) or (calc.data[subject_code]['플로우'][-1] == '하향' and current_price <= contract.list[subject_code]['체결가']):
                # 손절 청산
                log.info("손절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                min_price = 99999999
                max_price = 0
                return {'신규주문':True, '매도수구분':'신규매도', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
        
        elif contract.list[subject_code]['매도수구분'] == '신규매도':
            # 매도일때
            if (calc.data[subject_code]['플로우'][-1] == '상향' and current_price < contract.list[subject_code]['체결가'] and current_price > min_price + 50 * subject.info[subject_code]['단위']) or (calc.data[subject_code]['플로우'][-1] == '상향' and current_price >= contract.list[subject_code]['체결가']):
                # 손절 청산
                log.info("손절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                min_price = 99999999
                max_price = 0
                return {'신규주문':True, '매도수구분':'신규매수', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}

    max_price = max(max_price, current_price)
    min_price = min(min_price, current_price)
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
