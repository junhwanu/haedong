# -*- coding: utf-8 -*-
import contract, subject, log, calc, time, my_util
import log_result as res
import define as d

previous_profit = 0
temp_index = 0

first_chungsan = 77
first_chungsan_dribble = 5

second_chungsan = 300
second_chungsan_dribble = 15

def is_it_OK(subject_code, current_price):
    global previous_profit
    global temp_index
    gap_between_5ma_current_price = 3 # 전전 5이평선과 틱 차이로 급격하게 변할시 바로 매매


    #print(get_time(0,subject_code))
    profit_tick = subject.info[subject_code]['익절틱']
    sonjal_tick = subject.info[subject_code]['손절틱']
    mesu_medo_type = None
    false = {'신규주문': False}

    if calc.data[subject_code]['idx'] < 3000:
        return false
    
    if subject.info[subject_code]['상태'] == '매수중' or subject.info[subject_code]['상태'] == '매도중' or subject.info[subject_code]['상태'] == '청산시도중' or subject.info[subject_code]['상태'] == '매매시도중' or subject.info[subject_code]['상태'] == '중립대기':
        log.debug('신규 주문 가능상태가 아니므로 매매 불가. 상태 : ' + subject.info[subject_code]['상태'])
        return false
    
    if subject.info[subject_code]['상태'] != '매수대기' and subject.info[subject_code]['상태'] != '매도대기':  
        log.debug("종목코드(" + subject_code + ")  현재 Flow : " + subject.info[subject_code]['flow'] + " / SAR : " + str(subject.info[subject_code]['sar']) + " / 추세 : " + my_util.is_sorted(subject_code))
        if subject.info[subject_code]['flow'] == '상향': 
            if current_price < subject.info[subject_code]['sar'] and my_util.is_sorted(subject_code) == '하락세':
                mesu_medo_type = '신규매도'
                log.debug("종목코드(" + subject_code + ") 하향 반전.")
                
                if previous_profit > 500:
                    print("이전 이익이 500 이상으로 매매포기")
                    temp_index = calc.data[subject_code]['idx']
                    subject.info[subject_code]['상태'] = '중립대기'
                    previous_profit = 0
                    return false
                
                if calc.data[subject_code]['이동평균선'][5][-1] - current_price > subject.info[subject_code]['단위']* gap_between_5ma_current_price:
                    print("급격히 하락하여 바로 매도주문 들어갑니다.")
                    pass
                else:
                    subject.info[subject_code]['매도대기목표가'] = current_price + subject.info[subject_code]['단위']*subject.info[subject_code]['sar매매틱간격']
                    subject.info[subject_code]['상태'] = '매도대기'
                    print("천천히 하락하여 매도 대기 상태로 변경")
                    return false
                
            elif calc.data[subject_code]['플로우'][-2] =='하향' and my_util.is_sorted(subject_code) == '상승세':
                mesu_medo_type = '신규매수'
                log.debug("종목코드(" + subject_code + ") 상향 반전.")

                if previous_profit > 500:
                    print("이전 이익이 500 이상으로 매매포기")
                    temp_index = calc.data[subject_code]['idx']
                    subject.info[subject_code]['상태'] = '중립대기'
                    previous_profit = 0
                    return false

                if current_price - calc.data[subject_code]['이동평균선'][5][-1] > subject.info[subject_code]['단위']* gap_between_5ma_current_price :
                    print("급격히 상승하여 바로 매수주문 들어갑니다.")
                    pass
                else:
                    subject.info[subject_code]['매도대기목표가'] = current_price - subject.info[subject_code]['단위']*subject.info[subject_code]['sar매매틱간격']
                    subject.info[subject_code]['상태'] = '매수대기'
                    print("천천히 상승하여 매수 대기 상태로 변경")
                    return false
               
            else: return false
        elif subject.info[subject_code]['flow'] == '하향':
            if current_price > subject.info[subject_code]['sar'] and my_util.is_sorted(subject_code) == '상승세':
                mesu_medo_type = '신규매수'
                log.debug("종목코드(" + subject_code + ") 상향 반전.")

                if previous_profit > 500:
                    print("이전 이익이 500 이상으로 매매포기")
                    temp_index = calc.data[subject_code]['idx']
                    subject.info[subject_code]['상태'] = '중립대기'
                    previous_profit = 0
                    return false
                
                if current_price - calc.data[subject_code]['이동평균선'][5][-1] > subject.info[subject_code]['단위']* gap_between_5ma_current_price:
                    print("급격히 상승하여 바로 매수주문 들어갑니다.")
                    pass
                else:
                    subject.info[subject_code]['매도대기목표가'] = current_price - subject.info[subject_code]['단위']*subject.info[subject_code]['sar매매틱간격']
                    subject.info[subject_code]['상태'] = '매수대기'
                    print("천천히 상승하여 매수 대기 상태로 변경")
                    return false
                
            elif calc.data[subject_code]['플로우'][-2] =='상향' and my_util.is_sorted(subject_code) == '하락세':
                mesu_medo_type = '신규매도'
                log.debug("종목코드(" + subject_code + ") 하향 반전.")
                
                if previous_profit > 500:
                    print("이전 이익이 500 이상으로 매매포기")
                    temp_index = calc.data[subject_code]['idx']
                    subject.info[subject_code]['상태'] = '중립대기'
                    previous_profit = 0
                    return false
                
                if calc.data[subject_code]['이동평균선'][5][-1] - current_price > subject.info[subject_code]['단위']* gap_between_5ma_current_price:
                    print("급격히 하락하여 바로 매도주문 들어갑니다.")
                    pass
                else:
                    subject.info[subject_code]['매도대기목표가'] = current_price + subject.info[subject_code]['단위']*subject.info[subject_code]['sar매매틱간격']
                    subject.info[subject_code]['상태'] = '매도대기'
                    print("천천히 하락하여 매도 대기 상태로 변경")
                    return false
                
            else: return false
        else: return false
    
   
    
    
    
    elif subject.info[subject_code]['상태'] == '매수대기' or subject.info[subject_code]['상태'] == '매도대기':
        if subject.info[subject_code]['상태'] == '매수대기':
            if current_price < subject.info[subject_code]['매수대기목표가']:
                mesu_medo_type = '신규매수'
                print("%s 종목 매수대기목표가 터치하여 매수, 매수대기목표가:%s" % (subject_code,subject.info[subject_code]['매수대기목표가']))
            else: return false

        elif subject.info[subject_code]['상태'] == '매도대기':
            if current_price > subject.info[subject_code]['매도대기목표가']:
                mesu_medo_type = '신규매도'
                print("%s 종목 매도대기목표가 터치하여 매도, 매도대기목표가:%s" % (subject_code,subject.info[subject_code]['매도대기목표가']))
            else: return false
        else: return false
    else: return false

    '''        
    if temp_index == 0:
        temp_index = calc.data[subject_code]['idx']
    else:
        if calc.data[subject_code]['idx'] - temp_index > 2:
            if previous_profit > 500:
                print("이전 이익이 500 이상으로 매매포기")
                temp_index = calc.data[subject_code]['idx']
                subject.info[subject_code]['상태'] = '중립대기'

                return false
        else:
            if previous_profit != 0:
                previous_profit = 0
                print("ddd")
                return false 
    '''
        


    if get_time(0,subject_code) > 2100 and get_time(0,subject_code) < 2300:
        print("21~23 시 사이라 매매 포기 합니다.")
        #subject.info[subject_code]['상태'] = '매매완료'
        subject.info[subject_code]['상태'] = '중립대기'
        return false
    
    
    
    
    
    
    
    
    

        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    if d.get_mode() == d.REAL:
        contract_cnt = int(contract.my_deposit / subject.info[subject_code]['위탁증거금'])
    else:
        contract_cnt = 2
    
    contract_cnt = 2
    log.debug("종목코드(" + subject_code + ") 신규 매매 계약 수 " + str(contract_cnt))
    
    if contract_cnt == 0: return false
   

    subject.info[subject_code]['반전시현재가'] = current_price
    print("반전시현재가는 %s 입니다." % current_price)
    
    order_contents = {'신규주문':True, '매도수구분':mesu_medo_type, '익절틱':profit_tick, '손절틱':sonjal_tick, '수량':contract_cnt}
    subject.info[subject_code]['주문내용'] = order_contents
    log.debug('para.is_it_OK() : 모든 구매조건 통과.')
    log.debug(order_contents)
    return order_contents

def is_it_sell(subject_code, current_price):
    index = calc.data[subject_code]['idx']
    global first_chungsan, first_chungsan_dribble, second_chungsan, second_chungsan_dribble

    sar_before_reverse_tic = 1
    
    log.debug("종목코드(" + subject_code + ") is_it_sell() 진입.")
    log.debug("종목코드(" + subject_code + ") 현재 Flow : " + subject.info[subject_code]['flow'] + " / SAR : " + str(subject.info[subject_code]['sar']))
    if contract.get_contract_count(subject_code) > 0:
        # 계약 보유중
        log.debug("종목코드(" + subject_code + ") is_it_sell() / 보유 계약 : " + str(contract.get_contract_count(subject_code)))
        if contract.list[subject_code]['매도수구분'] == '신규매수':
            # 매수일때
            if current_price <= contract.list[subject_code]['손절가']:
                res.info("손절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                if contract.get_contract_count(subject_code) == subject.info[subject_code]['신규매매수량']:
                    contract.list[subject_code]['손절가'] = current_price - subject.info[subject_code]['익절틱'] * subject.info[subject_code]['단위']
                    return {'신규주문':True, '매도수구분':'신규매도', '수량':int((contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])/2)}
                else:
                    return {'신규주문':True, '매도수구분':'신규매도', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
            elif calc.data[subject_code]['플로우'][-1] == '상향' and (subject.info[subject_code]['sar'] + sar_before_reverse_tic*subject.info[subject_code]['단위']) > current_price:
                res.info("하향 반전되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                return {'신규주문':True, '매도수구분':'신규매도', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
            elif current_price > contract.list[subject_code]['익절가']:
                contract.list[subject_code]['익절가'] = current_price + subject.info[subject_code]['익절틱'] * subject.info[subject_code]['단위']
                contract.list[subject_code]['손절가'] = current_price - subject.info[subject_code]['익절틱'] * subject.info[subject_code]['단위']
                log.debug("종목코드(" + subject_code + ") 익절가 갱신.")
            elif current_price - subject.info[subject_code]['반전시현재가'] >= first_chungsan * subject.info[subject_code]['단위'] and subject.info[subject_code]['반전시현재가'] != 0 and contract.get_contract_count(subject_code) == subject.info[subject_code]['신규매매수량']:
                if contract.list[subject_code]['손절가'] < current_price - first_chungsan_dribble*subject.info[subject_code]['단위']:
                    contract.list[subject_code]['손절가'] = current_price - first_chungsan_dribble*subject.info[subject_code]['단위']
                    res.info("1차 청산 드리블 중 %s" % contract.list[subject_code]['손절가'])
            elif current_price - subject.info[subject_code]['반전시현재가'] >= second_chungsan * subject.info[subject_code]['단위'] and subject.info[subject_code]['반전시현재가'] != 0 and contract.get_contract_count(subject_code) == int(subject.info[subject_code]['신규매매수량'] - int(subject.info[subject_code]['신규매매수량']/2)):
                if contract.list[subject_code]['손절가'] < current_price - second_chungsan_dribble*subject.info[subject_code]['단위']:
                    contract.list[subject_code]['손절가'] = current_price - second_chungsan_dribble*subject.info[subject_code]['단위']
                    res.info("2차 청산 드리블 중 %s" % contract.list[subject_code]['손절가'])
                #return {'신규주문':True, '매도수구분':'신규매도', '수량':int((contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])/2)}
        elif contract.list[subject_code]['매도수구분'] == '신규매도':
            # 매도일때
            if current_price >= contract.list[subject_code]['손절가']:
                res.info("손절가가 되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                if contract.get_contract_count(subject_code) == subject.info[subject_code]['신규매매수량']:
                    contract.list[subject_code]['손절가'] = current_price + subject.info[subject_code]['익절틱'] * subject.info[subject_code]['단위']
                    return {'신규주문':True, '매도수구분':'신규매수', '수량':int((contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])/2)}
                else:
                    return {'신규주문':True, '매도수구분':'신규매수', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
            elif calc.data[subject_code]['플로우'][-1] == '하향' and (subject.info[subject_code]['sar'] - sar_before_reverse_tic*subject.info[subject_code]['단위']) < current_price:
                res.info("상향 반전되어 " + str(contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]) + "개 청산 요청.")
                return {'신규주문':True, '매도수구분':'신규매수', '수량':contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE]}
            elif current_price < contract.list[subject_code]['익절가']:
                contract.list[subject_code]['익절가'] = current_price - subject.info[subject_code]['익절틱'] * subject.info[subject_code]['단위']
                contract.list[subject_code]['손절가'] = current_price + subject.info[subject_code]['익절틱'] * subject.info[subject_code]['단위']
                log.debug("종목코드(" + subject_code + ") 익절가 갱신.")
            elif (subject.info[subject_code]['반전시현재가'] - current_price) >= first_chungsan * subject.info[subject_code]['단위'] and subject.info[subject_code]['반전시현재가'] != 0 and contract.get_contract_count(subject_code) == subject.info[subject_code]['신규매매수량']: #int(contract.get_contract_count(subject_code) / 2) > 0:
                if contract.list[subject_code]['손절가'] > current_price + first_chungsan_dribble*subject.info[subject_code]['단위']:
                    contract.list[subject_code]['손절가'] = current_price + first_chungsan_dribble*subject.info[subject_code]['단위']
                    res.info("1차 청산 드리블 중 %s" % contract.list[subject_code]['손절가'])
            elif (subject.info[subject_code]['반전시현재가'] - current_price) >= second_chungsan * subject.info[subject_code]['단위'] and subject.info[subject_code]['반전시현재가'] != 0 and contract.get_contract_count(subject_code) == int(subject.info[subject_code]['신규매매수량'] - int(subject.info[subject_code]['신규매매수량']/2)): 
                if contract.list[subject_code]['손절가'] > current_price + second_chungsan_dribble*subject.info[subject_code]['단위']:
                    contract.list[subject_code]['손절가'] = current_price + second_chungsan_dribble*subject.info[subject_code]['단위']
                    res.info("2차 청산 드리블 중 %s" % contract.list[subject_code]['손절가'])
                #return {'신규주문':True, '매도수구분':'신규매수', '수량':int((contract.list[subject_code]['계약타입'][contract.SAFE] + contract.list[subject_code]['계약타입'][contract.DRIBBLE])/2)}
            
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
        #print(calc.data[subject_code]['체결시간'][-1])
        current_hour = int(str(calc.data[subject_code]['체결시간'][-1])[8:10])
        current_min = int(str(calc.data[subject_code]['체결시간'][-1])[10:12])
        current_min += add_min
        if current_min >= 60:
            current_hour += 1
            current_min -= 60
    
        #print(current_hour)
        #print(current_min)
        current_time = current_hour*100 + current_min
        
        current_time = int(str(calc.data[subject_code]['체결시간'][-1])[8:12])
        
    return current_time