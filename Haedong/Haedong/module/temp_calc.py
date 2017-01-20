# -*- coding: utf-8 -*-
import subject, contract, log
import numpy as np
import matplotlib.pyplot as plt

data = {}
data['?̵????ռ?'] = {}
data['?̵????ռ?']['?ϼ?'] = [5, 20, 30, 60, 100, 200, 300]
current_price = 0

def create_data(subject_code):
    data[subject_code] = {}
    
    data[subject_code]['idx'] = -1
    data[subject_code]['?̵????ռ?'] = {}

    for days in data['?̵????ռ?']['?ϼ?']:
        data[subject_code]['?̵????ռ?'][days] = np.array([])

    data[subject_code]['?ϸ?????ǥ'] = {}

    data[subject_code]['???簡'] = np.array([])
    data[subject_code]['????'] = np.array([])
    data[subject_code]['????'] = np.array([])

    data[subject_code]['???迭????ƽ'] = 0
    data[subject_code]['?߼?'] = np.array([])
    data[subject_code]['?׷???'] = {}

    plt.ion()
    data[subject_code]['?׷???']['???簡'] = plt.plot( data[subject_code]['???簡'] )[0]
    #data[subject_code]['?׷???']['?̵????ռ?'] = {}
    #for days in [30, 60, 100]:
    #    data[subject_code]['?׷???']['?̵????ռ?'][days] = plt.plot( data[subject_code]['?̵????ռ?'][days] )[0]

    plt.show()

def is_sorted(subject_code, lst):
    '''
    ?̵????ռ? ???迭 ???? Ȯ??

    params : 'CLG17', [5, 30, 60]
    '''

    if max(lst) - 1 > data[subject_code]['idx']:
        return '????'


    lst_real = []
    lst_tmp = []
    for days in lst:
        lst_real.append(data[subject_code]['?̵????ռ?'][days][ data[subject_code]['idx'] ])
    
    log.debug(lst_real)
    lst_tmp = lst_real[:]
    lst_tmp.sort()
    if lst_real == lst_tmp:
        return '?϶???'
    
    lst_tmp.reverse()
    if lst_real == lst_tmp:
        return '???¼?'

    return '????'

def push(subject_code, price):
    '''
    ĵ?? ?߰?
    '''
    current_price = round(float(price['???簡']), subject.info[subject_code]['?ڸ???'])
    highest_price = round(float(price['????']), subject.info[subject_code]['?ڸ???'])
    lowest_price = round(float(price['????']), subject.info[subject_code]['?ڸ???'])
    data[subject_code]['???簡'] = np.append(data[subject_code]['???簡'], current_price)
    data[subject_code]['????'] = np.append(data[subject_code]['????'], highest_price)
    data[subject_code]['????'] = np.append(data[subject_code]['????'], lowest_price)

    data[subject_code]['idx'] = data[subject_code]['idx'] + 1
    
    calc(subject_code)

    trend = is_sorted(subject_code, [30, 60, 100])
    data[subject_code]['?߼?'] = np.append(data[subject_code]['?߼?'], trend)

    if trend == '????':
        if data[subject_code]['???迭????ƽ'] > 0:
            log.info('?̵????ռ? ???迭 ????ƽ ?ʱ?ȭ.')
        data[subject_code]['???迭????ƽ'] = 0
    else:
        data[subject_code]['???迭????ƽ'] += 1
        log.info('?̵????ռ? ' + trend + ' ' + str(data[subject_code]['???迭????ƽ']) + 'ƽ')

    draw(subject_code)
       

def draw(subject_code):

    # set X value
    arr_range = list(range(0, data[subject_code]['???簡'].size))
    data[subject_code]['?׷???']['???簡'].set_xdata( arr_range )
    '''
    data[subject_code]['?׷???']['???簡'].set_xdata( 
        np.append( data[subject_code]['?׷???']['???簡'].get_xdata(), data[subject_code]['?׷???']['???簡'].get_xdata().size ) )
    '''
    '''
    for days in [30, 60, 100]:
        data[subject_code]['?׷???']['?̵????ռ?'][days].set_xdata( 
            np.append( data[subject_code]['?׷???']['?̵????ռ?'][days].get_xdata(),
                       data[subject_code]['?׷???']['?̵????ռ?'][days].get_xdata().size ) 
        )
    '''
    # set Y value
    data[subject_code]['?׷???']['???簡'].set_ydata( data[subject_code]['???簡'] )
    '''
    data[subject_code]['?׷???']['???簡'].set_ydata( 
        np.append( data[subject_code]['?׷???']['???簡'].get_ydata(), data[subject_code]['???簡'][ data[subject_code]['?׷???']['???簡'].get_ydata().size ] ) )
    '''
    '''
    for days in [30, 60, 100]:
        data[subject_code]['?׷???']['?̵????ռ?'][days].set_ydata( 
            np.append( data[subject_code]['?׷???']['?̵????ռ?'][days].get_ydata(), 
                       data[subject_code]['?̵????ռ?'][days][ data[subject_code]['?׷???']['?̵????ռ?'][days].get_ydata().size ] )
        )
    '''
    #plt.draw()
 

def refresh(subject_code, price):
    '''
    ???? ?ϼ????? ???? ĵ???? ???簡?? ?־? ?????? ĵ???? ?ִ°?ó?? ?????ؾ? ????... ???? ĵ???? ?????ؾ?????..
    '''
    current_price = round(float(price['???簡']), subject.info[subject_code]['?ڸ???'])
    highest_price = round(float(price['????']), subject.info[subject_code]['?ڸ???'])
    lowest_price = round(float(price['????']), subject.info[subject_code]['?ڸ???'])

    # ???? ?ۼ?

    calc()

def calc(subject_code):
    '''
    ???? ?׷??? ????
    '''
    calc_ma_line(subject_code)
    calc_ilmok_chart(subject_code)
    calc_linear_regression(subject_code)

def calc_ma_line(subject_code):
    '''
    ?̵????ռ? ????
    '''    
    for days in data['?̵????ռ?']['?ϼ?']:
        if data[subject_code]['idx'] >= days - 1:
            avg = sum( data[subject_code]['???簡'][ data[subject_code]['idx'] - days + 1 : data[subject_code]['idx'] + 1] ) / days    
            data[subject_code]['?̵????ռ?'][days] = np.append(data[subject_code]['?̵????ռ?'][days], round(float(avg), subject.info[subject_code]['?ڸ???']) )
        else:
            data[subject_code]['?̵????ռ?'][days] = np.append(data[subject_code]['?̵????ռ?'][days], None )
                

def calc_ilmok_chart(subject_code):
    '''
    ?ϸ?????ǥ ????
    '''

    pass

def calc_linear_regression(subject_code):
    '''
    ????ȸ?? ????
    '''
    pass



