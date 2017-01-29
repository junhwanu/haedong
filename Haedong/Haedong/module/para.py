# -*- coding: utf-8 -*-
import contract, subject, log, calc, time

def is_it_OK(subject_code, current_price):
    if calc.data[subject_code]['idx'] < 100:
        return {'신규주문':False}
    if calc.data[subject_code]['idx'] == 100:
        subject.info[subject_code]['상태'] = '매매완료'

    if subject.info[subject_code]['상태'] != '중립대기':
        log.info('중립대기가 아니므로 매매 불가. 상태 : ' + subject.info[subject_code]['상태'])
        return {'신규주문':False}

    if calc.data[subject_code]['이동평균선'][30][-1] == None:
        log.info('이동평균선 미생성으로 매매 불가. 현재 이동평균선30 : ' + str(calc.data[subject_code]['이동평균선'][30][-1]))
        return {'신규주문':False}

    log.info('현재 flow : ' + subject.info[subject_code]['flow'])
    log.info('현재 sar : ' + str(subject.info[subject_code]['sar']))
    if subject.info[subject_code]['flow'] == '상향': 
        if current_price < subject.info[subject_code]['sar']:
            log.info('min 값 : ' + str( min(calc.data[subject_code]['이동평균선'][30][-1], subject.info[subject_code]['sar'] + subject.info[subject_code]['sar매매틱간격'] * subject.info[subject_code]['단위']) ))
            if min(calc.data[subject_code]['이동평균선'][30][-1], subject.info[subject_code]['sar'] + subject.info[subject_code]['sar매매틱간격'] * subject.info[subject_code]['단위']) <= current_price:
                pass
            else:
                log.info('min 값이 current_price보다 크므로 매매 불가.')
                return {'신규주문':False}
        else:
            if max(calc.data[subject_code]['이동평균선'][30][-1], subject.info[subject_code]['sar'] - subject.info[subject_code]['sar매매틱간격'] * subject.info[subject_code]['단위']) >= current_price:
                pass
            else:
                log.info('max 값이 current_price보다 작으므로 매매 불가.')
                return {'신규주문':False}
    elif subject.info[subject_code]['flow'] == '하향':
        if current_price > subject.info[subject_code]['sar']:
            log.info('max 값 : ' + str(max(calc.data[subject_code]['이동평균선'][30][-1], subject.info[subject_code]['sar'] - subject.info[subject_code]['sar매매틱간격'] * subject.info[subject_code]['단위'])))
            if max(calc.data[subject_code]['이동평균선'][30][-1], subject.info[subject_code]['sar'] - subject.info[subject_code]['sar매매틱간격'] * subject.info[subject_code]['단위']) >= current_price:
                pass
            else:
                log.info('max 값이 current_price보다 작으므로 매매 불가.')
                return {'신규주문':False}
        else:
            if min(calc.data[subject_code]['이동평균선'][30][-1], subject.info[subject_code]['sar'] + subject.info[subject_code]['sar매매틱간격'] * subject.info[subject_code]['단위']) <= current_price:
                pass
            else:
                log.info('min 값이 current_price보다 크므로 매매 불가.')
                return {'신규주문':False}

    contract_cnt = subject.info[subject_code]['신규매매수량']

    # 매도수구분 설정
    mesu_medo_type = None
    if subject.info[subject_code]['flow'] == '상향': 
        mesu_medo_type = '신규매수'
    elif subject.info[subject_code]['flow'] == '하향': 
        mesu_medo_type = '신규매도'

    profit_tick = 7

    order_contents = {'신규주문':True, '매도수구분':mesu_medo_type, '익절틱':profit_tick, '손절틱':profit_tick, '수량':contract_cnt}
    subject.info[subject_code]['주문내용'] = order_contents
    log.debug('para.is_it_OK() : 모든 구매조건 통과.')
    log.debug(order_contents)
    return order_contents

def is_it_sell(subject_code, current_price):
    if subject.info[subject_code]['flow'] == '상향':
        if current_price < subject.info[subject_code]['sar']:
            if contract.get_contract_count(subject_code) > 0:
                log.info('flow가 상향이고, 현재가가  sar 보다 작으므로 매도 시도')
                return {'신규주문':True, '매도수구분':'신규매도', '수량': contract.get_contract_count(subject_code)}
    elif subject.info[subject_code]['flow'] == '하향':
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
                        contract.list[subject_code]['익절가'] = current_price + ( subject.info[subject_code]['주문내용']['익절틱'] * subject.info[subject_code]['단위'] )
                        contract.list[subject_code]['손절가'] = current_price - ( (subject.info[subject_code]['주문내용']['손절틱'] - 1) * subject.info[subject_code]['단위'] ) # 수수료 때문에 1틱 뺌

                # 목표달성 청산
                if contract.list[subject_code]['계약타입'][contract.SAFE] > 0:
                    log.info("목표달성 청산으로 드리블 수량 제외하고 " + str(contract.list[subject_code]['계약타입'][contract.SAFE]) + "개 청산 요청.")
                    return {'신규주문':True, '매도수구분':'신규매도', '수량':contract.list[subject_code]['계약타입'][contract.SAFE]}
                
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
                        contract.list[subject_code]['익절가'] = current_price - ( subject.info[subject_code]['주문내용']['익절틱'] * subject.info[subject_code]['단위'] )
                        contract.list[subject_code]['손절가'] = current_price + ( (subject.info[subject_code]['주문내용']['손절틱'] - 1) * subject.info[subject_code]['단위'] ) # 수수료 때문에 1틱 뺌
                    
                # 목표달성 청산
                if contract.list[subject_code]['계약타입'][contract.SAFE] > 0:
                    log.info("목표달성 청산으로 드리블 수량 제외하고 " + str(contract.list[subject_code]['계약타입'][contract.SAFE]) + "개 청산 요청.")
                    return {'신규주문':True, '매도수구분':'신규매수', '수량':contract.list[subject_code]['계약타입'][contract.SAFE]}
                
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