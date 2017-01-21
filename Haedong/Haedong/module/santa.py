# -*- coding: utf-8 -*-
import contract, subject, log, calc

def is_it_OK(subject_code, price):
    '''
    이거 살까?
    '''

    # 종목 마감시간 확인

    # 이평선 정렬확인
    if calc.data[subject_code]['정배열연속틱'] < subject.info[subject_code]['최소연속일']:
        return {'신규주문':False}

    # 일목균형표 확인
    if calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '상승세':
        if calc.data[subject_code]['일목균형표']['선행스팬1'] > price and calc.data[subject_code]['일목균형표']['선행스팬2'] > price:
            return {'신규주문':False}

    if calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '하락세':
        if calc.data[subject_code]['일목균형표']['선행스팬1'] < price and calc.data[subject_code]['일목균형표']['선행스팬2'] < price:
            return {'신규주문':False}

    # 추세선 확인
        
    # 추세선의 기울기가 추세와 같은지 확인
    if calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '상승세':
        if calc.data[subject_code]['추세선'][ calc.data[subject_code]['idx'] ] - calc.data[subject_code]['추세선'][ calc.data[subject_code]['idx'] - 1] < 0:
            return {'신규주문':False}

    if calc.data[subject_code]['추세'][ calc.data[subject_code]['idx'] ] == '하락세':
        if calc.data[subject_code]['추세선'][ calc.data[subject_code]['idx'] ] - calc.data[subject_code]['추세선'][ calc.data[subject_code]['idx'] - 1] > 0:
            return {'신규주문':False}

    # 모든 조건 충족 시 현재 보유 계약 상태 확인해서 리턴

    # 초기에 계좌 잔고 저장해서, 몇개 살 수 있는지 확인해서 리턴

    return {'신규주문':True, '매도수구분':'매수', '목표틱':10, '손절틱':10, '계약타입':contract.DRIBBLE}

