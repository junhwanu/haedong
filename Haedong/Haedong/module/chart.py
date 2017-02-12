# -*- coding: utf-8 -*-
import calc, subject, my_util
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib import style
from scipy import stats

figure = {}
figure_count = 0
subplot = {}
graph = {}
#style.use('fivethirtyeight')

plt.ion()

def create_figure(subject_code):
    global figure_count

    if subject_code in figure.keys():
        return

    figure[subject_code] = plt.figure(figure_count)
    figure_count = figure_count + 1
    #ax = figure[subject_code].add_subplot(111) 
    ax = plt.subplot2grid((1,1), (0,0))
    ax.margins(y=.1)

    figure[subject_code].suptitle(subject_code, size=16)
    subplot[subject_code] = []
    subplot[subject_code].append(ax)

    figure[subject_code].show()

def init_graph(subject_code):
    # 그래프 초기화
    ax = subplot[subject_code][0]
    x_axis = list(range(0, calc.data[subject_code]['idx']+1))
    x_axis_span = list(range(0, len(calc.data[subject_code]['일목균형표']['선행스팬1'])))
    ax.grid(True)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)

    graph[subject_code] = {}
    
    graph[subject_code]['현재가'] = ax.plot(x_axis, calc.data[subject_code]['현재가'], color='black', label='Closing price', linewidth=1)[0]
    graph[subject_code]['일목균형표'] = {}
    graph[subject_code]['일목균형표']['선행스팬1'] = ax.plot(x_axis_span, calc.data[subject_code]['일목균형표']['선행스팬1'], color='#F7A26A', linewidth=1)[0]
    graph[subject_code]['일목균형표']['선행스팬2'] = ax.plot(x_axis_span, calc.data[subject_code]['일목균형표']['선행스팬2'], color='#6A8BEF', linewidth=1)[0]
    graph[subject_code]['추세선'] = ax.plot(x_axis_span, calc.data[subject_code]['추세선'], color='#f37e21', label='Trend line', linewidth=1.5)[0]
    graph[subject_code]['추세선밴드'] = {}
    graph[subject_code]['추세선밴드']['상한선'] = ax.plot(x_axis_span, calc.data[subject_code]['추세선밴드']['상한선'], color='#0f98ab', linewidth=1)[0]
    graph[subject_code]['추세선밴드']['하한선'] = ax.plot(x_axis_span, calc.data[subject_code]['추세선밴드']['하한선'], color='#0f98ab', linewidth=1)[0]
    graph[subject_code]['볼린저밴드'] = {}
    graph[subject_code]['볼린저밴드']['상한선'] = ax.plot(x_axis, calc.data[subject_code]['볼린저밴드']['상한선'], color='#fa8072', linewidth=1)[0]
    graph[subject_code]['볼린저밴드']['중심선'] = ax.plot(x_axis, calc.data[subject_code]['볼린저밴드']['중심선'], color='#c79bbf', linewidth=1)[0]
    graph[subject_code]['볼린저밴드']['하한선'] = ax.plot(x_axis, calc.data[subject_code]['볼린저밴드']['하한선'], color='#fa8072', linewidth=1)[0]

    graph[subject_code]['지수이동평균선'] = {}
    colors = ['red', 'blue', 'green']
    color_idx = 0
    for line in subject.info[subject_code]['이동평균선']:
        graph[subject_code]['지수이동평균선'][line] = ax.plot(x_axis, calc.data[subject_code]['지수이동평균선'][line], color=colors[color_idx], label='SMA' + str(line), linewidth=1.5)[0]
        color_idx += 1

    figure[subject_code].canvas.draw()

def draw(subject_code):
    if subject_code not in graph.keys():
        init_graph(subject_code)
        
    ax = subplot[subject_code][0]
    x_axis = list(range(0, calc.data[subject_code]['idx']+1))
    x_axis_span = list(range(0, len(calc.data[subject_code]['일목균형표']['선행스팬1'])))

    '''
    ax.clear()
    ax.grid(True)
    ax.get_yaxis().get_major_formatter().set_useOffset(False)
    ax.get_yaxis().get_major_formatter().set_scientific(False)
    '''

    # 대표 X Label
    labels = [item.get_text() for item in ax.get_xticklabels()]
    label_idx = 0
    for idx in ax.get_xticks():
        if idx <= calc.data[subject_code]['idx']:
            labels[label_idx] = my_util.get_date_string_from_date_int(calc.data[subject_code]['체결시간'][int(idx)])
            label_idx += 1

    ax.set_xticklabels(labels, rotation=45)
    
    #ax.draw_artist(ax.patch)
    
    # 캔들
    candlestick_ohlc(ax, calc.data[subject_code]['캔들'], width = 0.8, colorup='#C22525', colordown='#4455DD')

    # 종가
    graph[subject_code]['현재가'].set_xdata(x_axis)
    graph[subject_code]['현재가'].set_ydata(calc.data[subject_code]['현재가'])
    #ax.draw_artist(graph[subject_code]['현재가'])
    
    # 추세선
    graph[subject_code]['추세선'].set_xdata(x_axis_span)
    graph[subject_code]['추세선'].set_ydata(calc.data[subject_code]['추세선'])
    #ax.draw_artist(graph[subject_code]['추세선'])

    # 추세선밴드
    graph[subject_code]['추세선밴드']['상한선'].set_xdata(x_axis_span)
    graph[subject_code]['추세선밴드']['상한선'].set_ydata(calc.data[subject_code]['추세선밴드']['상한선'])
    graph[subject_code]['추세선밴드']['하한선'].set_xdata(x_axis_span)
    graph[subject_code]['추세선밴드']['하한선'].set_ydata(calc.data[subject_code]['추세선밴드']['하한선'])
    #ax.draw_artist(graph[subject_code]['추세선밴드']['상한선'])
    #ax.draw_artist(graph[subject_code]['추세선밴드']['하한선'])

    # 볼린저밴드
    graph[subject_code]['볼린저밴드']['상한선'].set_xdata(x_axis)
    graph[subject_code]['볼린저밴드']['상한선'].set_ydata(calc.data[subject_code]['볼린저밴드']['상한선'])
    graph[subject_code]['볼린저밴드']['하한선'].set_xdata(x_axis)
    graph[subject_code]['볼린저밴드']['하한선'].set_ydata(calc.data[subject_code]['볼린저밴드']['하한선'])
    graph[subject_code]['볼린저밴드']['중심선'].set_xdata(x_axis)
    graph[subject_code]['볼린저밴드']['중심선'].set_ydata(calc.data[subject_code]['볼린저밴드']['중심선'])
    #ax.draw_artist(graph[subject_code]['볼린저밴드']['상한선'])
    #ax.draw_artist(graph[subject_code]['볼린저밴드']['하한선'])
    #ax.draw_artist(graph[subject_code]['볼린저밴드']['중심선'])

    # 이동평균선
    for line in subject.info[subject_code]['이동평균선']:
        graph[subject_code]['지수이동평균선'][line].set_xdata(x_axis)
        graph[subject_code]['지수이동평균선'][line].set_ydata(calc.data[subject_code]['지수이동평균선'][line])
        #ax.draw_artist(graph[subject_code]['이동평균선'][line])

    # 일목균형표
    ax.set_xlim(len(x_axis_span)-300, len(x_axis_span))
    graph[subject_code]['일목균형표']['선행스팬1'].set_xdata(x_axis_span)
    graph[subject_code]['일목균형표']['선행스팬1'].set_ydata(calc.data[subject_code]['일목균형표']['선행스팬1'])
    graph[subject_code]['일목균형표']['선행스팬2'].set_xdata(x_axis_span)
    graph[subject_code]['일목균형표']['선행스팬2'].set_ydata(calc.data[subject_code]['일목균형표']['선행스팬2'])
    #ax.draw_artist(graph[subject_code]['일목균형표']['선행스팬1'])
    #ax.draw_artist(graph[subject_code]['일목균형표']['선행스팬2'])


    figure[subject_code].canvas.draw()
    #figure[subject_code].update()
    #figure[subject_code].flush_events()
