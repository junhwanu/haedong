# -*- coding: utf-8 -*-
import contract, subject, log, calc, time
import log_result as res

def is_it_OK(subject_code, current_price):
    
    profit_tick = 10
    sonjal_tick = 10
    
    # 마감시간 임박 구매 불가
    if get_time(30) >= int(subject.info[subject_code]['마감시간']) and get_time(0) < int(subject.info[subject_code]['마감시간']):
        log.debug('마감시간 임박으로 구매 불가')
        return {'신규주문':False}

    if calc.data[subject_code]['idx'] < 300:
        return {'신규주문':False}
    if calc.data[subject_code]['idx'] == 300:
        subject.info[subject_code]['상태'] = '매매완료'

    if subject.info[subject_code]['상태'] == '매수중' or subject.info[subject_code]['상태'] == '매도중' or subject.info[subject_code]['상태'] == '청산시도중' or subject.info[subject_code]['상태'] == '매매시도중':
        log.info('신규 주문 가능상태가 아니므로 매매 불가. 상태 : ' + subject.info[subject_code]['상태'])
        return {'신규주문':False}

    if calc.data[subject_code]['이동평균선'][30][-1] == None :
        log.info('이동평균선 미생성으로 매매 불가. 현재 이동평균선30 : ' + str(calc.data[subject_code]['이동평균선'][30][-1]))
        return {'신규주문':False}

    if calc.data[subject_code]['일목균형표']['선행스팬1'][-1] == None :
        log.info('선행스팬 미생성으로 매매 불가.')
        return {'신규주문':False}    
    

    #log.info('현재 flow : ' + subject.info[subject_code]['flow'])
    #log.info('현재 sar : ' + str(subject.info[subject_code]['sar']))
    #log.info('현재 flow : ' + subject.info[subject_code]['flow'])
    if subject.info[subject_code]['flow'] == '상향' and subject.info[subject_code]['상태'] != '매도가능': 
        #res.info('현재 SAR : ' + str(subject.info[subject_code]['sar']) + ', 현재가 : ' + str(current_price))
        if current_price < subject.info[subject_code]['sar']:
            if current_price < min(calc.data[subject_code]['일목균형표']['선행스팬1'][-1],calc.data[subject_code]['일목균형표']['선행스팬2'][-1]):
                log.info('상태 변경, ' + subject.info[subject_code]['상태'] + ' -> 매도가능, 현재가:'+str(current_price))
                subject.info[subject_code]['상태'] = '매도가능' # flow가 상향일 때, 현재가가 SAR을 하향 돌파하여, 매도 가능 상태로 변경
                calc.data[subject_code]['매매가능가'] = current_price + subject.info[subject_code]['sar매매틱간격'] * subject.info[subject_code]['단위']
                calc.data[subject_code]['매매가능가'] = round(calc.data[subject_code]['매매가능가'],subject.info[subject_code]['자릿수'])
                log.info('현재 SAR : ' + str(subject.info[subject_code]['sar']) + ', 매매가능가 : ' + str(calc.data[subject_code]['매매가능가']))
            else:
                log.info("현재가가 일목균형표 아래 위치 하지 않아 매도 시도 하지 않습니다. flow는 skip 합니다.")
                subject.info[subject_code]['상태'] = '매매완료'
    elif subject.info[subject_code]['flow'] == '하향' and subject.info[subject_code]['상태'] != '매수가능':
        #res.info('현재 SAR : ' + str(subject.info[subject_code]['sar']) + ', 현재가 : ' + str(current_price))
        if current_price > subject.info[subject_code]['sar']:
            if current_price > max(calc.data[subject_code]['일목균형표']['선행스팬1'][-1],calc.data[subject_code]['일목균형표']['선행스팬2'][-1]):
                log.info('상태 변경, ' + subject.info[subject_code]['상태'] + ' -> 매수가능, 현재가:'+str(current_price))
                subject.info[subject_code]['상태'] = '매수가능' # flow가 하향일 때, 현재가가 SAR을 상향 돌파하여, 매수 가능 상태로 변경
                calc.data[subject_code]['매매가능가'] = current_price - subject.info[subject_code]['sar매매틱간격'] * subject.info[subject_code]['단위']
                calc.data[subject_code]['매매가능가'] = round(calc.data[subject_code]['매매가능가'],subject.info[subject_code]['자릿수'])
                log.info('현재 SAR : ' + str(subject.info[subject_code]['sar']) + ', 매매가능가 : ' + str(calc.data[subject_code]['매매가능가']))
            else:
                log.info("현재가가 일목균형표 위에 위치 하지 않아 매도 시도 하지 않습니다. 해동 flow는 skip 합니다.")
                subject.info[subject_code]['상태'] = '매매완료'
                
    if subject.info[subject_code]['상태'] == '매수가능' :
        #if max(calc.data[subject_code]['매매가능가'], calc.data[subject_code]['이동평균선'][30][-1]) >= current_price:
        if calc.data[subject_code]['매매가능가'] >= current_price:
            log.info('매수 시점. 매매가능가 : ' + str(calc.data[subject_code]['매매가능가']) + ', 30이평선 : ' + str(calc.data[subject_code]['이동평균선'][30][-1]))
            pass
        else: return {'신규주문':False}
    elif subject.info[subject_code]['상태'] == '매도가능':
        #if min(calc.data[subject_code]['매매가능가'], calc.data[subject_code]['이동평균선'][30][-1]) <= current_price:
        if calc.data[subject_code]['매매가능가'] <= current_price:
            log.info('매도 시점. 매매가능가 : ' + str(calc.data[subject_code]['매매가능가']) + ', 30이평선 : ' + str(calc.data[subject_code]['이동평균선'][30][-1]))
            pass
        else: return {'신규주문':False}
    else : return {'신규주문':False}

    contract_cnt = subject.info[subject_code]['신규매매수량']

    # 매도수구분 설정
    mesu_medo_type = None
    if subject.info[subject_code]['상태'] == '매수가능' :
        mesu_medo_type = '신규매수'
    elif subject.info[subject_code]['상태'] == '매도가능':
        mesu_medo_type = '신규매도'

    order_contents = {'신규주문':True, '매도수구분':mesu_medo_type, '익절틱':profit_tick, '손절틱':sonjal_tick, '수량':contract_cnt}
    subject.info[subject_code]['주문내용'] = order_contents
    log.debug('para.is_it_OK() : 모든 구매조건 통과.')
    log.debug(order_contents)
    return order_contents

def is_it_sell(subject_code, current_price):
    if subject.info[subject_code]['flow'] == '상향' and subject.info[subject_code]['상태'] == '매수중':
        if current_price < subject.info[subject_code]['sar']:
            if contract.get_contract_count(subject_code) > 0:
                log.info('flow가 상향이고, 현재가가  sar 보다 작으므로 매도 시도')
                return {'신규주문':True, '매도수구분':'신규매도', '수량': contract.get_contract_count(subject_code)}
    elif subject.info[subject_code]['flow'] == '하향' and subject.info[subject_code]['상태'] == '매도중':
        if current_price > subject.info[subject_code]['sar']:
            if contract.get_contract_count(subject_code) > 0:
                log.info('flow가 하향이고, 현재가가  sar 보다 크므로 매수 시도')
                return {'신규주문':True, '매도수구분':'신규매수', '수량': contract.get_contract_count(subject_code)}

    if contract.get_contract_count(subject_code) > 0:
        #log.info('보유 계약 수 : ' + str(contract.get_contract_count(subject_code)))
        # 계약 보유중
        if contract.list[subject_code]['매도수구분'] == '신규매수':
            # 매수일때
            if current_price >= contract.list[subject_code]['익절가']: 
                if contract.list[subject_code]['계약타입'][contract.DRIBBLE] > 0:
                    # 드리블 수량이 남아있다면
                    if get_time(30) >= int(subject.info[subject_code]['마감시간']) and get_time(0) < int(subject.info[subject_code]['마감시간']):
                        log.info('마감시간 임박으로 드리블 불가. 모두 청산.')
                        return {'신규주문':True, '매도수구분':'신규매도', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
                    else:
                        log.info("드리블 목표 달성으로 익절가 수정.")
                        #contract.list[subject_code]['익절가'] = current_price + ( subject.info[subject_code]['주문내용']['익절틱'] * subject.info[subject_code]['단위'] )
                        contract.list[subject_code]['익절가'] = current_price + ( subject.info[subject_code]['단위'] )
                        contract.list[subject_code]['손절가'] = current_price - ( (subject.info[subject_code]['주문내용']['손절틱'] - 1) * subject.info[subject_code]['단위'] ) # 수수료 때문에 1틱 뺌
                        #contract.list[subject_code]['손절가'] = current_price - ( subject.info[subject_code]['단위'] ) # 수수료 때문에 1틱 뺌

                # 목표달성 청산
                if contract.list[subject_code]['계약타입'][contract.SAFE] > 0:
                    log.info("목표달성 청산으로 드리블 수량 제외하고 " + str(contract.list[subject_code]['계약타입'][contract.SAFE]) + "개 청산 요청.")
                    return {'신규주문':True, '매도수구분':'신규매도', '수량':contract.list[subject_code]['계약타입'][contract.SAFE]}
            
            ### 예를 들어 10틱 목표가인데 8틱까지 올라가면 손절가를 체결가 + 1 로 설정하여 -10틱 까지 가서 손절되는것을 막는다
            elif current_price >= contract.list[subject_code]['익절가'] - (int(subject.info[subject_code]['주문내용']['익절틱']*0.2)*subject.info[subject_code]['단위']):
                if contract.list[subject_code]['체결가'] > contract.list[subject_code]['손절가']:
                    contract.list[subject_code]['손절가'] = contract.list[subject_code]['체결가'] + ( 1*subject.info[subject_code]['단위'] ) #매수가보다 1틱 올려서 손절가 설정
            ########
               
            elif current_price <= contract.list[subject_code]['손절가']: 
                # 손절 청산
                log.info("손절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                return {'신규주문':True, '매도수구분':'신규매도', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
        
        elif contract.list[subject_code]['매도수구분'] == '신규매도':
            # 매도일때
            if current_price <= contract.list[subject_code]['익절가']: 
                if contract.list[subject_code]['계약타입'][contract.DRIBBLE] > 0:
                    # 드리블 수량이 남아있다면
                    if get_time(30) >= int(subject.info[subject_code]['마감시간']) and get_time(0) < int(subject.info[subject_code]['마감시간']):
                        log.info('마감시간 임박으로 드리블 불가. 모두 청산.')
                        return {'신규주문':True, '매도수구분':'신규매수', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
                    else:
                        log.info("드리블 목표 달성으로 익절가 수정.")
                        #contract.list[subject_code]['익절가'] = current_price - ( subject.info[subject_code]['주문내용']['익절틱'] * subject.info[subject_code]['단위'] )
                        contract.list[subject_code]['익절가'] = current_price - ( subject.info[subject_code]['단위'] )
                        contract.list[subject_code]['손절가'] = current_price + ( (subject.info[subject_code]['주문내용']['손절틱'] - 1) * subject.info[subject_code]['단위'] ) # 수수료 때문에 1틱 뺌
                        #contract.list[subject_code]['손절가'] = current_price + ( subject.info[subject_code]['단위'] ) # 수수료 때문에 1틱 뺌

                # 목표달성 청산
                if contract.list[subject_code]['계약타입'][contract.SAFE] > 0:
                    log.info("목표달성 청산으로 드리블 수량 제외하고 " + str(contract.list[subject_code]['계약타입'][contract.SAFE]) + "개 청산 요청.")
                    return {'신규주문':True, '매도수구분':'신규매수', '수량':contract.list[subject_code]['계약타입'][contract.SAFE]}

            ### 예를 들어 10틱 목표가인데 8틱까지 올라가면 손절가를 체결가 + 1 로 설정하여 -10틱 까지 가서 손절되는것을 막는다
            elif current_price <= contract.list[subject_code]['익절가'] + (int(subject.info[subject_code]['주문내용']['익절틱']*0.2)*subject.info[subject_code]['단위']):
                if contract.list[subject_code]['체결가'] < contract.list[subject_code]['손절가']:
                    contract.list[subject_code]['손절가'] = contract.list[subject_code]['체결가'] - ( 1*subject.info[subject_code]['단위'] ) #매수가보다 1틱 올려서 손절가 설정
            ########

            elif current_price >= contract.list[subject_code]['손절가']: 
                # 손절청산
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