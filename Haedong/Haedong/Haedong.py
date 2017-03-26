# -*- coding: utf-8 -*-
import sys, os, time, threading
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/module')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/item')
import kiwoom, cmd, log, contract, subject, calc, tester, dbinsert, dbsubject, my_util, gmail
import define as d
import log_result as res
import matplotlib.pyplot as plt
import datetime

kw = None
            
if __name__ == "__main__":
    log.init(os.path.dirname(os.path.abspath(__file__).replace('\\','/')))
    res.init(os.path.dirname(os.path.abspath(__file__).replace('\\','/')))
    
    print('실제투자(1), 테스트(2), DB Insert(3)')
    d.mode = int(input())
        
    #cmd.init()
    if d.get_mode() == 1:
        try:
            kw = kiwoom.api()
        except Exception as err:
            body = str(err) + '\n'
            body = body + str(sys.exc_info()[0])
            gmail.send_email("[긴급] 해동이 작동중지.", body)
    elif d.get_mode() == 2:
        tester.init() 

    elif d.get_mode() == 3:
        kw = dbinsert.api()

    else:
        print('잘못된 입력입니다.')
    