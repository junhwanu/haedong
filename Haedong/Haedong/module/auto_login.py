import threading
import time
import psutil
import pywinauto
import configparser
import os


class Login(threading.Thread):
    USER_ID = 'id'
    USER_PASSWD = 'passwd'
    AUTH_PASSWD = 'passwd'

    LOGIN_PNAME = ["kfstarter.exe", "KFStarter.exe"]
    LOGIN_PID = 0
    REAL_INVEST = False
    AUTO_LOGIN = True

    def __init__(self):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False

        # 사용자 계정 정보 Config 읽기
        config = configparser.RawConfigParser()
        config.read(os.path.dirname(os.path.abspath(__file__).replace('\\','/')) + '/../config/user.cfg')

        # config file searching
        if config.has_section('AUTO_LOGIN_CONFIG'):

            if config.BOOLEAN_STATES.get(config.get('AUTO_LOGIN_CONFIG', 'AUTO_LOGIN_ENABLE')) :
                self.AUTO_LOGIN = True
                self.USER_ID = config.get('AUTO_LOGIN_CONFIG', 'USER_ID')
                self.USER_PASSWD = config.get('AUTO_LOGIN_CONFIG', 'USER_PASSWD')
                self.AUTH_PASSWD = config.get('AUTO_LOGIN_CONFIG', 'AUTH_PASSWD')

                # 실제 투자 / 모의투자
                if config.BOOLEAN_STATES.get(config.get('AUTO_LOGIN_CONFIG', 'REAL_INVEST_FLAG')):
                    self.REAL_INVEST = True
                else:
                    self.REAL_INVEST = False

            else :
                self.AUTO_LOGIN = False

        else :
            print('Auto Login Config File을 찾을 수 없습니다.')
            self.AUTO_LOGIN = False
            time.sleep(1)

    def run(self):
        if self.AUTO_LOGIN is False :
            print("자동 로그인을 사용하지 않습니다.")
            return

        if self.REAL_INVEST :
            print("실제 투자용 자동 로그인")
        else :
            print("모의 투자용 자동 로그인")

        time.sleep(3)

        looping_flag = True
        while looping_flag:
            for proc in psutil.process_iter():
                if proc.name() in self.LOGIN_PNAME:
                    self.LOGIN_PID = proc.pid
                    print('로그인 프로그램 pid(%d)' % self.LOGIN_PID)
                    looping_flag = False

            if looping_flag :
                print("로그인 프로그램을 찾는 중입니다.")
                time.sleep(5)

        app = pywinauto.Application().connect(process=self.LOGIN_PID)

        title = "영웅문W Login"
        dlg = pywinauto.timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))

        try :
            dlg.Edit1.SetFocus()
        except pywinauto.findwindows.ElementNotFoundError as err :
            time.sleep(3)
            print("로그인 윈도우를 찾지 못했습니다. 5초후 재시도")

        user_id = dlg.Edit1
        user_id.SetFocus()
        user_id.TypeKeys(self.USER_ID)
        print('키움 사용자 ID(%s)' % self.USER_ID)

        user_passwd = dlg.Edit2
        user_passwd.SetFocus()
        user_passwd.TypeKeys(self.USER_PASSWD)
        print('키움 사용자 PASSWORD(%s)' % self.USER_PASSWD)

        # 모의투자
        if self.REAL_INVEST :
            auth_passwd = dlg.Edit3
            auth_passwd.SetFocus()
            auth_passwd.TypeKeys(self.AUTH_PASSWD)
            print('공인인증서 PASSWORD(%s)' % self.AUTH_PASSWD)

        login_button = dlg.Button0
        login_button.Click()

        time.sleep(10)

        print("Auto Login Thread 종료")
        # self.account_password_setup()

if __name__ == '__main__':
    login = Login()
    login.start()