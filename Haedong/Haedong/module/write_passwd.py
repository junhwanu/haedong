import time
import psutil
import pywinauto
import pyautogui

AUTH_PASSWD = '0000'


KFOPCOM_PNAME = ["kfopcomms.exe", "kfopcomms.exe"]
PYTHON_PNAME = "python.exe"
KFOPCOM_PID = 0


def write_passwd() :
    while True:
        print('트레이 아이콘을 찾는 중입니다.')
        트레이아이콘 = pyautogui.locateCenterOnScreen('kf.png', grayscale=True)
        if 트레이아이콘 :
            print('트레이 아이콘을 찾았습니다.')
            print(트레이아이콘)
            x, y = 트레이아이콘
            print(x, y)
            pyautogui.click(x, y, button='right')
            break

    time.sleep(3)
    # 등록 버튼 누르기
    print('등록버튼 누르기')
    pyautogui.moveRel(10, -35)
    pyautogui.click()

    time.sleep(3)

    looping_flag = True

    while looping_flag:
        for proc in psutil.process_iter():
            if proc.name() in PYTHON_PNAME:
                KFOPCOM_PID = proc.pid
                print('거래 프로그램 pid(%d)' % KFOPCOM_PID)
                looping_flag = False

        if looping_flag:
            print("거래 프로그램을 찾는 중입니다.")
            time.sleep(5)

    time.sleep(5)

    app = pywinauto.Application().connect(process=KFOPCOM_PID)
    title = "계좌번호관리"
    dlg = pywinauto.timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))
    app.window_().print_control_identifiers()


    비밀번호 = '0000'
    비밀번호수정 = dlg.Edit1
    비밀번호수정.SetFocus()
    비밀번호수정.Click()
    비밀번호수정.TypeKeys(비밀번호)
    print(비밀번호)

    time.sleep(0.5)

    일괄저장버튼 = dlg.Button3
    일괄저장버튼.Click()

    time.sleep(0.5)

    닫기버튼 = dlg.Button2
    닫기버튼.Click()

    return

            # a
            #
            #
            # dlg = pywinauto.timings.WaitUntilPasses(20, 0.5, lambda: app.window_(title=title))
            #
            # try:
            #     dlg.Edit1.SetFocus()
            # except pywinauto.findwindows.ElementNotFoundError as err:
            #     time.sleep(3)
            #     print("로그인 윈도우를 찾지 못했습니다. 5초후 재시도")
            #
            # user_id = dlg.Edit1
            # user_id.SetFocus()
            # user_id.TypeKeys(self.USER_ID)
            # print('키움 사용자 ID(%s)' % self.USER_ID)
            #
            # user_passwd = dlg.Edit2
            # user_passwd.SetFocus()
            # user_passwd.TypeKeys(self.USER_PASSWD)
            # print('키움 사용자 PASSWORD(%s)' % self.USER_PASSWD)
            #
            # # 모의투자
            # if self.REAL_INVEST:
            #     auth_passwd = dlg.Edit3
            #     auth_passwd.SetFocus()
            #     auth_passwd.TypeKeys(self.AUTH_PASSWD)
            #     print('공인인증서 PASSWORD(%s)' % self.AUTH_PASSWD)
            #
            # login_button = dlg.Button0
            # login_button.Click()
            #
            # time.sleep(10)
            #
            # print("Auto Login Thread 종료")
            # # self.account_password_setup()

if __name__ == '__main__':
    write_passwd()
