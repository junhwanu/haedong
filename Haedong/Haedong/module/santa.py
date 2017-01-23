# -*- coding: utf-8 -*-
import contract, subject, log, calc, time

def is_it_OK(subject_code, current_price):
    '''
    이거 살까?
    '''

    # 종목 마감시간 확인
    current_time = time.localtime().tm_hour * 100 + time.localtime().tm_min
    if current_time + 30 >= int(subject.info[subject_code]['마감시간']):
        return {'신규주문':False}

    # 이평선 정렬확인
    if calc.data[subject_code]['정배열연속틱'] < subject.info[subject_code]['최소연속틱']:
        return {'신규주문':False}

    # 일목균형표 확인
    if calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '상승세':
        if calc.data[subject_code]['일목균형표']['선행스팬1'][ calc.data[subject_code]['idx'] ] > current_price and calc.data[subject_code]['일목균형표']['선행스팬2'][ calc.data[subject_code]['idx'] ] > current_price:
            return {'신규주문':False}

    elif calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '하락세':
        if calc.data[subject_code]['일목균형표']['선행스팬1'][ calc.data[subject_code]['idx'] ] < current_price and calc.data[subject_code]['일목균형표']['선행스팬2'][ calc.data[subject_code]['idx'] ] < current_price:
            return {'신규주문':False}

    # 추세선 터치여부 확인
    if subject.info[subject_code]['상태'] == '매매구간진입' and subject.info[subject_code]['매매구간누적캔들'] >= 1:
        pass
    else: return {'신규주문':False}
        
    # 추세선의 기울기가 추세와 같은지 확인
    if calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '상승세':
        if calc.data[subject_code]['추세선'][ calc.data[subject_code]['idx'] ] - calc.data[subject_code]['추세선'][ calc.data[subject_code]['idx'] - 1] < 0:
            return {'신규주문':False}

    elif calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '하락세':
        if calc.data[subject_code]['추세선'][ calc.data[subject_code]['idx'] ] - calc.data[subject_code]['추세선'][ calc.data[subject_code]['idx'] - 1] > 0:
            return {'신규주문':False}

    # 모든 조건 충족 시 현재 보유 계약 상태 확인해서 리턴

    # 초기에 계좌 잔고 저장해서, 몇개 살 수 있는지 확인해서 리턴
    contract_cnt = 2

    # 매도수구분 설정
    mesu_medo_type = None
    if calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '상승세':
        mesu_medo_type = '신규매수'
    elif calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '하락세':
        mesu_medo_type = '신규매도'

    return {'신규주문':True, '매도수구분':mesu_medo_type, '익절틱':10, '손절틱':10, '수량':contract_cnt}


def is_it_sell(subject_code, current_price):
    if contract.get_contract_count(subject_code) > 0:
        # 계약 보유중
        if contract.list[subject_code]['매도수구분'] == '신규매수':
            # 매수일때
            if current_price >= contract.list[subject_code]['익절가']: 
                # 목표달성 청산
                if contract.list[subject_code][contract.DRIBBLE] > 0:
                    # 드리블 수량이 남아있다면
                    contract.list[subject_code]['익절가'] = current_price + ( subject.info[subject_code]['주문내용']['익절틱'] * subject.info[subject_code]['단위'] )
                    contract.list[subject_code]['손절가'] = current_price - ( (subject.info[subject_code]['주문내용']['손절틱'] - 1) * subject.info[subject_code]['단위'] ) # 수수료 때문에 1틱 뺌

                return {'신규주문':True, '매도수구분':'신규매도', '수량':contract.list[subject_code][contract.SAFE]}

            elif current_price <= contract.list[subject_code]['손절가']: 
                # 손절 청산
                return {'신규주문':True, '매도수구분':'신규매도', '수량':contract.list[subject_code][contract.SAFE] + contract.list[subject_code][contract.DRIBBLE]}
        
        elif contract.list[subject_code]['매도수구분'] == '신규매도':
            # 매도일때
            if current_price <= contract.list[subject_code]['익절가']: 
                # 목표달성 청산
                if contract.list[subject_code][contract.DRIBBLE] > 0:
                    # 드리블 수량이 남아있다면
                    contract.list[subject_code]['익절가'] = current_price - ( subject.info[subject_code]['주문내용']['익절틱'] * subject.info[subject_code]['단위'] )
                    contract.list[subject_code]['손절가'] = current_price + ( (subject.info[subject_code]['주문내용']['손절틱'] - 1) * subject.info[subject_code]['단위'] ) # 수수료 때문에 1틱 뺌

                return {'신규주문':True, '매도수구분':'신규매수', '수량':contract.list[subject_code][contract.SAFE]}

            elif current_price >= contract.list[subject_code]['손절가']: 
                # 손절청산
                return {'신규주문':True, '매도수구분':'신규매수', '수량':contract.list[subject_code][contract.SAFE] + contract.list[subject_code][contract.DRIBBLE]}

    else: return {'신규주문':False}

def update_state_by_current_price(subject_code, current_price):
    if subject.info[subject_code]['상태'] == '중립대기':
        if calc.data[subject_code]['정배열연속틱'] >= subject.info[subject_code]['최소연속틱']:
            if calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '상승세':
                if calc.data[subject_code]['매매선'][ calc.data[subject_code]['idx'] ] >= current_price:
                    subject.info[subject_code]['상태'] = '매매선터치'
            elif calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '하락세':
                if calc.data[subject_code]['매매선'][ calc.data[subject_code]['idx'] ] <= current_price:
                    subject.info[subject_code]['상태'] = '매매선터치'
                

def update_state_by_current_candle(subject_code, price):
    current_price = float(price['현재가'])
    start_price = float(price['시가'])

    if subject.info[subject_code]['상태'] == '매매선터치' or subject.info[subject_code]['상태'] == '매매구간진입' :
        if calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '상승세':
            if current_price >= calc.data[subject_code]['매매선'][ calc.data[subject_code]['idx'] ]:
                if start_price < calc.data[subject_code]['매매선'][ calc.data[subject_code]['idx'] ]:
                    subject.info[subject_code]['상태'] == '매매선터치'
                    subject.info[subject_code]['매매구간누적캔들'] = 0
                else:
                    subject.info[subject_code]['상태'] == '매매구간진입'
                    subject.info[subject_code]['매매구간누적캔들'] += 1
        elif calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '하락세':
            if current_price <= calc.data[subject_code]['매매선'][ calc.data[subject_code]['idx'] ]:
                if start_price < calc.data[subject_code]['매매선'][ calc.data[subject_code]['idx'] ]:
                    subject.info[subject_code]['상태'] == '매매선터치'
                    subject.info[subject_code]['매매구간누적캔들'] = 0
                else:
                    subject.info[subject_code]['상태'] == '매매구간진입'
                    subject.info[subject_code]['매매구간누적캔들'] += 1