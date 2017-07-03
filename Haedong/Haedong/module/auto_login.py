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

    HEADONG_PNAME = ""
    HEADONG_PID = 0
    REAL_INVEST = False

    def __init__(self):
        threading.Thread.__init__(self)
        self.__suspend = False
        self.__exit = False

        self.HEADONG_PNAME = "kfstarter.exe"
        self.HEADONG_PID = 0

        # 사용자 계정 정보 Config 읽기
        config = configparser.RawConfigParser()

        config.read(os.path.dirname(os.path.abspath(__file__).replace('\\','/')) + '/../config/user.cfg')
        print(os.path.dirname(os.path.abspath(__file__).replace('\\','/')) + '/../config/user.cfg')

        if config.has_section('user_account') and config.has_section('test_config'):
            self.USER_ID = config.get('user_account', 'userid')
            self.USER_PASSWD = config.get('user_account', 'userpasswd')
            self.AUTH_PASSWD = config.get('user_account', 'authpasswd')

            # 실제 투자 / 모의투자
            real_flag = config.get('test_config', 'real_invest_flag')
            if real_flag == 'y':
                self.REAL_INVEST = True
                print("실제 투자용 자동 로그인")
            else:
                self.REAL_INVEST = False
                print("모의 투자용 자동 로그인")

        else :
            print("Config file을 찾을 수 없습니다.")

    def run(self):
        time.sleep(3)

        looping_flag = True
        while looping_flag:
            for proc in psutil.process_iter():
                if proc.name() == self.HEADONG_PNAME:
                    self.HEADONG_PID = proc.pid
                    print('로그인 프로그램 pid(%d)' % self.HEADONG_PID)
                    looping_flag = False

            if looping_flag is True:
                print("로그인 프로그램을 찾을 수 없습니다. 3초 후 다시 검색합니다.")
                time.sleep(3)

        app = pywinauto.Application().connect(process=self.HEADONG_PID)

        title = "영웅문W Login"
        dlg = pywinauto.timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))

        user_id = dlg.Edit1
        user_id.SetFocus()
        user_id.TypeKeys(self.USER_ID)
        print('키움 사용자 ID(%s)' % self.USER_ID)

        user_passwd = dlg.Edit2
        user_passwd.SetFocus()
        user_passwd.TypeKeys(self.USER_PASSWD)
        print('키움 사용자 PASSWORD(%s)' % self.USER_PASSWD)

        # 모의투자
        if self.REAL_INVEST is True:
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