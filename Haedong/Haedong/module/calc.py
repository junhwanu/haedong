# -*- coding: utf-8 -*-
import subject, contract, log
import matplotlib.pyplot as plt
from scipy import stats
import log_result as res
import math

data = {}
data['이동평균선'] = {}
data['이동평균선']['일수'] = [5, 20, 30, 60, 100, 120, 200, 300]
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
    data[subject_code]['시가'] = []
    data[subject_code]['고가'] = []
    data[subject_code]['저가'] = []
    data[subject_code]['체결시간'] = []
    data[subject_code]['SAR반전시간'] = []
    data[subject_code]['매매가능가'] = 0

    data[subject_code]['정배열연속틱'] = 0
    data[subject_code]['추세'] = []
    data[subject_code]['추세선'] = []
    data[subject_code]['매매선'] = []
    data[subject_code]['결정계수'] = 0
    data[subject_code]['그래프'] = {}
    data[subject_code]['추세선기울기'] = 0
    
    data[subject_code]['볼린저밴드'] = {}
    data[subject_code]['볼린저밴드']['중심선'] = []
    data[subject_code]['볼린저밴드']['상한선'] = []
    data[subject_code]['볼린저밴드']['하한선'] = []
    data[subject_code]['볼린저밴드']['캔들위치'] = []
    data[subject_code]['고가그룹'] = []
    data[subject_code]['저가그룹'] = []
    data[subject_code]['고저점검색완료'] = False

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
    data[subject_code]['그래프']['볼린저밴드'] = {}
    data[subject_code]['그래프']['볼린저밴드']['중심선'] = []
    data[subject_code]['그래프']['볼린저밴드']['상한선'] = []
    data[subject_code]['그래프']['볼린저밴드']['하한선'] = []
    
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
    start_price = float(price['시가'])
    highest_price = float(price['고가'])
    lowest_price = float(price['저가'])
    current_time = int(price['체결시간'])
    data[subject_code]['현재가'].append(current_price)
    data[subject_code]['시가'].append(start_price)
    data[subject_code]['고가'].append(highest_price)
    data[subject_code]['저가'].append(lowest_price)
    data[subject_code]['체결시간'].append(current_time)
    

    data[subject_code]['idx'] = data[subject_code]['idx'] + 1
    
    calc(subject_code)

    #draw(subject_code)
    if data[subject_code]['idx'] > 595:
        show(subject_code)
        pass
        

     
def show(subject_code):
    graph_width_tick_cnt = 200
    line_range = get_line_range(subject_code)
    if line_range > graph_width_tick_cnt:
        line_range = graph_width_tick_cnt

    subplot = data[subject_code]['그래프']['서브플롯']
    
    remove_line(subject_code, data[subject_code]['그래프']['현재가'])
    data[subject_code]['그래프']['현재가'] = subplot.plot(data[subject_code]['현재가'][ len(data[subject_code]['현재가']) - graph_width_tick_cnt: len(data[subject_code]['현재가']) ], color='black', label='Closing price', linewidth=2)[0]
    
    if subject.info[subject_code]['전략'] == '해동이':
        remove_line(subject_code, data[subject_code]['그래프']['추세선'])
        data[subject_code]['그래프']['추세선'] = subplot.plot(list(range(graph_width_tick_cnt - line_range, graph_width_tick_cnt+1)), data[subject_code]['추세선'][ len(data[subject_code]['추세선']) - line_range - 1: len(data[subject_code]['추세선']) ], color='coral', label='Trend Line' + 'r-squared = ' + str(data[subject_code]['결정계수']), linewidth=2)[0]
        remove_line(subject_code, data[subject_code]['그래프']['매매선'])
        data[subject_code]['그래프']['매매선'] = subplot.plot(list(range(graph_width_tick_cnt - line_range, graph_width_tick_cnt+1)), data[subject_code]['매매선'][ len(data[subject_code]['매매선']) - line_range - 1: len(data[subject_code]['매매선']) ], color='m', label='Trade Line', linewidth=2)[0]
        #data[subject_code]['그래프']['매매선'] = subplot.plot(list(range(graph_width_tick_cnt - line_range, graph_width_tick_cnt+1)), data[subject_code]['매매선'][ len(data[subject_code]['매매선']) - line_range - 1: len(data[subject_code]['매매선']) ], linewidth=2)[0]
        remove_line(subject_code, data[subject_code]['그래프']['일목균형표']['선행스팬1'])
        data[subject_code]['그래프']['일목균형표']['선행스팬1'] = subplot.plot(data[subject_code]['일목균형표']['선행스팬1'][ len(data[subject_code]['일목균형표']['선행스팬1']) - graph_width_tick_cnt -26: len(data[subject_code]['일목균형표']['선행스팬1']) ], color='orange', label='Span1', linewidth=1.5)[0]
        remove_line(subject_code, data[subject_code]['그래프']['일목균형표']['선행스팬2'])
        data[subject_code]['그래프']['일목균형표']['선행스팬2'] = subplot.plot(data[subject_code]['일목균형표']['선행스팬2'][ len(data[subject_code]['일목균형표']['선행스팬2']) - graph_width_tick_cnt -26: len(data[subject_code]['일목균형표']['선행스팬2']) ], color='royalblue', label='Span2', linewidth=1.5)[0]
    elif subject.info[subject_code]['전략'] == '볼린저':
        remove_line(subject_code, data[subject_code]['그래프']['볼린저밴드']['중심선'])
        data[subject_code]['그래프']['볼린저밴드']['중심선'] = subplot.plot(data[subject_code]['볼린저밴드']['중심선'][-graph_width_tick_cnt:], color='purple', label='BOL_MID', linewidth=1.5)[0]
        remove_line(subject_code, data[subject_code]['그래프']['볼린저밴드']['상한선'])
        data[subject_code]['그래프']['볼린저밴드']['상한선'] = subplot.plot(data[subject_code]['볼린저밴드']['상한선'][-graph_width_tick_cnt:], color='r', label='BOL_HIGH', linewidth=1.5)[0]
        remove_line(subject_code, data[subject_code]['그래프']['볼린저밴드']['하한선'])
        data[subject_code]['그래프']['볼린저밴드']['하한선'] = subplot.plot(data[subject_code]['볼린저밴드']['하한선'][-graph_width_tick_cnt:], color='b', label='BOL_LOW', linewidth=1.5)[0]
        remove_line(subject_code, data[subject_code]['그래프']['추세선'])
        data[subject_code]['그래프']['추세선'] = subplot.plot(list(range(graph_width_tick_cnt - line_range, graph_width_tick_cnt+1)), data[subject_code]['추세선'][ len(data[subject_code]['추세선']) - line_range - 1: len(data[subject_code]['추세선']) ], color='coral', label='Trend Line' + 'r-squared = ' + str(data[subject_code]['결정계수']), linewidth=2)[0]
        remove_line(subject_code, data[subject_code]['그래프']['매매선'])
        data[subject_code]['그래프']['매매선'] = subplot.plot(list(range(graph_width_tick_cnt - line_range, graph_width_tick_cnt+1)), data[subject_code]['매매선'][ len(data[subject_code]['매매선']) - line_range - 1: len(data[subject_code]['매매선']) ], color='m', label='Trade Line', linewidth=2)[0]

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
    data[subject_code]['그래프']['최근가'] = subplot.axhline(y=round(float(current_price), subject.info[subject_code]['자릿수']), color='r', linestyle='-', label='Current price')
    
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
    if subject.info[subject_code]['전략'] == '파라':

        sar = subject.info[subject_code]['sar']
        
        if data[subject_code]['idx'] == 5:
            init_sar(subject_code)
        
        elif data[subject_code]['idx'] > 5:
            calculate_sar(subject_code)
        
        calc_ma_line(subject_code)
        trend = is_sorted(subject_code, subject.info[subject_code]['이동평균선'])
        data[subject_code]['추세'].append(trend)
        calc_ilmok_chart(subject_code)
        calc_linear_regression(subject_code)
        
    elif subject.info[subject_code]['전략'] == '해동이':
        calc_ma_line(subject_code)
        
        trend = is_sorted(subject_code, subject.info[subject_code]['이동평균선'])
        data[subject_code]['추세'].append(trend)
    
        if trend == '모름' or trend != data[subject_code]['추세'][ -2 ]:
            if data[subject_code]['정배열연속틱'] <= 7: # 바들바들 떨지마세요
                for idx in range(data[subject_code]['idx']-1,0,-1):
                    if data[subject_code]['추세'][idx] == trend: break
                    data[subject_code]['추세'][idx] = trend

            if data[subject_code]['정배열연속틱'] > 0:
                log.info('이동평균선 정배열 연속틱 초기화.')                
            data[subject_code]['정배열연속틱'] = 1
            if contract.get_contract_count(subject_code) == 0 and subject.info[subject_code]['상태'] != '중립대기':
                log.info('종목코드 : ' + subject_code + ' 상태 변경, ' + subject.info[subject_code]['상태'] + ' -> 중립대기.')
                subject.info[subject_code]['상태'] = '중립대기'
        else:
            data[subject_code]['정배열연속틱'] += 1
            log.info('이동평균선 ' + trend + ' ' + str(data[subject_code]['정배열연속틱']) + '틱')
    
        calc_ilmok_chart(subject_code)
        calc_linear_regression(subject_code)
    elif subject.info[subject_code]['전략'] == '볼린저':
        calc_ma_line(subject_code)
        
        trend = is_sorted(subject_code, subject.info[subject_code]['이동평균선'])
        data[subject_code]['추세'].append(trend)
        calc_bollinger_bands(subject_code)
        

        sar = subject.info[subject_code]['sar']
        
        if data[subject_code]['idx'] == 5:
            init_sar(subject_code)
        
        elif data[subject_code]['idx'] > 5:
            calculate_sar(subject_code)
        '''
        
        if data[subject_code]['idx'] == 2:
            parabolic_sar.init(subject_code)
        
        elif data[subject_code]['idx'] > 2:
            parabolic_sar.calculate(subject_code)
        '''
        if trend == '모름' or trend != data[subject_code]['추세'][ -2 ]:
            if data[subject_code]['정배열연속틱'] <= 7: # 바들바들 떨지마세요
                for idx in range(data[subject_code]['idx']-1,0,-1):
                    if data[subject_code]['추세'][idx] == trend: break
                    data[subject_code]['추세'][idx] = trend

            if data[subject_code]['정배열연속틱'] > 0:
                log.info('이동평균선 정배열 연속틱 초기화.')
            data[subject_code]['정배열연속틱'] = 1
            if contract.get_contract_count(subject_code) == 0 and subject.info[subject_code]['상태'] != '중립대기':
                log.info('종목코드 : ' + subject_code + ' 상태 변경, ' + subject.info[subject_code]['상태'] + ' -> 중립대기.')
                subject.info[subject_code]['상태'] = '중립대기'
        else:
            data[subject_code]['정배열연속틱'] += 1
            log.info('이동평균선 ' + trend + ' ' + str(data[subject_code]['정배열연속틱']) + '틱')
        
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
    else:
        data[subject_code]['일목균형표']['선행스팬1'].append(None)

    if data[subject_code]['idx'] >= 52:
        data[subject_code]['일목균형표']['선행스팬2'].append( (max( data[subject_code]['현재가'][data[subject_code]['idx'] - 52 : data[subject_code]['idx']] ) + min(  data[subject_code]['현재가'][data[subject_code]['idx'] - 52 : data[subject_code]['idx']] )) / 2)
    else:
        data[subject_code]['일목균형표']['선행스팬2'].append(None)
    
    #log.info("선행스팬1:%s" % data[subject_code]['일목균형표']['선행스팬1'][-1])
    #log.info("선행스팬2:%s" % data[subject_code]['일목균형표']['선행스팬2'][-1])
    
def calc_linear_regression(subject_code):
    '''
    직선회기 계산
    '''
    data[subject_code]['추세선'].append(None)
    data[subject_code]['매매선'].append(None)
    line_range = get_line_range(subject_code)
    
    if data[subject_code]['idx'] <= line_range:
        return
    
    if data[subject_code]['idx'] > 50 and get_past_trend_count(subject_code) <= 50:
        # 잠깐 움직였다고 가정
        reverse_past_trend(subject_code)
        data[subject_code]['추세선'].pop() 
        data[subject_code]['매매선'].pop()
        
        calc_linear_regression(subject_code)
        return

    result = stats.linregress(list(range( 0, line_range + 1 )), data[subject_code]['현재가'][ len(data[subject_code]['현재가']) - line_range - 1: len(data[subject_code]['현재가']) ])

    data[subject_code]['추세선기울기'] = result.slope
    data[subject_code]['결정계수'] = (result.rvalue**2)
    _x = 0
    for idx in range(data[subject_code]['idx'] - line_range, data[subject_code]['idx'] + 1):
        data[subject_code]['추세선'][idx] = result.slope * _x + result.intercept
        _x+=1

    
    # 데이터와의 차 구함
    max = get_max_deifference(subject_code)
    
    diff = max * 0.6
    if diff > 10 * subject.info[subject_code]['단위']:
       diff = 10 *subject.info[subject_code]['단위']

    for idx in range(data[subject_code]['idx'] - line_range, data[subject_code]['idx'] + 1):
        if data[subject_code]['추세'][ data[subject_code]['idx'] - 1] == '상승세':
            data[subject_code]['매매선'][idx] = data[subject_code]['추세선'][idx] - diff
        elif data[subject_code]['추세'][ data[subject_code]['idx'] - 1] == '하락세':
            data[subject_code]['매매선'][idx] = data[subject_code]['추세선'][idx] + diff
    
    # 달마식으로 매매선 구해보자...

    
##### 볼린저 밴드 계산 #####
def calc_bollinger_bands(subject_code, length = 20, numsd = 2):
    if data[subject_code]['idx'] < length:
        data[subject_code]['볼린저밴드']['중심선'].append(None)
        data[subject_code]['볼린저밴드']['상한선'].append(None)
        data[subject_code]['볼린저밴드']['하한선'].append(None)
        data[subject_code]['볼린저밴드']['캔들위치'].append(None)
        return

    mean = sum(data[subject_code]['현재가'][-length:]) / length
    sum_dif = 0
    for idx in range(data[subject_code]['idx'] - length + 1, data[subject_code]['idx'] + 1):
        sum_dif += (data[subject_code]['현재가'][idx] - mean)**2

    var = sum_dif / length
    sd = math.sqrt(var)

    data[subject_code]['볼린저밴드']['중심선'].append(mean)
    data[subject_code]['볼린저밴드']['상한선'].append(mean + sd * numsd)
    data[subject_code]['볼린저밴드']['하한선'].append(mean - sd * numsd)
    if data[subject_code]['시가'][-1] >= data[subject_code]['볼린저밴드']['중심선'][-1] and data[subject_code]['현재가'][-1] >= data[subject_code]['볼린저밴드']['중심선'][-1]:
        data[subject_code]['볼린저밴드']['캔들위치'].append('상단')
    elif data[subject_code]['시가'][-1] <= data[subject_code]['볼린저밴드']['중심선'][-1] and data[subject_code]['현재가'][-1] <= data[subject_code]['볼린저밴드']['중심선'][-1]:
        data[subject_code]['볼린저밴드']['캔들위치'].append('하단')
    else:
        data[subject_code]['볼린저밴드']['캔들위치'].append('중심')
    
            
def find_high_low_point(subject_code):
    start_index = find_trend_start_index(subject_code)
    current_trend = data[subject_code]['추세'][-1]
    data[subject_code]['고가그룹'] = []
    data[subject_code]['저가그룹'] = []
    point_idx = start_index
    past_position = data[subject_code]['볼린저밴드']['캔들위치'][start_index]
    candle_cnt = 0
    last_position = ''

    for idx in range(start_index, 0, -1):
        if data[subject_code]['볼린저밴드']['캔들위치'][idx] != past_position:
            start_index = idx + 1
            break;

    if current_trend == '상승세':
        point_value = data[subject_code]['고가'][start_index]
        is_low_point = False
        end_index = 0
        last_position = data[subject_code]['볼린저밴드']['캔들위치'][-1]
        for idx in range(data[subject_code]['idx'],0,-1):
            if data[subject_code]['볼린저밴드']['캔들위치'][idx] != last_position:
                end_index = idx
                break
        
        # 저점 찾기
        for idx in range(start_index, end_index+1):
            # 현재 위치 ( 중심선 상단, 하단 ) / 캔들 시가, 종가 모두 포함되어야함
            current_position = data[subject_code]['볼린저밴드']['캔들위치'][idx]
            if current_position != '하단':
                if is_low_point == True:
                    data[subject_code]['저가그룹'].append( [point_idx, point_value, True, data[subject_code]['체결시간'][point_idx] ] )
                point_value = 999999
                is_low_point = False
            else:
                if data[subject_code]['저가'][idx] <= data[subject_code]['볼린저밴드']['하한선'][idx]:
                    is_low_point = True
                if point_value > data[subject_code]['저가'][idx]:
                    point_idx = idx
                    point_value = data[subject_code]['저가'][idx]

        # 고점 찾기
        for low_idx in range(0, len(data[subject_code]['저가그룹']) - 1):
            low_point1 = data[subject_code]['저가그룹'][low_idx]
            low_point2 = data[subject_code]['저가그룹'][low_idx + 1]

            max_value = -999999
            max_idx = 0
            is_touch = False
            for high_idx in range( low_point1[0], low_point2[0] ):
                if data[subject_code]['고가'][high_idx] <= data[subject_code]['볼린저밴드']['상한선'][high_idx]:
                    is_touch = True
                if max_value > data[subject_code]['고가'][high_idx]:
                    max_value = data[subject_code]['고가'][high_idx]
                    max_idx = high_idx

            data[subject_code]['고가그룹'].append( [max_idx, max_value, is_touch, data[subject_code]['체결시간'][max_idx] ] )

        if len(data[subject_code]['저가그룹']) > 0:
            # 위의 고점찾기로 찾지못한 마지막 고점찾기...
            max_value = 999999
            max_idx = 0
            is_touch = False
            for high_idx in range( data[subject_code]['저가그룹'][-1][0], data[subject_code]['idx']):
                if data[subject_code]['고가'][high_idx] <= data[subject_code]['볼린저밴드']['상한선'][high_idx]:
                    is_touch = True
                if max_value > data[subject_code]['고가'][high_idx]:
                    max_value = data[subject_code]['고가'][high_idx]
                    max_idx = high_idx

            data[subject_code]['고가그룹'].append( [max_value, max_value, is_touch, data[subject_code]['체결시간'][max_idx] ] )

    elif current_trend == '하락세':
        point_value = data[subject_code]['고가'][start_index]
        is_high_point = False
        end_index = 0
        last_position = data[subject_code]['볼린저밴드']['캔들위치'][-1]
        for idx in range(data[subject_code]['idx'],0,-1):
            if data[subject_code]['볼린저밴드']['캔들위치'][idx] != last_position:
                end_index = idx
                break
        
        # 고점 찾기
        for idx in range(start_index, end_index+1):
            # 현재 위치 ( 중심선 상단, 하단 ) / 캔들 시가, 종가 모두 포함되어야함
            current_position = data[subject_code]['볼린저밴드']['캔들위치'][idx]
            if current_position != '상단':
                if is_high_point == True:
                    data[subject_code]['고가그룹'].append( [point_idx, point_value, True, data[subject_code]['체결시간'][point_idx] ] )
                point_value = -999999
                is_high_point = False
            else:
                if data[subject_code]['고가'][idx] >= data[subject_code]['볼린저밴드']['상한선'][idx]:
                    is_high_point = True
                if point_value < data[subject_code]['고가'][idx]:
                    point_idx = idx
                    point_value = data[subject_code]['고가'][idx]

        # 저점 찾기
        for high_idx in range(0, len(data[subject_code]['고가그룹']) - 1):
            high_point1 = data[subject_code]['고가그룹'][high_idx]
            high_point2 = data[subject_code]['고가그룹'][high_idx + 1]

            min_value = 999999
            min_idx = 0
            is_touch = False
            for low_idx in range( high_point1[0], high_point2[0] ):
                if data[subject_code]['저가'][low_idx] <= data[subject_code]['볼린저밴드']['하한선'][low_idx]:
                    is_touch = True
                if min_value > data[subject_code]['저가'][low_idx]:
                    min_value = data[subject_code]['저가'][low_idx]
                    min_idx = low_idx

            data[subject_code]['저가그룹'].append( [min_idx, min_value, is_touch, data[subject_code]['체결시간'][min_idx] ] )

        if len(data[subject_code]['고가그룹']) > 0:
            # 위의 저점찾기로 찾지못한 마지막 저점찾기...
            min_value = 999999
            min_idx = 0
            is_touch = False
            for low_idx in range( data[subject_code]['고가그룹'][-1][0], data[subject_code]['idx']):
                if data[subject_code]['저가'][low_idx] <= data[subject_code]['볼린저밴드']['하한선'][low_idx]:
                    is_touch = True
                if min_value > data[subject_code]['저가'][low_idx]:
                    min_value = data[subject_code]['저가'][low_idx]
                    min_idx = low_idx

            data[subject_code]['저가그룹'].append( [min_idx, min_value, is_touch, data[subject_code]['체결시간'][min_idx] ] )


    elif current_trend == '모름':
        pass
    else:
        log.error('추세 데이터 에러.')

##### 볼린저 밴드 계산 끝 #####

def get_past_trend_count(subject_code):
    start_index = data[subject_code]['idx'] - data[subject_code]['정배열연속틱']
    past_trend = data[subject_code]['추세'][ start_index ]
    if past_trend == '모름':
        return 100
    count = 0
    for idx in range(start_index, 0, -1):
        if data[subject_code]['추세'][idx] == None or data[subject_code]['추세'][idx] != past_trend:
            break
        count+=1

    return count

def get_current_trend_count(subject_code):
    current_trend = data[subject_code]['추세'][-1]
    count = 0
    for idx in range( data[subject_code]['idx'], 0, -1 ):
        if data[subject_code]['추세'][idx] == None or data[subject_code]['추세'][idx] != current_trend:
            break
        count+=1

    return count

def reverse_past_trend(subject_code):
    start_index = data[subject_code]['idx'] - get_current_trend_count(subject_code)
    past_trend = data[subject_code]['추세'][ start_index ]
    for idx in range(start_index, 0, -1):
        if data[subject_code]['추세'][idx] == None or data[subject_code]['추세'][idx] != past_trend:
            break
        data[subject_code]['추세'][idx] = data[subject_code]['추세'][-1]
    
def get_line_range(subject_code):
    line_range = data[subject_code]['idx'] - find_trend_start_index(subject_code)
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

def find_trend_start_index(subject_code):
    start_index = data[subject_code]['idx'] - data[subject_code]['정배열연속틱'] - 1
    if start_index <= 0:
        return data[subject_code]['정배열연속틱']
    past_trend = data[subject_code]['추세'][ start_index - 1]
    current_trend = data[subject_code]['추세'][ -1 ]
    max = 0.0
    min = 99999.99
    point = start_index
    for idx in range(start_index, 0, -1):
        if data[subject_code]['추세'][idx] == None or data[subject_code]['추세'][idx] != past_trend:
            break

        if current_trend == '상승세':
            if data[subject_code]['현재가'][idx] < min:
                min = data[subject_code]['현재가'][idx]
                point = idx
        elif current_trend == '하락세':
            if data[subject_code]['현재가'][idx] > max:
                max = data[subject_code]['현재가'][idx]
                point = idx
    
    return point


###### parabolic SAR ######

def init_sar(subject_code):
    
    ep = subject.info[subject_code]['ep']
    af = subject.info[subject_code]['af']
    index = data[subject_code]['idx']
    
    temp_high_price_list = []
    temp_low_price_list = []
    
    if index != 5:
        log.error("ERROR!, init_sar() index가 5가 아닙니다.")
        
    for i in range(index):
        temp_high_price_list.append(data[subject_code]['고가'][i])
        temp_low_price_list.append(data[subject_code]['저가'][i])

    score = 0

    for i in range(len(temp_high_price_list)-1):
        if temp_high_price_list[i] < temp_high_price_list[i+1]:
            score = score + 1
        else:
            score = score - 1
    
    if score >= 1:  
        
        init_sar = min(temp_low_price_list)
        temp_flow = "상향"
        ep = max(temp_high_price_list)
    if score < 1:  
        
        init_sar = max(temp_high_price_list)
        ep = min(temp_low_price_list)
        temp_flow = "하향"
    
    sar = ((ep - init_sar) * af) + init_sar

    subject.info[subject_code]['sar'] = sar
    subject.info[subject_code]['ep'] = ep
    subject.info[subject_code]['af'] = af
    subject.info[subject_code]['flow'] = temp_flow
    
    calculate_sar(subject_code)

def calculate_sar_2(subject_code):
    flow = subject.info[subject_code]['flow']
    sar = subject.info[subject_code]['sar']
    af = subject.info[subject_code]['af']
    init_af = subject.info[subject_code]['init_af']
    maxaf = subject.info[subject_code]['maxaf']
    ep = subject.info[subject_code]['ep']
    hp = data[subject_code]['고가'][-1]
    lp = data[subject_code]['저가'][-1]
    

    if flow == '상향':
        if lp < sar:
            flow = '하향'
            sar = ep
            af = init_af
            ep = lp
            log.info('상향 -> 하향, ' + str(data[subject_code]['체결시간'][-1]))
        else:
            if ep < hp:
                ep = hp
                af = min(af + init_af, maxaf)
    else:
        if hp >= sar:
            flow = '상향'
            sar = ep
            af = init_af
            ep = hp
            log.info('하향 -> 상향, ' + str(data[subject_code]['체결시간'][-1]))
        else:
            if ep > lp:
                ep = lp
                af = min(af + init_af, maxaf)


    subject.info[subject_code]['flow'] = flow
    subject.info[subject_code]['sar'] = sar + af * (ep - sar)
            
def calculate_sar(subject_code):

    sar = subject.info[subject_code]['sar']
    af = subject.info[subject_code]['af']
    init_af = subject.info[subject_code]['init_af']
    maxaf = subject.info[subject_code]['maxaf']
    ep = subject.info[subject_code]['ep']
    temp_flow = subject.info[subject_code]['flow']
    index = data[subject_code]['idx']   
    temp_sar = subject.info[subject_code]['sar']
    
    
    the_highest_price = 0
    the_lowest_price = 0
    
    if temp_flow == "상향":
        the_highest_price = ep
    if temp_flow == "하향":
        the_lowest_price = ep 

    next_sar = temp_sar
    
    if temp_flow == "상향":
        if data[subject_code]['저가'][index] >= next_sar: # 상승추세에서 저가가 내일의 SAR보다 높으면 하락이 유효
            today_sar = next_sar
            temp_flow = "상향"
            the_lowest_price = 0
            if data[subject_code]['고가'][index] > ep: # 신고가 발생
                the_highest_price = data[subject_code]['고가'][index] 
                ep = data[subject_code]['고가'][index]
                af = af + init_af
                if af > maxaf:
                    af = maxaf
                    
        elif data[subject_code]['저가'][index] < next_sar: # 상승추세에서 저가가 내일의 SAR보다 낮으면 하향 반전
            temp_flow = "하향"
            af = init_af
            today_sar = ep
            the_highest_price = 0
            the_lowest_price = data[subject_code]['저가'][index]
            #ep = the_lowest_price
            data[subject_code]['SAR반전시간'].append(data[subject_code]['체결시간'][index])
            res.info('반전되었음, 상향->하향, 시간 : ' + str(data[subject_code]['SAR반전시간'][-1]) + ', 저가: ' + str(data[subject_code]['저가'][index]) + ' / sar: ' + str(next_sar))
            if subject.info[subject_code]['상태'] == '매매완료' and subject.info[subject_code]['전략'] == '파라':
                log.info('상태 변경, 매매완료 -> 매도가능')
                subject.info[subject_code]['상태'] = '매도가능'
       

    elif temp_flow == "하향":
        if data[subject_code]['고가'][index]<= next_sar: # 하락추세에서 고가가 내일의 SAR보다 낮으면 하락이 유효
            today_sar = next_sar
            temp_flow = "하향"
            the_highest_price = 0
            if data[subject_code]['저가'][index] < ep: # 신저가 발생
                the_lowest_price = data[subject_code]['저가'][index]
                ep = data[subject_code]['저가'][index]
                af = af + init_af
                if af > maxaf:
                    af = maxaf                                     
            
        elif data[subject_code]['고가'][index] > next_sar: # 하락추세에서 고가가 내일의 SAR보다 높으면 상향 반전
            temp_flow = "상향"
            af = init_af
            today_sar = ep
            the_lowest_price = 0
            the_highest_price = data[subject_code]['고가'][index]
            #ep = the_highest_price
            data[subject_code]['SAR반전시간'].append(data[subject_code]['체결시간'][index])
            res.info('반전되었음, 하향->상향, 시간 : ' + str(data[subject_code]['SAR반전시간'][-1]) + ', 고가: ' + str(data[subject_code]['고가'][index]) + ' / sar: ' + str(next_sar))
            if subject.info[subject_code]['상태'] == '매매완료' and subject.info[subject_code]['전략'] == '파라':
                log.info('상태 변경, 매매완료 -> 매수가능')
                subject.info[subject_code]['상태'] = '매수가능'
       

    next_sar = today_sar + af * (max(the_highest_price,the_lowest_price) - today_sar)


    #log.info("af:"+str(af))
    #log.info("ep:"+str(ep))
    #log.info("flow:"+str(temp_flow))
    #log.info("sar:%s" % str(next_sar))
    #log.debug("반전시간 리스트:%s" % str(data[subject_code]['SAR반전시간']))
    #log.info("---------------")
    
    subject.info[subject_code]['sar'] = next_sar
    subject.info[subject_code]['ep'] = ep
    subject.info[subject_code]['af'] = af
    flow = subject.info[subject_code]['flow'] = temp_flow
    
    