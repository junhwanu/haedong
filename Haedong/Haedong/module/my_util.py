# -*- coding: utf-8 -*-
import subject, calc

def get_date_string_from_date_int(date):
    date = str(date)
    return date[4:6] + '-' + date[6:8] + ' ' + date[8:10] + ':' + date[10:12]

def get_start_index_of_trend(subject_code):
    start_index = calc.data[subject_code]['idx'] - calc.data[subject_code]['정배열연속틱'] + 1

    if start_index <= 0:
        return 0
    
    past_trend = calc.data[subject_code]['추세'][ start_index - 1 ]
    current_trend = calc.data[subject_code]['추세'][ -1 ]

    max = 0.0
    min = 99999.99
    point = start_index
    for idx in range(start_index - 1, 0, -1):
        if calc.data[subject_code]['추세'][idx] == None or calc.data[subject_code]['추세'][idx] != past_trend:
            break

        if current_trend == '상승세':
            if calc.data[subject_code]['현재가'][idx] < min:
                min = calc.data[subject_code]['현재가'][idx]
                point = idx
        elif current_trend == '하락세':
            if calc.data[subject_code]['현재가'][idx] > max:
                max = calc.data[subject_code]['현재가'][idx]
                point = idx
    
    return point

def chanege_past_trend(subject_code):
    start_index = calc.data[subject_code]['idx'] - calc.data[subject_code]['정배열연속틱'] + 1

    for idx in range(start_index - 1, 0, -1):
        if calc.data[subject_code]['추세'][idx] == None or calc.data[subject_code]['추세'][idx] == calc.data[subject_code]['추세'][-1]:
            break
        calc.data[subject_code]['추세'][idx] = calc.data[subject_code]['추세'][-1]

def get_trend_continuous_tick_count(subject_code):
    return calc.data[subject_code]['idx'] - get_start_index_of_trend(subject_code) + 1
