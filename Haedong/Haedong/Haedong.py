# -*- coding: utf-8 -*-
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/module')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/item')
import kiwoom, cmd, log, contract, subject, calc
import matplotlib.pyplot as plt

kw = None

if __name__ == "__main__":
   
    log.init(os.path.dirname(os.path.abspath(__file__).replace('\\','/')))
    
    #cmd.init()
    kw = kiwoom.api()
    
