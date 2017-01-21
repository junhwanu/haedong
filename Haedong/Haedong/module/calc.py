# -*- coding: utf-8 -*-
import subject, contract, log
import matplotlib.pyplot as plt
from scipy import stats

data = {}
data['이동평균선'] = {}
data['이동평균선']['일수'] = [5, 20, 60, 120, 200, 300]
figure = {}
figure_count = 0

def create_data(subject_code):
    global figure_count
    data[subject_code] = {}
    
    data[subject_code]['idx'] = -1
    data[subject_code]['이동평균선'] = {}

    for days in data['이동평균선']['일수']:
        data[subject_code]['이동평균선'][days] = []

    data[subject_code]['일목균형표'] = {}
    data[subject_code]['일목균형표']['전환선'] = []
    data[subject_code]['일목균형표']['기준선'] = []
    data[subject_code]['일목균형표']['선행스팬1'] = []
    data[subject_code]['일목균형표']['선행스팬2'] = []
    for index in range(0,26):
        data[subject_code]['일목균형표']['선행스팬1'].append(None)
        data[subject_code]['일목균형표']['선행스팬2'].append(None)

    data[subject_code]['현재가'] = []
    data[subject_code]['고가'] = []
    data[subject_code]['저가'] = []

    data[subject_code]['정배열연속틱'] = 0
    data[subject_code]['추세'] = []
    data[subject_code]['추세선'] = []
    data[subject_code]['매매선'] = []
    data[subject_code]['그래프'] = {}
    
    
    figure[subject_code] = plt.figure(figure_count)
    figure_count = figure_count + 1
    subplot = figure[subject_code].add_subplot(111) 

    figure[subject_code].suptitle(subject_code, size=16)
    data[subject_code]['그래프']['서브플롯'] = subplot
    
    data[subject_code]['그래프']['최근가'] = None
    data[subject_code]['그래프']['현재가'] = None
    data[subject_code]['그래프']['추세선'] = None
    data[subject_code]['그래프']['매매선'] = None
    data[subject_code]['그래프']['이동평균선'] = {}
    for days in subject.info[subject_code]['이동평균선']:
        data[subject_code]['그래프']['이동평균선'][days] = None
    data[subject_code]['그래프']['일목균형표'] = {}
    data[subject_code]['그래프']['일목균형표']['전환선'] = []
    data[subject_code]['그래프']['일목균형표']['기준선'] = []
    data[subject_code]['그래프']['일목균형표']['선행스팬1'] = []
    data[subject_code]['그래프']['일목균형표']['선행스팬2'] = []
    
    plt.ion()
    for i in range(1,250):
        if i % 10 != 0:
            subplot.axvline(x=i, color='silver', linestyle='-')
        else:
            subplot.axvline(x=i, color='dimgrey', linestyle='-')
    plt.show()



def is_sorted(subject_code, lst):
    '''
    이동평균선 정배열 여부 확인

    params : 'CLG17', [5, 30, 60]
    '''

    if max(lst) - 1 > data[subject_code]['idx']:
        return '모름'


    lst_real = []
    lst_tmp = []
    for days in lst:
        lst_real.append(data[subject_code]['이동평균선'][days][ data[subject_code]['idx'] ])
    
    log.debug(lst_real)
    lst_tmp = lst_real[:]
    lst_tmp.sort()
    if lst_real == lst_tmp:
        return '하락세'
    
    lst_tmp.reverse()
    if lst_real == lst_tmp:
        return '상승세'

    return '모름'

def push(subject_code, price):
    '''
    캔들 추가
    '''
    '''
    current_price = round(float(price['현재가']), subject.info[subject_code]['자릿수'])
    highest_price = round(float(price['고가']), subject.info[subject_code]['자릿수'])
    lowest_price = round(float(price['저가']), subject.info[subject_code]['자릿수'])
    '''
    current_price = float(price['현재가'])
    highest_price = float(price['고가'])
    lowest_price = float(price['저가'])
    data[subject_code]['현재가'].append(current_price)
    data[subject_code]['고가'].append(highest_price)
    data[subject_code]['저가'].append(lowest_price)

    data[subject_code]['idx'] = data[subject_code]['idx'] + 1
    
    calc(subject_code)

    #draw(subject_code)
    if data[subject_code]['idx'] > 595:
        show(subject_code)
     
def show(subject_code):
    graph_width_tick_cnt = 200
    line_range = get_line_range(subject_code)
    if line_range > graph_width_tick_cnt:
        line_range = graph_width_tick_cnt

    subplot = data[subject_code]['그래프']['서브플롯']
    
    remove_line(subject_code, data[subject_code]['그래프']['현재가'])
    data[subject_code]['그래프']['현재가'] = subplot.plot(data[subject_code]['현재가'][ len(data[subject_code]['현재가']) - graph_width_tick_cnt: len(data[subject_code]['현재가']) ], color='black', label='Closing Price', linewidth=2)[0]
    remove_line(subject_code, data[subject_code]['그래프']['추세선'])
    data[subject_code]['그래프']['추세선'] = subplot.plot(list(range(graph_width_tick_cnt - line_range, graph_width_tick_cnt+1)), data[subject_code]['추세선'][ len(data[subject_code]['추세선']) - line_range - 1: len(data[subject_code]['추세선']) ], color='coral', label='Trend Line', linewidth=2)[0]
    remove_line(subject_code, data[subject_code]['그래프']['매매선'])
    data[subject_code]['그래프']['매매선'] = subplot.plot(list(range(graph_width_tick_cnt - line_range, graph_width_tick_cnt+1)), data[subject_code]['매매선'][ len(data[subject_code]['매매선']) - line_range - 1: len(data[subject_code]['매매선']) ], color='m', label='Trade Line', linewidth=2)[0]
    #data[subject_code]['그래프']['매매선'] = subplot.plot(list(range(graph_width_tick_cnt - line_range, graph_width_tick_cnt+1)), data[subject_code]['매매선'][ len(data[subject_code]['매매선']) - line_range - 1: len(data[subject_code]['매매선']) ], linewidth=2)[0]
    remove_line(subject_code, data[subject_code]['그래프']['일목균형표']['선행스팬1'])
    data[subject_code]['그래프']['일목균형표']['선행스팬1'] = subplot.plot(data[subject_code]['일목균형표']['선행스팬1'][ len(data[subject_code]['일목균형표']['선행스팬1']) - graph_width_tick_cnt -26: len(data[subject_code]['일목균형표']['선행스팬1']) ], color='orange', label='Span1', linewidth=1.5)[0]
    remove_line(subject_code, data[subject_code]['그래프']['일목균형표']['선행스팬2'])
    data[subject_code]['그래프']['일목균형표']['선행스팬2'] = subplot.plot(data[subject_code]['일목균형표']['선행스팬2'][ len(data[subject_code]['일목균형표']['선행스팬2']) - graph_width_tick_cnt -26: len(data[subject_code]['일목균형표']['선행스팬2']) ], color='royalblue', label='Span2', linewidth=1.5)[0]

    list_color = ['red', 'green', 'blue', 'm', 'lightpink']
    color_idx = 0
    for days in subject.info[subject_code]['이동평균선']:
        remove_line(subject_code, data[subject_code]['그래프']['이동평균선'][days])
        data[subject_code]['그래프']['이동평균선'][days] = subplot.plot(data[subject_code]['이동평균선'][days][ len(data[subject_code]['이동평균선'][days]) - graph_width_tick_cnt: len(data[subject_code]['이동평균선'][days]) ], color=list_color[color_idx], label='MA' + str(days), linewidth=2)[0]
        color_idx += 1
    
    plt.legend(loc='best')
    plt.show()  

def show_current_price(subject_code, current_price):
    subplot = data[subject_code]['그래프']['서브플롯']
    remove_line(subject_code, data[subject_code]['그래프']['최근가'])
    data[subject_code]['그래프']['최근가'] = subplot.axhline(y=round(float(current_price), subject.info[subject_code]['자릿수']), color='r', linestyle='-', label='Current Price')
    
    plt.legend(loc='best')
    plt.show()

def remove_line(subject_code, line):
    for c in data[subject_code]['그래프']['서브플롯'].lines:
        if id(c) == id(line):
          c.remove()

def draw(subject_code):

    # set X value
    arr_range = list(range(0, len(data[subject_code]['현재가'])))
    data[subject_code]['그래프']['현재가'].set_xdata( arr_range )
    '''
    data[subject_code]['그래프']['현재가'].set_xdata( 
        np.append( data[subject_code]['그래프']['현재가'].get_xdata(), data[subject_code]['그래프']['현재가'].get_xdata().size ) )
    '''
    '''
    for days in subject.info[subject_code]['이동평균선']:
        data[subject_code]['그래프']['이동평균선'][days].set_xdata( 
            np.append( data[subject_code]['그래프']['이동평균선'][days].get_xdata(),
                       data[subject_code]['그래프']['이동평균선'][days].get_xdata().size ) 
        )
    '''
    # set Y value
    data[subject_code]['그래프']['현재가'].set_ydata( data[subject_code]['현재가'] )
    '''
    data[subject_code]['그래프']['현재가'].set_ydata( 
        np.append( data[subject_code]['그래프']['현재가'].get_ydata(), data[subject_code]['현재가'][ data[subject_code]['그래프']['현재가'].get_ydata().size ] ) )
    '''
    '''
    for days in subject.info[subject_code]['이동평균선']:
        data[subject_code]['그래프']['이동평균선'][days].set_ydata( 
            np.append( data[subject_code]['그래프']['이동평균선'][days].get_ydata(), 
                       data[subject_code]['이동평균선'][days][ data[subject_code]['그래프']['이동평균선'][days].get_ydata().size ] )
        )
    '''
    #plt.draw()
 

def refresh(subject_code, price):
    '''
    아직 완성되지 않은 캔들의 현재가를 넣어 마지막 캔들이 있는것처럼 계산해야 할지... 현재 캔들은 제외해야할지..
    '''
    current_price = round(float(price['현재가']), subject.info[subject_code]['자릿수'])
    highest_price = round(float(price['고가']), subject.info[subject_code]['자릿수'])
    lowest_price = round(float(price['저가']), subject.info[subject_code]['자릿수'])

    # 로직 작성

    calc(subject_code)

def calc(subject_code):
    '''
    각종 그래프 계산
    '''
    calc_ma_line(subject_code)
    
    trend = is_sorted(subject_code, subject.info[subject_code]['이동평균선'])
    data[subject_code]['추세'].append(trend)

    if trend != data[subject_code]['추세'][ data[subject_code]['idx']-1 ]:
        if data[subject_code]['정배열연속틱'] > 0:
            log.info('이동평균선 정배열 연속틱 초기화.')
        data[subject_code]['정배열연속틱'] = 1
    else:
        data[subject_code]['정배열연속틱'] += 1
        log.info('이동평균선 ' + trend + ' ' + str(data[subject_code]['정배열연속틱']) + '틱')

    calc_ilmok_chart(subject_code)
    calc_linear_regression(subject_code)

def calc_ma_line(subject_code):
    '''
    이동평균선 계산
    '''    
    for days in data['이동평균선']['일수']:
        if data[subject_code]['idx'] >= days - 1:
            avg = sum( data[subject_code]['현재가'][ data[subject_code]['idx'] - days + 1 : data[subject_code]['idx'] + 1] ) / days    
            #data[subject_code]['이동평균선'][days].append(round(float(avg), subject.info[subject_code]['자릿수']))
            data[subject_code]['이동평균선'][days].append(avg)
        else:
            data[subject_code]['이동평균선'][days].append(None)
                

def calc_ilmok_chart(subject_code):
    '''
    일목균형표 계산
    '''
    if data[subject_code]['idx'] < 9:
        data[subject_code]['일목균형표']['전환선'].append(None)
    else:
        data[subject_code]['일목균형표']['전환선'].append( (max( data[subject_code]['현재가'][data[subject_code]['idx'] - 9 : data[subject_code]['idx']] ) + min(  data[subject_code]['현재가'][data[subject_code]['idx'] - 9 : data[subject_code]['idx']] )) / 2)

    if data[subject_code]['idx'] < 26:
        data[subject_code]['일목균형표']['기준선'].append(None)
    else:
        data[subject_code]['일목균형표']['기준선'].append( (max( data[subject_code]['현재가'][data[subject_code]['idx'] - 26 : data[subject_code]['idx']] ) + min(  data[subject_code]['현재가'][data[subject_code]['idx'] - 26 : data[subject_code]['idx']] )) / 2)

    if data[subject_code]['idx'] >= 26:
        data[subject_code]['일목균형표']['선행스팬1'].append( (data[subject_code]['일목균형표']['전환선'][data[subject_code]['idx']] + data[subject_code]['일목균형표']['기준선'][data[subject_code]['idx']]) / 2)

    if data[subject_code]['idx'] >= 52:
        data[subject_code]['일목균형표']['선행스팬2'].append( (max( data[subject_code]['현재가'][data[subject_code]['idx'] - 52 : data[subject_code]['idx']] ) + min(  data[subject_code]['현재가'][data[subject_code]['idx'] - 52 : data[subject_code]['idx']] )) / 2)

def calc_linear_regression(subject_code):
    '''
    직선회기 계산
    '''
    data[subject_code]['추세선'].append(None)
    data[subject_code]['매매선'].append(None)
    line_range = get_line_range(subject_code)
    
    if data[subject_code]['idx'] <= line_range:
        return
    
    result = stats.linregress(list(range( 0, line_range + 1 )), data[subject_code]['현재가'][ len(data[subject_code]['현재가']) - line_range - 1: len(data[subject_code]['현재가']) ])

    _x = 0
    for idx in range(data[subject_code]['idx'] - line_range, data[subject_code]['idx']):
        data[subject_code]['추세선'][idx] = result.slope * _x + result.intercept
        _x+=1

    # 데이터와의 차 구함
    max = get_max_deifference(subject_code)
    
    diff = max * 0.4

    for idx in range(data[subject_code]['idx'] - line_range, data[subject_code]['idx']):
        if data[subject_code]['추세'][ data[subject_code]['idx'] - 1] == '상승세':
            data[subject_code]['매매선'][idx] = data[subject_code]['추세선'][idx] - diff
        elif data[subject_code]['추세'][ data[subject_code]['idx'] - 1] == '하락세':
            data[subject_code]['매매선'][idx] = data[subject_code]['추세선'][idx] + diff
    

def get_line_range(subject_code):
    line_range = data[subject_code]['정배열연속틱']
    if line_range < 10:
        line_range = 10

    return line_range

def get_max_deifference(subject_code):
    '''
    추세선과 실제 데이터의 차이 중 가장 큰 값을 리턴한다.
    '''
    
    max = 0
    line_range = get_line_range(subject_code)
    for idx in range(data[subject_code]['idx'] - line_range, data[subject_code]['idx']):
        if data[subject_code]['추세'][idx] == '상승세':
            if data[subject_code]['추세선'][idx] >= data[subject_code]['현재가'][idx] and abs(data[subject_code]['추세선'][idx] - data[subject_code]['현재가'][idx]) > max:
                max = abs(data[subject_code]['추세선'][idx] - data[subject_code]['현재가'][idx])
        elif data[subject_code]['추세'][idx] == '하락세':
            if data[subject_code]['추세선'][idx] <= data[subject_code]['현재가'][idx] and abs(data[subject_code]['추세선'][idx] - data[subject_code]['현재가'][idx]) > max:
                max = abs(data[subject_code]['추세선'][idx] - data[subject_code]['현재가'][idx])
    return max