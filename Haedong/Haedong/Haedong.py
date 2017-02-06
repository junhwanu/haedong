# -*- coding: utf-8 -*-
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/module')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/item')
import kiwoom, cmd, log, contract, subject, calc, tester
import define as d
import log_result as res
import matplotlib.pyplot as plt

kw = None

if __name__ == "__main__":
    log.init(os.path.dirname(os.path.abspath(__file__).replace('\\','/')))
    res.init(os.path.dirname(os.path.abspath(__file__).replace('\\','/')))
    
    #cmd.init()
    
    print('실제투자(1), 테스트(2)')
    d.mode = int(input())
    #kw = kiwoom.api()

    if d.get_mode() == 1:
        kw = kiwoom.api()
    elif d.get_mode() == 2:
        tester.init() 
    else:
        print('잘못된 입력입니다.')

    
