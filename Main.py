from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import requests
import json

CLIENT_ID = '1bf80eba491150561ba72093ebac49b3'
REDIRECT_URL = 'http://52.79.237.120:5000/kakao_oauth'

GET_KAKAO_AUTHENTICATION_CODE = 'https://kauth.kakao.com/oauth/authorize?client_id=' + CLIENT_ID + \
                                '&redirect_uri=' + REDIRECT_URL + '&response_type=code'


class BrowserWindow(QMainWindow):

    def __init__(self, parent=None):
        super(BrowserWindow, self).__init__(parent)
        self.setWindowTitle("두번째 화면")
        # setGeometry(int x, int y, int width, int height)
        self.setGeometry(800, 500, 400, 650)
        self.form_widget = FormWidget(self)
        self.setCentralWidget(self.form_widget)


def get_access_token(code):
    try:
        print("kakao code: " + code)
        url = "https://kauth.kakao.com/oauth/token"
        payload ={"grant_type": "authorization_code", "client_id": CLIENT_ID, "redirect_uri": REDIRECT_URL, "code": code}

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",

        }

        response = requests.request("POST", url, data=payload, headers=headers)



        access_token = json.loads(((response.text).encode('utf-8')))['access_token']
        print("access token: " + access_token)


        url = "https://kapi.kakao.com/v1/user/signup"

        headers.update({'Authorization':"Bearer " + access_token})

        response = requests.request("POST", url, headers=headers)

        print("signup response: " + response.text)


        url = "https://kapi.kakao.com/v1/user/me"

        response = requests.request("POST", url, headers=headers)

        print("me response: " + response.text)

    except Exception as ex:
        print(ex)



class FormWidget(QWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        self.browser = QWebEngineView(self)

        # print(os.path.split(os.path.abspath(__file__))[0])

        # 아래 방법으로 해야 로컬컴퓨터에 저장된  html파일을 읽을 수 있음
        # self.browser.load(QtCore.QUrl().fromLocalFile(
        #     os.path.split(os.path.abspath(__file__))[0] + '/index.html'
        # ))

        self.browser.setUrl(QUrl(GET_KAKAO_AUTHENTICATION_CODE))
        # 페이지 로딩이 끝나면 돔 트리 구성
        self.browser.loadFinished.connect(self.load_finished)

        self.layout.addWidget(self.browser)
        self.setLayout(self.layout)

    def get_response(self, text):
        print(text)

    def load_finished(self):
        print("load_finished")
        page = self.browser.page()

        # TODO 수정하세요
        page.toPlainText(lambda code: get_access_token(code))


class Manager:
    def __init__(self):
        self.window = BrowserWindow()

        self.window.show()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    manager = Manager()
    sys.exit(app.exec_())