# -*- coding: utf-8 -*-
import sys, time, os
import gmail, log, calc, santa, screen, para, tester
import define as d
import json
import subject, contract
import log_result as res

from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QApplication

kiwoom = None

def get_instance():
    if kiwoom == None:
        kiwoom = api()
    
    return kiwoom

class api():
    app = None
    recent_price = {}
    recent_candle_time = {}
    account = ""
    cnt = 0

    def __init__(self, mode = 1):
        super(api, self).__init__()
        if d.get_mode() == d.REAL:
            self.app = QApplication(sys.argv)

            self.ocx = QAxWidget("KFOPENAPI.KFOpenAPICtrl.1")
            self.ocx.OnEventConnect[int].connect(self.OnEventConnect)
            self.ocx.OnReceiveTrData[str, str, str, str, str].connect(self.OnReceiveTrData)
            self.ocx.OnReceiveChejanData[str, int, str].connect(self.OnReceiveChejanData)
            self.ocx.OnReceiveRealData[str, str, str].connect(self.OnReceiveRealData)
        
            if self.connect() == 0:
                self.app.exec_()

        elif d.get_mode() == d.TEST:
            pass


    ####################################################
    # Interface Methods
    ####################################################

    def connect(self):
        """
        로그인 윈도우를 실행한다.
        로그인이 성공하거나 실패하는 경우 OnEventConnect 이벤트가 발생하고 이벤트의 인자 값으로 로그인 성공 여부를 알 수 있다.

        :return: 0 - 성공, 음수값은 실패
        """

        if self.ocx.dynamicCall("GetConnectState()") == 0:
            rtn = self.ocx.dynamicCall("CommConnect(1)")
            if rtn == 0:
                print("연결 성공")
            else:
                print("연결 실패")

            return rtn

    def get_login_info(self, sTag):
        """
        로그인한 사용자 정보를 반환한다.

        :param sTag: 사용자 정보 구분 TAG값
            “ACCOUNT_CNT” ? 전체 계좌 개수를 반환한다.
            "ACCNO" ? 전체 계좌를 반환한다. 계좌별 구분은 ‘;’이다.
            “USER_ID” - 사용자 ID를 반환한다.
            “USER_NAME” ? 사용자명을 반환한다.
            “KEY_BSECGB” ? 키보드보안 해지여부. 0:정상, 1:해지
            “FIREW_SECGB” ? 방화벽 설정 여부. 0:미설정, 1:설정, 2:해지
            Ex) openApi.GetLoginInfo(“ACCOUNT_CNT”);
        :return: TAG값에 따른 데이터 반환
        """
        return self.ocx.dynamicCall("GetLoginInfo(QString)", [sTag]).rstrip(';')
    
    def get_dynamic_subject_info(self):
        self.get_dynamic_subject_code()
        self.get_dynamic_subject_market_time()
    
    def get_dynamic_subject_code(self):
        lists = ['MTL','ENG','CUR','IDX','CMD']
        for list in lists:
            self.set_input_value("상품코드", list)
            self.comm_rq_data("상품별현재가조회", "opt10006", "", screen.S0010)
            time.sleep(0.5)
        
    def get_dynamic_subject_market_time(self):
        lists = ['MTL','ENG','CUR','IDX','CMD']
        for list in lists:
            self.set_input_value("품목구분", list)
            self.comm_rq_data("장운영정보조회", "opw50001", "", screen.S0011)
            time.sleep(0.5)
        

    def send_order(self, contract_type, subject_code, contract_cnt):
        
        """
        주식 주문을 서버로 전송한다.
        신규매수:self.send_order("신규매수","0101",my_account_number,1,subject_code,1,now_current_price,"","2","")
           

        신규매도:
        매수청산:
       매도청산:self.send_order("신규매수","0101",my_account_number,2,subject_code,subject_info[subject_code]['보유수량'],now_current_price,"2","")
       
 
        :param sRQName: 사용자 구분 요청 명
        :param sScreenNo: 화면번호[4]
        :param sAccNo: 계좌번호[10]
        :param nOrderType: 주문유형 (1:신규매수, 2:신규매도, 3:매수취소, 4:매도취소, 5:매수정정, 6:매 도정정)
        :param sCode: 주식종목코드
        :param nQty: 주문수량
        :param sPrice: 주문단가
        :param sStop: 스탑단가
        :param sHogaGb: 거래구분 1:시장가, 2:지정가, 3:STOP, 4:STOP LIMIT
            
            ※ 시장가, 최유리지정가, 최우선지정가, 시장가IOC, 최유리IOC, 시장가FOK, 최유리FOK, 장전시간외, 장후시간외 주문시 주문가격을 입력하지 않습니다.
            ex)
            지정가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 1, “000660”, 10, 48500, “00”, “”);
            시장가 매수 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 1, “000660”, 10, 0, “03”, “”);
            매수 정정 - openApi.SendOrder(“RQ_1”,“0101”, “5015123410”, 5, “000660”, 10, 49500, “00”, “1”);
            매수 취소 - openApi.SendOrder(“RQ_1”, “0101”, “5015123410”, 3, “000660”, 10, 0, “00”, “2”);
        :param sOrgOrderNo: 원주문번호
        :return: 에러코드 - parse_error_code
            -201     : 주문과부하 
            -300     : 주문입력값 오류
            -301     : 계좌비밀번호를 입력하십시오.
            -302     : 타인 계좌를 사용할 수 없습니다.
            -303     : 경고-주문수량 200개 초과
            -304     : 제한-주문수량 400개 초과

        """
        _contract_type = 0
        if contract_type == '신규매수':
            _contract_type = 2
        elif contract_type == '신규매도':
            _contract_type = 1
        else: return -300

        if d.get_mode() == d.REAL:
            return self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, QString, QString, QString, QString)",
                                        [contract_type, '0101', self.account, _contract_type, subject_code, contract_cnt, '0', '0', '1', ''])
        elif d.get_mode() == d.TEST: #테스트
            tester.send_order(contract_type, subject_code, contract_cnt, '1')
            return 0

    def request_tick_info(self, subject_code, tick_unit, prevNext):

        self.set_input_value("종목코드", subject_code)
        self.set_input_value("시간단위", tick_unit)
        '''
        temp = prevNext
        if prevNext != "":
            tmp_num = temp.split()[2]
            a = tmp_num[0:len(tmp_num)-6]
            tmp_num.replace(a, "")
            if int(a) <= 1756800000 and ' 09 ' in temp:
                temp = temp.replace(' 09 ', ' 00 ')
                temp = temp.replace('F0','EE')
            '''
        rtn = self.comm_rq_data("해외선물옵션틱그래프조회","opc10001", prevNext, subject.info[subject_code]['화면번호'])

        if rtn != 0:
            # 에러코드별 로그
            log.error(self.parse_error_code(rtn))
            
        while rtn == -200:
            time.sleep(0.05)
            rtn = self.comm_rq_data("해외선물옵션틱그래프조회","opc10001", prevNext, subject.info[subject_code]['화면번호'])
        

    def set_input_value(self, sID, sValue):
        """
        Tran 입력 값을 서버통신 전에 입력한다.

        :param sID: 아이템명
        :param sValue: 입력 값
        Ex) openApi.SetInputValue(“종목코드”, “000660”);
            openApi.SetInputValue(“계좌번호”, “5015123401”);
        """
        self.ocx.dynamicCall("SetInputValue(QString, QString)", sID, sValue)

    def comm_rq_data(self, sRQName, sTrCode, nPrevNext, sScreenNo):
        """
        Tran을 서버로 송신한다.

        :param sRQName: 사용자구분 명
        :param sTrCode: Tran명 입력
        :param nPrevNext: 0:조회, 2:연속
        :param sScreenNo: 4자리의 화면번호
        Ex) openApi.CommRqData( “RQ_1”, “OPT00001”, 0, “0101”);
        :return:
        OP_ERR_SISE_OVERFLOW – 과도한 시세조회로 인한 통신불가
        OP_ERR_RQ_STRUCT_FAIL – 입력 구조체 생성 실패
        OP_ERR_RQ_STRING_FAIL – 요청전문 작성 실패
        OP_ERR_NONE(0) – 정상처리
        """
        return self.ocx.dynamicCall("CommRqData(QString, QString, QString, QString)", sRQName, sTrCode, nPrevNext, sScreenNo)

    def quit(self):
        """ Quit the server """

        QApplication.quit()
        sys.exit()  

    ####################################################
    # Control Event Handlers
    ####################################################

    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext, candle = None):
        """
        Tran 수신시 이벤트
        서버통신 후 데이터를 받은 시점을 알려준다.

        :param py: 화면번호
        :param sRQName: 사용자구분 명
        :param sTrCode: Tran 명
        :param sRecordName: Record 명
        :param sPreNext: 연속조회 유무
        :param nDataLength: 1.0.0.1 버전 이후 사용하지 않음.
        :param sErrorCode: 1.0.0.1 버전 이후 사용하지 않음.
        :param sMessage: 1.0.0.1 버전 이후 사용하지 않음.
        :param sSplmMsg: 1.0.0.1 버전 이후 사용하지 않음.
        """
        
        price = {}
        
        if sRQName == "해외선물옵션틱그래프조회":
            for subject_code in subject.info.keys():
                if sScrNo == subject.info[subject_code]['화면번호']:  
                    if subject_code not in calc.data:
                        calc.create_data(subject_code)

                        if d.get_mode() == d.REAL:
                            # 초기 데이터 수신
                            data = self.ocx.dynamicCall("GetCommFullData(QString, QString, int)", sTrCode, sRecordName, 0)
                            data = data.split()
                        
                            subject.info[subject_code]['현재가변동횟수'] = int(data[0])

                            current_idx = len(data) - 7
                            start_time = self.get_start_time(subject_code)
                            while current_idx > 8:
                            
                                price['현재가'] = data[current_idx]
                                price['고가'] = data[current_idx + 4]
                                price['저가'] = data[current_idx + 5]
                                price['체결시간'] = data[current_idx + 2]
                            
                                current_idx -= 7
                                ''' 오늘 데이터만 받아오는 코드
                                if int(data[current_idx + 2]) >= int(start_time):
                                    calc.push(subject_code, price)
                                '''
                                calc.push(subject_code, price)

                            # 최근가
                            self.recent_price[subject_code] = round(float(data[1]), subject.info[subject_code]['자릿수'])

                            self.recent_candle_time[subject_code] = data[10]
                            log.debug('지난 데이터 수신 완료.')

                            calc.show_current_price(subject_code, self.recent_price[subject_code])
                        elif d.get_mode() == d.TEST:
                            self.recent_price[subject_code] = candle['현재가']
                            self.recent_candle_time[subject_code] = candle['체결시간']
                        
                    if d.get_mode() == d.REAL: # 실제투자
                        price['현재가'] = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, 1, '현재가')
                        price['저가'] = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, 1, '저가')
                        price['고가'] = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, 1, '고가')
                        price['시가'] = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, 1, '시가')
                        price['체결시간'] = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, 1, '체결시간')
                    elif d.get_mode() == d.TEST: # 테스트
                        price = candle


                    # 캔들이 갱신되었는지 확인
                    if self.recent_candle_time[subject_code] != price['체결시간']:
                        # 캔들 갱신
                        santa.update_state_by_current_candle(subject_code, price)
                        calc.push(subject_code, price)
                        self.recent_candle_time[subject_code] = price['체결시간']
                        log.debug("캔들 추가, 체결시간: " + self.recent_candle_time[subject_code])
                        
                    break
                
        if sRQName == '상품별현재가조회':
            
            for i in range(20):
                d.RECEIVED_PRODUCT_COUNT += 1
                subject_code = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, '종목코드n').strip() #현재가 = 틱의 종가
                subject_symbol = subject_code[:2] 
                if subject_symbol in subject.info.keys():
                    log.info("금일 %s의 종목코드는 %s 입니다." % (subject.info[subject_symbol]["종목명"],subject_code))
                    subject.info[subject_code] = subject.info[subject_symbol]
                    del subject.info[subject_symbol]
                    
                    # 초기 데이터 요청
                    self.request_tick_info(subject_code,subject.info[subject_code]["시간단위"], "")
        
            if d.RECEIVED_PRODUCT_COUNT == d.PRODUCT_CNT:
                self.ocx.dynamicCall("DisconnectRealData(QString)", screen.S0010)
                self.ocx.dynamicCall("DisconnectRealData(QString)", screen.S0011)

        if sRQName == "장운영정보조회":
            
            log.info("장운영정보조회")
            for i in range(20):
                subject_code = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, '파생품목코드')
                market_time1 = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, '장운영시간1')
                market_time2 = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, '장운영시간2')
                market_time3 = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, '장운영시간3')
                market_time4 = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, '장운영시간4')
                
                log.info(subject_code)
                log.info(market_time1)
                log.info(market_time2)
                log.info(market_time3)
                log.info(market_time4)
            
    def OnReceiveRealData(self, subject_code, sRealType, sRealData):
        """
        실시간 시세 이벤트
        실시간데이터를 받은 시점을 알려준다.

        :param subject_code: 종목코드
        :param sRealType: 리얼타입
        :param sRealData: 실시간 데이터전문
        """
        # 캔들 생기는 시점 확인해서 가격이 안바뀌어도 옥수수에 3틱으로 설정할 경우 가격변동없이 캔들이 생기는 경우가 있으니 request_tick_info 시점 확인
        
        #log.debug("OnReceiveRealData entered.")
        if subject_code not in subject.info.keys() and d.get_mode() == d.REAL: #정의 하지 않은 종목이 실시간 데이터 들어오는 경우 실시간 해제
            #self.ocx.dynamicCall("DisconnectRealData(QString)", screen.S0010)
            #self.ocx.dynamicCall("DisconnectRealData(QString)", screen.S0011)
            return

        if subject_code not in calc.data.keys():
            return

        if sRealType == '해외선물시세':
            if d.get_mode() == d.REAL: #실제투자
                current_price = self.ocx.dynamicCall("GetCommRealData(QString, int)", "현재가", 140)    # 140이 뭔지 확인
                current_time = self.ocx.dynamicCall("GetCommRealData(QString, int)", "체결시간", 20)    # 체결시간이 뭔지 확인
            elif d.get_mode() == d.TEST: #테스트
                current_price = sRealData['현재가']    
                current_time = sRealData['체결시간']
                    
            current_price = round(float(current_price), subject.info[subject_code]['자릿수'])

            # 마감시간 임박 계약 청산
            if santa.get_time(3) < int(subject.info[subject_code]['시작시간']) and santa.get_time(3) >= int(subject.info[subject_code]['마감시간']):
                if contract.get_contract_count(subject_code) > 0:
                    log.info('마감시간 임박으로 모든 계약 청산 요청.')
                    if contract.list[subject_code]['매도수구분'] == '신규매도':
                        self.send_order('신규매수', subject_code, contract.get_contract_count(subject_code))
                    elif contract.list[subject_code]['매도수구분'] == '신규매수':
                        self.send_order('신규매도', subject_code, contract.get_contract_count(subject_code))

            subject.info[subject_code]['현재가변동횟수'] += 1 # 시세 조회 횟수 누적

            if self.recent_price[subject_code] != current_price:
                # 청산
                if contract.get_contract_count(subject_code) > 0 and subject.info[subject_code]['상태'] != '청산시도중':
                    sell_contents = None
                    if subject.info[subject_code]['전략'] == '해동이':
                        sell_contents = santa.is_it_sell(subject_code, current_price)
                    elif subject.info[subject_code]['전략'] == '파라':
                        sell_contents = para.is_it_sell(subject_code, current_price)
                    if sell_contents['신규주문'] == True:
                        res.info('주문 체결시간 : ' + str(current_time))
                        order_result = self.send_order(sell_contents['매도수구분'], subject_code, sell_contents['수량'])
                        if d.get_mode() == d.REAL: #실제투자
                            if order_result != 0:
                                log.info(self.parse_error_code(order_result))
                            else:
                                log.info("종목코드 : " + subject_code + ' 상태변경, ' + subject.info[subject_code]['상태'] + ' -> 청산시도중.')
                                subject.info[subject_code]['상태'] = '청산시도중'
                                log.info("%s 종목 %s %s개 청산요청." % (subject_code, sell_contents['매도수구분'], sell_contents['수량']))

                # 신규주문
                #elif contract.get_contract_count(subject_code) == 0 and subject.info[subject_code]['상태'] != '매매시도중' and subject.info[subject_code]['상태'] != '매매완료' and subject.info[subject_code]['상태'] != '청산시도중':
                elif contract.get_contract_count(subject_code) == 0 and subject.info[subject_code]['상태'] != '매매시도중' and subject.info[subject_code]['상태'] != '청산시도중':
                    order_contents = None
                    if subject.info[subject_code]['전략'] == '해동이':
                        order_contents = santa.is_it_OK(subject_code, current_price)
                    elif subject.info[subject_code]['전략'] == '파라':
                        order_contents = para.is_it_OK(subject_code, current_price)
                        #log.info('para.is_it_OK? ' + str(order_contents))
                    if order_contents['신규주문'] == True:
                        
                        res.info('주문 체결시간 : ' + str(current_time))
                        # return value를 리스트로 받아와서 어떻게 사야하는지 확인
                        order_result = self.send_order(order_contents['매도수구분'], subject_code, order_contents['수량'])
                        if d.get_mode() == d.REAL : #실제투자
                            if order_result != 0:
                                log.info(self.parse_error_code(order_result))
                            else:
                                subject.info[subject_code]['주문내용'] = order_contents
                                log.info("종목코드 : " + subject_code + ' 상태변경, ' + subject.info[subject_code]['상태'] + ' -> 매매시도중.')
                                subject.info[subject_code]['상태'] = '매매시도중'
                                log.info("%s 종목 %s %s개 요청." % (subject_code, order_contents['매도수구분'], order_contents['수량']))

                if subject.info[subject_code]['전략'] == '해동이':
                    santa.update_state_by_current_price(subject_code, current_price)

                log.debug("price changed, " + str(self.recent_price[subject_code]) + " -> " + str(current_price))
                self.recent_price[subject_code] = current_price
                if d.get_mode() == d.REAL: #실제투자
                    if subject.info[subject_code]['현재가변동횟수'] >= subject.info[subject_code]['시간단위']:
                        self.request_tick_info(subject_code, subject.info[subject_code]['시간단위'], "")
                        subject.info[subject_code]['현재가변동횟수'] = 0
                calc.show_current_price(subject_code, current_price)
                
        else:
            log.error("OnReceiveRealData : 요청하지 않은 데이터 수신")
            log.error(str(sRealType) + ' / ' + str(subject_code) + ' / ' + str(sRealData))
        

    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList, o_info = None):
        """
        체결데이터를 받은 시점을 알려준다.

        :param sGubun: 체결구분 - 0:주문체결통보, 1:잔고통보, 3:특이신호
        :param nItemCnt: 아이템갯수
        :param sFidList: 데이터리스트 - 데이터 구분은 ‘;’ 이다.
        """

        order_info = {}

        if d.get_mode() == d.REAL: #실제투자
            order_info['주문번호'] = int(self.ocx.dynamicCall("GetChejanData(int)", 9203))        # 주문번호 
            order_info['원주문번호'] = int(self.ocx.dynamicCall("GetChejanData(int)", 904))       # 원주문번호
            order_info['주문유형'] = int(self.ocx.dynamicCall("GetChejanData(int)", 906))         # 주문유형(1 : 시장가, 2 : 지정가, 3 : STOP)
            order_info['종목코드'] = self.ocx.dynamicCall("GetChejanData(int)", 9001)             # 종목코드
            order_info['매도수구분'] = int(self.ocx.dynamicCall("GetChejanData(int)", 907)  )     # 매도수구분(1 : 매도, 2 : 매수)
            order_info['체결표시가격'] = self.ocx.dynamicCall("GetChejanData(int)", 13331)        # 체결표시가격
            order_info['신규수량'] = self.ocx.dynamicCall("GetChejanData(int)", 13327)     # 신규수량
            order_info['청산수량'] = self.ocx.dynamicCall("GetChejanData(int)", 13328)     # 청산수량
            order_info['체결수량'] = self.ocx.dynamicCall("GetChejanData(int)", 911)         # 체결수량
        elif d.get_mode() == d.TEST: # 테스트
            order_info = o_info

        if sGubun == '0':
            # 주문체결통보
            pass

        elif sGubun == '1':
            
            if subject.info[subject_code]['이상신호'] == True:
                log.info(str(subject_code)+"종목 이상신호에 대한 체결로 무시")
                return
            #log.info(order_info)

            log.info(order_info)
            order_info['체결표시가격'] = round( float(order_info['체결표시가격']), subject.info[order_info['종목코드']]['자릿수'])
            log.info('체결잔고')
            #res.info(order_info)
            # 잔고통보

            subject_code = order_info['종목코드']
            add_cnt = int(order_info['신규수량'])
            remove_cnt = int(order_info['청산수량'])

            # 청산
            if remove_cnt > 0:
                # 관리되고 있는 계약이 있으면,
                if subject_code in contract.list:
                    if contract.get_contract_count(subject_code) > 0:
                        profit = 0
                        if order_info['매도수구분'] == 1:
                            profit = ((float(order_info['체결표시가격']) - float(contract.list[subject_code]['체결가'])) / subject.info[subject_code]['단위'] * subject.info[subject_code]['틱가치'] - 15) * remove_cnt
                        elif order_info['매도수구분'] == 2:
                            profit = ((float(contract.list[subject_code]['체결가'] - float(order_info['체결표시가격']))) / subject.info[subject_code]['단위'] * subject.info[subject_code]['틱가치'] - 15) * remove_cnt
                            
                        contract.remove_contract(order_info)
                        
                        subject.info[subject_code]['누적수익'] += round(profit, 1)
                        res.info('누적 수익 : ' + str(subject.info[subject_code]['누적수익']))

                        if subject.info[subject_code]['전략'] == '해동이':
                            if contract.get_contract_count(subject_code) > 0:
                                log.info("종목코드 : " + subject_code + ' 상태변경, ' + subject.info[subject_code]['상태'] + ' -> 매매중.')
                                subject.info[subject_code]['상태'] = '매매중'
                            else:
                                if order_info['매도수구분'] == 1:
                                    if calc.data[subject_code]['추세'][ calc.data[subject_code]['idx']] == '상승세':
                                        log.info("종목코드 : " + subject_code + ' 상태변경, ' + subject.info[subject_code]['상태'] + ' -> 매매완료.')
                                        subject.info[subject_code]['상태'] = '매매완료'
                                    else:
                                        log.info("종목코드 : " + subject_code + ' 상태변경, ' + subject.info[subject_code]['상태'] + ' -> 중립대기.')
                                        subject.info[subject_code]['상태'] = '중립대기'
                                elif order_info['매도수구분'] == 2:
                                    if calc.data[subject_code]['추세'][ calc.data[subject_code]['idx']] == '하락세':
                                        log.info("종목코드 : " + subject_code + ' 상태변경, ' + subject.info[subject_code]['상태'] + ' -> 매매완료.')
                                        subject.info[subject_code]['상태'] = '매매완료'
                                    else:
                                        log.info("종목코드 : " + subject_code + ' 상태변경, ' + subject.info[subject_code]['상태'] + ' -> 중립대기.')
                                        subject.info[subject_code]['상태'] = '중립대기'
                        elif subject.info[subject_code]['전략'] == '파라':
                            if contract.get_contract_count(subject_code) > 0:
                                if order_info['매도수구분'] == 1:
                                    log.info("종목코드 : " + subject_code + ' 상태변경, ' + subject.info[subject_code]['상태'] + ' -> 매수중.')
                                    subject.info[subject_code]['상태'] = '매수중'
                                elif order_info['매도수구분'] == 2:
                                    log.info("종목코드 : " + subject_code + ' 상태변경, ' + subject.info[subject_code]['상태'] + ' -> 매도중.')
                                    subject.info[subject_code]['상태'] = '매도중'
                                pass
                            else:
                                log.info("종목코드 : " + subject_code + ' 상태변경, ' + subject.info[subject_code]['상태'] + ' -> 매매완료.')
                                subject.info[subject_code]['상태'] = '매매완료'

                    else:
                        log.error('관리되지 않은 계약 ' + str(remove_cnt) + '개 청산 됨.')
                else:
                    log.error('관리되지 않은 계약 ' + str(remove_cnt) + '개 청산 됨.')

            # 신규매매
            if add_cnt > 0:
                rtn = contract.add_contract(order_info, subject.info[subject_code]['주문내용'])
                if rtn == False:
                    self.clear_all_subject(subject_code)
                    return

                if order_info['매도수구분'] == 2:
                    log.info("종목코드 : " + subject_code + ' 상태변경, ' + subject.info[subject_code]['상태'] + ' -> 매수중.')
                    subject.info[subject_code]['상태'] = '매수중'
                    log.info("%s 종목 %s개 신규매수." % (subject_code, order_info['신규수량']))
                elif order_info['매도수구분'] == 1:
                    log.info("종목코드 : " + subject_code + ' 상태변경, ' + subject.info[subject_code]['상태'] + ' -> 매도중.')
                    subject.info[subject_code]['상태'] = '매도중'
                    log.info("%s 종목 %s개 신규매도." % (subject_code, order_info['신규수량']))
                

    def OnEventConnect(self, nErrCode):
        """
        통신 연결 상태 변경시 이벤트

        :param nErrCode: 에러 코드 - 0이면 로그인 성공, 음수면 실패, 에러코드 참조
        """
        print("OnEventConnect received")
        
        if nErrCode == 0:
            print("로그인 성공")
            # 계좌번호 저장
            self.account = self.get_login_info("ACCNO")
            log.info("계좌번호 : " + self.account)
            
            # 다이나믹 종목 정보 요청
            #self.get_dynamic_subject_info()
            self.get_dynamic_subject_code()

            # 초기 데이터 요청
            #self.request_tick_info('CLH17', subject.info['CLH17']['시간단위'], "")
            #self.request_tick_info('GCG17', subject.info['GCG17']['시간단위'], "")
            
            # 종목 정보 로그 찍기
            log.info("참여 종목 : %s" % subject.info.values())


        else:
            c_time = "%02d%02d" % (time.localtime().tm_hour, time.localtime().tm_min)

            # 로그인 실패 로그 표시 및 에러코드별 에러내용 발송
            err_msg = "에러코드별 메시지"
            log.critical(err_msg)

            if int(c_time) >= 800 or int(c_time) < 700:
                # 메일 발송
                gmail.send_email('[긴급' + str(c_time) + '] 해동이 작동 중지', '에러코드')

                # 자동이 재시작 로직 작성
                pass

            self.quit()

    ####################################################
    # Custom Methods
    ####################################################

    @staticmethod
    def parse_error_code(err_code):
        """
        Return the message of error codes

        :param err_code: Error Code
        :type err_code: str
        :return: Error Message
        """
        err_code = str(err_code)
        ht = {
            "0": "정상처리",
            "-100": "사용자정보교환에 실패하였습니다. 잠시후 다시 시작하여 주십시오.",
            "-101": "서버 접속 실패",
            "-102": "버전처리가 실패하였습니다.",
            "-200": "시세조회 과부하",
            "-201": "REQUEST_INPUT_st Failed",
            "-202": "요청 전문 작성 실패",
            "-300": "주문 입력값 오류",
            "-301": "계좌비밀번호를 입력하십시오.",
            "-302": "타인계좌는 사용할 수 없습니다.",
            "-303": "주문가격이 20억원을 초과합니다.",
            "-304": "주문가격은 50억원을 초과할 수 없습니다.",
            "-305": "주문수량이 총발행주수의 1%를 초과합니다.",
            "-306": "주문수량은 총발행주수의 3%를 초과할 수 없습니다."
        }
        return ht[err_code] + " (%s)" % err_code if err_code in ht else err_code

    def get_start_time(self, subject_code):
        start_time = int(subject.info[subject_code]['시작시간'])
        end_time = int(subject.info[subject_code]['마감시간'])
        current_hour = time.localtime().tm_hour
        current_min = time.localtime().tm_min
        current_time = current_hour*100 + current_min
        return_time = ''
        if current_time < end_time:
            yesterday = time.localtime(time.time() - 86400)
            mon = yesterday.tm_mon
            if mon < 10:
                mon = '0' + str(mon)
            day = yesterday.tm_mday
            if day < 10:
                day = '0' + str(day)
            return_time = str(yesterday.tm_year) + str(mon) + str(day) + subject.info[subject_code]['시작시간'] + '00'
        elif current_time >= start_time:
            today = time.localtime()
            mon = today.tm_mon
            if mon < 10:
                mon = '0' + str(mon)
            day = today.tm_mday
            if day < 10:
                day = '0' + str(day)
            return_time = str(today.tm_year) + str(mon) + str(day) + subject.info[subject_code]['시작시간'] + '00'

        return return_time
    
    def clear_all_subject(self,subject_code):
        #차후 키움 API를 통해 현재 보유 중인 정확한 계약 수량을 가지고 와서 처리하는 것이 바람직 
        count = contract.get_contract_count(subject_code)
        if count > 0:
            if list[subject_code]['매도수구분'] == '1':
                self.send_order("신규매수", subject_code, count)
            
            elif list[subject_code]['매도수구분'] == '2':
                self.send_order("신규매도", subject_code, count)
            
            contract.delete_contract(subject_code)
            subject.info[subject_code]['상태'] = '중립대기'
            subject.info[subject_code]['이상신호'] = False
                
        
        

            