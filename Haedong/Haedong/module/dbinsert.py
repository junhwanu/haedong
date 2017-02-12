# -*- coding: utf-8 -*-
import sys, time, os, shutil
import gmail, log, calc, santa, screen, db, kiwoom
import json
import subject, contract
import pymysql

from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtWidgets import QApplication


class api():
    app = None
    recent_price = {}
    recent_candle_time = {}
    recent_request_candle_time = 0
    price_changed_cnt = 0
    account = ""
    cnt = 0
    data = []
    start_date = ''
    recent_date = None
    
    def __init__(self):
        super(api, self).__init__()
        self.app = QApplication(sys.argv)

        self.ocx = QAxWidget("KFOPENAPI.KFOpenAPICtrl.1")
        self.ocx.OnEventConnect[int].connect(self.OnEventConnect)
        self.ocx.OnReceiveTrData[str, str, str, str, str].connect(self.OnReceiveTrData)
        self.ocx.OnReceiveChejanData[str, int, str].connect(self.OnReceiveChejanData)
        self.ocx.OnReceiveRealData[str, str, str].connect(self.OnReceiveRealData)
        
        print("�����͸� �о�� �������� �Է��ϼ���. ex)20170125")
        self.start_date = input()
        print(self.start_date)
        if self.connect() == 0:
            self.app.exec_()


    ####################################################
    # Interface Methods
    ####################################################

    def connect(self):
        """
        �α��� �����츦 �����Ѵ�.
        �α����� �����ϰų� �����ϴ� ��� OnEventConnect �̺�Ʈ�� �߻��ϰ� �̺�Ʈ�� ���� ������ �α��� ���� ���θ� �� �� �ִ�.

        :return: 0 - ����, �������� ����
        """

        if self.ocx.dynamicCall("GetConnectState()") == 0:
            rtn = self.ocx.dynamicCall("CommConnect(1)")
            if rtn == 0:
                print("���� ����")
            else:
                print("���� ����")

            return rtn

    def get_login_info(self, sTag):
        """
        �α����� ����� ������ ��ȯ�Ѵ�.

        :param sTag: ����� ���� ���� TAG��
            ��ACCOUNT_CNT�� ? ��ü ���� ������ ��ȯ�Ѵ�.
            "ACCNO" ? ��ü ���¸� ��ȯ�Ѵ�. ���º� ������ ��;���̴�.
            ��USER_ID�� - ����� ID�� ��ȯ�Ѵ�.
            ��USER_NAME�� ? ����ڸ��� ��ȯ�Ѵ�.
            ��KEY_BSECGB�� ? Ű���庸�� ��������. 0:����, 1:����
            ��FIREW_SECGB�� ? ��ȭ�� ���� ����. 0:�̼���, 1:����, 2:����
            Ex) openApi.GetLoginInfo(��ACCOUNT_CNT��);
        :return: TAG���� ���� ������ ��ȯ
        """
        return self.ocx.dynamicCall("GetLoginInfo(QString)", [sTag]).rstrip(';')
    
    def get_dynamic_subject_info(self):
        self.get_dynamic_subject_code()
        self.get_dynamic_subject_market_time()
    
    def get_dynamic_subject_code(self):
        lists = ['MTL','ENG','CUR','IDX','CMD']
        for list in lists:
            self.set_input_value("��ǰ�ڵ�", list)
            self.comm_rq_data("��ǰ�����簡��ȸ", "opt10006", "", screen.S0010)
            time.sleep(0.5)
        
    def get_dynamic_subject_market_time(self):
        lists = ['MTL','ENG','CUR','IDX','CMD']
        for list in lists:
            self.set_input_value("ǰ�񱸺�", list)
            self.comm_rq_data("��������ȸ", "opw50001", "", screen.S0011)
            time.sleep(0.5)
        

    def send_order(self, contract_type, subject_code, contract_cnt):
        
        """
        �ֽ� �ֹ��� ������ �����Ѵ�.
        �űԸż�:self.send_order("�űԸż�","0101",my_account_number,1,subject_code,1,now_current_price,"","2","")
           

        �űԸŵ�:
        �ż�û��:
       �ŵ�û��:self.send_order("�űԸż�","0101",my_account_number,2,subject_code,subject_info[subject_code]['��������'],now_current_price,"2","")
       
 
        :param sRQName: ����� ���� ��û ��
        :param sScreenNo: ȭ���ȣ[4]
        :param sAccNo: ���¹�ȣ[10]
        :param nOrderType: �ֹ����� (1:�űԸż�, 2:�űԸŵ�, 3:�ż����, 4:�ŵ����, 5:�ż�����, 6:�� ������)
        :param sCode: �ֽ������ڵ�
        :param nQty: �ֹ�����
        :param sPrice: �ֹ��ܰ�
        :param sStop: ��ž�ܰ�
        :param sHogaGb: �ŷ����� 1:���尡, 2:������, 3:STOP, 4:STOP LIMIT
            
            �� ���尡, ������������, �ֿ켱������, ���尡IOC, ������IOC, ���尡FOK, ������FOK, �����ð���, ���Ľð��� �ֹ��� �ֹ������� �Է����� �ʽ��ϴ�.
            ex)
            ������ �ż� - openApi.SendOrder(��RQ_1��, ��0101��, ��5015123410��, 1, ��000660��, 10, 48500, ��00��, ����);
            ���尡 �ż� - openApi.SendOrder(��RQ_1��, ��0101��, ��5015123410��, 1, ��000660��, 10, 0, ��03��, ����);
            �ż� ���� - openApi.SendOrder(��RQ_1��,��0101��, ��5015123410��, 5, ��000660��, 10, 49500, ��00��, ��1��);
            �ż� ��� - openApi.SendOrder(��RQ_1��, ��0101��, ��5015123410��, 3, ��000660��, 10, 0, ��00��, ��2��);
        :param sOrgOrderNo: ���ֹ���ȣ
        :return: �����ڵ� - parse_error_code
            -201     : �ֹ������� 
            -300     : �ֹ��Է°� ����
            -301     : ���º�й�ȣ�� �Է��Ͻʽÿ�.
            -302     : Ÿ�� ���¸� ����� �� �����ϴ�.
            -303     : ���-�ֹ����� 200�� �ʰ�
            -304     : ����-�ֹ����� 400�� �ʰ�

        """
        _contract_type = 0
        if contract_type == '�űԸż�':
            _contract_type = 2
        elif contract_type == '�űԸŵ�':
            _contract_type = 1
        else: return -300

        return self.ocx.dynamicCall("SendOrder(QString, QString, QString, int, QString, int, QString, QString, QString, QString)",
                                    [contract_type, '0101', self.account, _contract_type, subject_code, contract_cnt, '0', '0', '1', ''])

    def request_tick_info(self, subject_code, tick_unit, prevNext):

        self.set_input_value("�����ڵ�", subject_code)
        self.set_input_value("�ð�����", tick_unit)
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
        rtn = self.comm_rq_data("�ؿܼ����ɼ�ƽ�׷�����ȸ","opc10001", prevNext, subject.info[subject_code]['ȭ���ȣ'])

        if rtn != 0:
            # �����ڵ庰 �α�
            log.error(self.parse_error_code(rtn))
            
        while rtn == -200:
            time.sleep(0.05)
            rtn = self.comm_rq_data("�ؿܼ����ɼ�ƽ�׷�����ȸ","opc10001", prevNext, subject.info[subject_code]['ȭ���ȣ'])
        

    def set_input_value(self, sID, sValue):
        """
        Tran �Է� ���� ������� ���� �Է��Ѵ�.

        :param sID: �����۸�
        :param sValue: �Է� ��
        Ex) openApi.SetInputValue(�������ڵ塱, ��000660��);
            openApi.SetInputValue(�����¹�ȣ��, ��5015123401��);
        """
        self.ocx.dynamicCall("SetInputValue(QString, QString)", sID, sValue)

    def comm_rq_data(self, sRQName, sTrCode, nPrevNext, sScreenNo):
        """
        Tran�� ������ �۽��Ѵ�.

        :param sRQName: ����ڱ��� ��
        :param sTrCode: Tran�� �Է�
        :param nPrevNext: 0:��ȸ, 2:����
        :param sScreenNo: 4�ڸ��� ȭ���ȣ
        Ex) openApi.CommRqData( ��RQ_1��, ��OPT00001��, 0, ��0101��);
        :return:
        OP_ERR_SISE_OVERFLOW ? ������ �ü���ȸ�� ���� ��źҰ�
        OP_ERR_RQ_STRUCT_FAIL ? �Է� ����ü ���� ����
        OP_ERR_RQ_STRING_FAIL ? ��û���� �ۼ� ����
        OP_ERR_NONE(0) ? ����ó��
        """
        return self.ocx.dynamicCall("CommRqData(QString, QString, QString, QString)", sRQName, sTrCode, nPrevNext, sScreenNo)

    def quit(self):
        """ Quit the server """

        QApplication.quit()
        sys.exit()  

    ####################################################
    # Control Event Handlers
    ####################################################

    def OnReceiveTrData(self, sScrNo, sRQName, sTrCode, sRecordName, sPreNext):
        """
        Tran ���Ž� �̺�Ʈ
        ������� �� �����͸� ���� ������ �˷��ش�.

        :param py: ȭ���ȣ
        :param sRQName: ����ڱ��� ��
        :param sTrCode: Tran ��
        :param sRecordName: Record ��
        :param sPreNext: ������ȸ ����
        :param nDataLength: 1.0.0.1 ���� ���� ������� ����.
        :param sErrorCode: 1.0.0.1 ���� ���� ������� ����.
        :param sMessage: 1.0.0.1 ���� ���� ������� ����.
        :param sSplmMsg: 1.0.0.1 ���� ���� ������� ����.
        """
        
        price = {}
        now_time = time.localtime()
        today_time = "%04d%02d%02d" % (now_time.tm_year, now_time.tm_mon, now_time.tm_mday)
        
        if sRQName == "�ؿܼ����ɼ�ƽ�׷�����ȸ":
            for subject_code in subject.info.keys():
                if sScrNo == subject.info[subject_code]['ȭ���ȣ']:                    
                    # �ʱ� ������ ����
                    _data = self.ocx.dynamicCall("GetCommFullData(QString, QString, int)", sTrCode, sRecordName, 0)
                    _data = _data.split()
                    
                    if self.recent_date == None:
                        self.recent_date = _data[6]

                    if int(self.recent_date) < int(_data[6]):
                        # �Է��� �������� �� �����͸� �޾ƿ����� �ϴ°�!!(2��ġ �������� ���Ǿ���)
                        log.info('self.recent_date' + self.recent_date)
                        log.info('�������� : ' + str(_data[6]))
                        self.data.reverse()
                        log.debug(self.start_date)
                        db.insert(self.data, self.start_date, subject_code)
                        break
#                     print('today_time',today_time)
                    if int(_data[6]) <= int (today_time):
                        self.recent_date = str(_data[6])
                        self.data.extend(_data)
                        #self.data.append(_data)
                    
                    log.info("recent date is " + _data[6])    
                    log.info('ü��ð� : int(_data[2])   ' + _data[2])
                    log.info('���簡 : ' + _data[0])
                    log.info('self.data.__len__()' + str(len(self.data)))
                    
                    if int(_data[2][:12]) < int(self.start_date + subject.info[subject_code]['���۽ð�']):
                        # �Է��� �������� �� �����͸� �޾ƿ����� �ϴ°�!!
                        log.info('���������Դϴ� : ' + str(_data[6]))
                        self.data.reverse()
                        log.debug(self.start_date)
                        db.insert(self.data, self.start_date, subject_code)
                    else:
                        time.sleep(0.2)
                        self.request_tick_info(subject_code,1, sPreNext)    
                          
                break
                
        if sRQName == '��ǰ�����簡��ȸ':
            
            for i in range(20):
                
                subject_code = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, '�����ڵ�n').strip() #���簡 = ƽ�� ����
                subject_symbol = subject_code[:2] 
                if subject_symbol in subject.info.keys():
                    log.info("���� %s�� �����ڵ�� %s �Դϴ�." % (subject.info[subject_symbol]["�����"],subject_code))
                    subject.info[subject_code] = subject.info[subject_symbol]
                    del subject.info[subject_symbol]
                    
                    # �ʱ� ������ ��û
                    self.request_tick_info(subject_code,1, "")
                    self.recent_request_candle_time = time.time()
        
        if sRQName == "��������ȸ":
            
            log.info("��������ȸ")
            for i in range(20):
                subject_code = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, '�Ļ�ǰ���ڵ�')
                market_time1 = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, '���ð�1')
                market_time2 = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, '���ð�2')
                market_time3 = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, '���ð�3')
                market_time4 = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", sTrCode, sRecordName, i, '���ð�4')
                
                log.info(subject_code)
                log.info(market_time1)
                log.info(market_time2)
                log.info(market_time3)
                log.info(market_time4)
            
    def OnReceiveRealData(self, sSubjectCode, sRealType, sRealData):
        """
        �ǽð� �ü� �̺�Ʈ
        �ǽð������͸� ���� ������ �˷��ش�.

        :param sSubjectCode: �����ڵ�
        :param sRealType: ����Ÿ��
        :param sRealData: �ǽð� ����������
        """
        # ĵ�� ����� ���� Ȯ���ؼ� ������ �ȹٲ� �������� 3ƽ���� ������ ��� ���ݺ������� ĵ���� ����� ��찡 ������ request_tick_info ���� Ȯ��
        
        #log.debug("OnReceiveRealData entered.")
        if sSubjectCode[:2] not in subject.info.keys(): #���� ���� ���� ������ �ǽð� ������ ������ ��� �ǽð� ����
            self.ocx.dynamicCall("DisconnectRealData(QString)", screen.S0010)
            self.ocx.dynamicCall("DisconnectRealData(QString)", screen.S0011)
            
        pass
        

    def OnReceiveChejanData(self, sGubun, nItemCnt, sFidList):
        """
        ü�ᵥ���͸� ���� ������ �˷��ش�.

        :param sGubun: ü�ᱸ�� - 0:�ֹ�ü���뺸, 1:�ܰ��뺸, 3:Ư�̽�ȣ
        :param nItemCnt: �����۰���
        :param sFidList: �����͸���Ʈ - ������ ������ ��;�� �̴�.
        """
        pass

    def OnEventConnect(self, nErrCode):
        """
        ��� ���� ���� ����� �̺�Ʈ

        :param nErrCode: ���� �ڵ� - 0�̸� �α��� ����, ������ ����, �����ڵ� ����
        """
        print("OnEventConnect received")
        
        if nErrCode == 0:
            print("�α��� ����")
            # ���¹�ȣ ����
            self.account = self.get_login_info("ACCNO")
            log.info("���¹�ȣ : " + self.account)
            
            # ���̳��� ���� ���� ��û
            #self.get_dynamic_subject_info()
            self.get_dynamic_subject_code()

            # �ʱ� ������ ��û
            #self.request_tick_info('CLH17', subject.info['CLH17']['�ð�����'], "")
            #self.request_tick_info('GCG17', subject.info['GCG17']['�ð�����'], "")
            
            # ���� ���� �α� ���
            log.info("���� ���� : %s" % subject.info.values())


        else:
            c_time = "%02d%02d" % (time.localtime().tm_hour, time.localtime().tm_min)

            # �α��� ���� �α� ǥ�� �� �����ڵ庰 �������� �߼�
            err_msg = "�����ڵ庰 �޽���"
            log.critical(err_msg)

            if int(c_time) >= 800 or int(c_time) < 700:
                # ���� �߼�
                gmail.send_email('[���' + str(c_time) + '] �ص��� �۵� ����', '�����ڵ�')

                # �ڵ��� ����� ���� �ۼ�
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
            "0": "����ó��",
            "-100": "�����������ȯ�� �����Ͽ����ϴ�. ����� �ٽ� �����Ͽ� �ֽʽÿ�.",
            "-101": "���� ���� ����",
            "-102": "����ó���� �����Ͽ����ϴ�.",
            "-200": "�ü���ȸ ������",
            "-201": "REQUEST_INPUT_st Failed",
            "-202": "��û ���� �ۼ� ����",
            "-300": "�ֹ� �Է°� ����",
            "-301": "���º�й�ȣ�� �Է��Ͻʽÿ�.",
            "-302": "Ÿ�ΰ��´� ����� �� �����ϴ�.",
            "-303": "�ֹ������� 20����� �ʰ��մϴ�.",
            "-304": "�ֹ������� 50����� �ʰ��� �� �����ϴ�.",
            "-305": "�ֹ������� �ѹ����ּ��� 1%�� �ʰ��մϴ�.",
            "-306": "�ֹ������� �ѹ����ּ��� 3%�� �ʰ��� �� �����ϴ�."
        }
        return ht[err_code] + " (%s)" % err_code if err_code in ht else err_code

    def get_today_date(self):
        ret = ''
        ret += str(time.localtime().tm_year)
        if time.localtime().tm_mon < 10:
            ret += '0'
        ret += str(time.localtime().tm_mon)
        if time.localtime().tm_mday < 10:
            ret += '0'
        ret += str(time.localtime().tm_mday)

        return ret

    def get_start_time(self, subject_code):
        start_time = int(subject.info[subject_code]['���۽ð�'])
        end_time = int(subject.info[subject_code]['�����ð�'])
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
            return_time = str(yesterday.tm_year) + str(mon) + str(day) + subject.info[subject_code]['���۽ð�'] + '00'
        elif current_time >= start_time:
            today = time.localtime()
            mon = today.tm_mon
            if mon < 10:
                mon = '0' + str(mon)
            day = today.tm_mday
            if day < 10:
                day = '0' + str(day)
            return_time = str(today.tm_year) + str(mon) + str(day) + subject.info[subject_code]['���۽ð�'] + '00'

        return return_time