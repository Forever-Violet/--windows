import sys
import os
import requests
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import win32api
import win32con
sys.setrecursionlimit(1000000)

# 进入虚拟环境 pipenv shell 再打包成exe
class MyWindow(QWidget):
    service = 1
    user = 0
    password = 0
    auto_flag = '0'

    def __init__(self):
        super().__init__()
        self.setWindowTitle("校园网快捷登录(〃'▽'〃)")
        self.resize(400, 300)
        self.setWindowOpacity(0.90)  # 设置窗口透明度
         # 加了self为全局布局，没加为局部布局
        l1 = QLabel("用户名:")
        nm = QLineEdit()
        fbox = QFormLayout()
        fbox.addRow(l1, nm)
        l2 = QLabel("密  码:")
        add1 = QLineEdit()
        vbox = QVBoxLayout()
        vbox.addWidget(add1)
        fbox.addRow(l2, vbox)

        key_name = r'Software\\fastLogin'
        try:
            key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, key_name)  # 进入父健
            while True:
                try:
                    self.user = win32api.RegQueryValueEx(key, 'username')
                    self.password = win32api.RegQueryValueEx(key, 'password')
                    self.service = win32api.RegQueryValueEx(key, 'service')
                    self.auto_flag = win32api.RegQueryValueEx(key, 'auto_flag')
                    self.user = list(self.user)  # 元组类型转为list才能修改
                    self.password = list(self.password)
                    self.service = list(self.service)
                    self.auto_flag = list(self.auto_flag)
                    break
                except:
                    win32api.RegSetValueEx(key, 'username', 1, win32con.REG_SZ, '首次使用请点击断连, 然后点击登录以验证信息是否正确')
                    win32api.RegSetValueEx(key, 'password', 1, win32con.REG_SZ, '请输入密码')
                    win32api.RegSetValueEx(key, 'service', 1, win32con.REG_SZ, '1')
                    win32api.RegSetValueEx(key, 'auto_flag', 1, win32con.REG_SZ, '0')
            win32api.RegCloseKey(key)
        except:
            print('\33[1;36merror！')
        print('\33[1;36msuccess！')
        nm.setText(self.user[0])  # 获取用户名
        add1.setText(self.password[0])  # 获取密码

        nm.editingFinished.connect(lambda :self.change_user(nm))
        add1.editingFinished.connect(lambda :self.change_pwd(add1))

        r1 = QRadioButton("移动")
        if self.service[0] == '1':
            r1.setChecked(True)
        r2 = QRadioButton("联通")
        if self.service[0] == '2':
            r2.setChecked(True)
        r3 = QRadioButton("电信")
        if self.service[0] == '3':
            r3.setChecked(True)
        r1.clicked.connect(lambda: self.change_service(r1))
        r2.clicked.connect(lambda: self.change_service(r2))
        r3.clicked.connect(lambda: self.change_service(r3))
        hbox = QHBoxLayout()
        hbox.addWidget(r1)
        hbox.addWidget(r2)
        hbox.addWidget(r3)
        hbox.addStretch()

        fbox.addRow(QLabel("运营商:"), hbox)
        b1 = QPushButton("登录")
        b2 = QPushButton("断连")
        fbox.addRow(b1)
        fbox.addRow(b2)
        b3 = QPushButton("卸载记录(删除在注册表记录的信息)")
        fbox.addRow(b3)
        b4 = QPushButton("验证网络是否连通")
        fbox.addRow(b4)
        b1.clicked.connect(self.login)  # 点击登录按钮
        b2.clicked.connect(self.logout)  # 点击断连按钮
        b3.clicked.connect(self.delete_data)  # 点击卸载按钮
        b4.clicked.connect(self.ping)  # 点击验证网络按钮

        b1.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:25px;height:20px}
        QPushButton:hover{background:green;}''')
        b2.setStyleSheet('''QPushButton{background:#F76677;border-radius:25px;height:20px}
        QPushButton:hover{background:red;}''')
        b3.setStyleSheet('''QPushButton{background:#F7D674;border-radius:25px;height:20px}
        QPushButton:hover{background:yellow;}''')
        b4.setStyleSheet('''QPushButton{background:#F9C6CF;border-radius:25px;height:20px}
        QPushButton:hover{background:pink;}''')
        auto_btn = QCheckBox("开机自启(若在已勾选此选项的情况下移动了本程序的位置, 则需要取消然后再勾选此选项)")
        if self.auto_flag[0] == '1':  # 若已勾选过开机自启
            auto_btn.setChecked(True)
        auto_btn.clicked.connect(lambda: self.change_auto_flag(auto_btn))
        fbox.addRow(auto_btn)
        self.setLayout(fbox)

    # 卸载信息
    def delete_data(self):
        key_name = r'Software'
        KeyName = r'Software\Microsoft\Windows\CurrentVersion\Run'
        try:
            key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, key_name)  # 进入父健
            win32api.RegDeleteKey(key, 'fastLogin')
            win32api.RegCloseKey(key)
            if self.auto_flag[0] == '1':  # 删除开机自启信息
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
                win32api.RegDeleteValue(key, 'fastLogin')  # 删除键值
                win32api.RegCloseKey(key)
            info_box = QMessageBox()
            info_box.setWindowTitle("恭喜!(～￣▽￣)～ ")  # QMessageBox标题
            info_box.setText("成功卸载信息!\n若想删除本程序, 请直接将它丢进回收站(*^▽^*)")  # QMessageBox的提示文字
            info_box.setStandardButtons(QMessageBox.Yes)
            info_box.exec_()
        except:
            QMessageBox.critical(self, "出错啦!", "请重试")
            print('\33[1;36merror！')
        print('\33[1;36msuccess！')

    def change_user(self, nm):
        self.user[0] = nm.text()
        key_name = r'Software\\fastLogin'
        try:
            key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, key_name)  # 进入父健
            win32api.RegSetValueEx(key, 'username', 1, win32con.REG_SZ, self.user[0])
            win32api.RegCloseKey(key)
        except:
            print('\33[1;36merror！')
        print('\33[1;36msuccess！')

    def change_pwd(self, add1):
        self.password[0] = add1.text()
        key_name = r'Software\\fastLogin'
        try:
            key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, key_name)  # 进入父健
            win32api.RegSetValueEx(key, 'password', 1, win32con.REG_SZ, self.password[0])
            win32api.RegCloseKey(key)
        except:
            print('\33[1;36merror！')
        print('\33[1;36msuccess！')

    # 更改运营商处理
    def change_service(self, r):
        key_name = r'Software\\fastLogin'
        try:
            key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, key_name)  # 进入父健
            if r.text() == "移动":
                self.service[0] = '1'
                win32api.RegSetValueEx(key, 'service', 1, win32con.REG_SZ, self.service[0])
            elif r.text() == '联通':
                self.service[0] = '2'
                win32api.RegSetValueEx(key, 'service', 1, win32con.REG_SZ, self.service[0])
            elif r.text() == '电信':
                self.service[0] = '3'
                win32api.RegSetValueEx(key, 'service', 1, win32con.REG_SZ, self.service[0])
            win32api.RegCloseKey(key)
        except:
            print('\33[1;36merror！')
        print('\33[1;36msuccess！')

    # 点击开机自启处理 auto_flag处理
    def change_auto_flag(self, flag):
        key_name = r'Software\\fastLogin'
        if flag.isChecked():
            self.auto_flag[0] = '1'
            try:
                key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, key_name)
                win32api.RegSetValueEx(key, 'auto_flag', 1, win32con.REG_SZ, '1')
                win32api.RegCloseKey(key)
            except:
                print('\33[1;36merror！')
            print('\33[1;36msuccess！')

        else:
            self.auto_flag[0] = '0'
            try:
                key = win32api.RegCreateKey(win32con.HKEY_CURRENT_USER, key_name)
                win32api.RegSetValueEx(key, 'auto_flag', 1, win32con.REG_SZ, '0')
                win32api.RegCloseKey(key)
            except:
                print('\33[1;36merror！')
            print('\33[1;36msuccess！')
        self.auto_start_up()

    # 开机自启处理
    def auto_start_up(self):
        name = 'fastLogin'
        if hasattr(sys, 'frozen'):   # 打包成exe后的绝对路径
            path = os.path.realpath(sys.executable)
        elif __file__:  # 作为python文件时的绝对路径
            path = os.path.realpath(os.path.abspath(__file__))
        value = '"'+path+'"'+' autorun'
        KeyName = r'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
        if self.auto_flag[0] == '1':  # 如果选中开机自启
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)  # 进入父健
                win32api.RegSetValueEx(key, name, 1, win32con.REG_SZ, value)  # 创建键
                win32api.RegCloseKey(key)
            except:
                print('\33[1;36merror！')
            print('\33[1;36msuccess！')
        elif self.auto_flag[0] == '0':  # 取消选中
            try:
                key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
                win32api.RegDeleteValue(key, name)  # 删除键值
                win32api.RegCloseKey(key)
            except:
                print('\33[1;36merror！')
            print('\33[1;36msuccess！')

    # 验证登录
    def ping(self):
        cnt = 1
        while True:
            r = os.system('ping -n 2 -l 8 www.baidu.com')  # ping两个8字节数据包 多了慢
            if r:
                cnt += 1
                print("\33[1;36m网络连通失败")
                QMessageBox.critical(self, "出错啦!o(╥﹏╥)o",
                 "出现该错误常见原因如下:\n1.用户名或密码输入错误\n2.选择了错误的运营商\n3.该校园网连接的设备上限了\n4.已连接成功, 请稍等片刻!(〃'▽'〃)")
                if cnt == 2:
                    return False
            else:
                info_box = QMessageBox()
                info_box.setWindowTitle("恭喜(oﾟ▽ﾟ)o  ")  # QMessageBox标题
                info_box.setText("网络正常连通! \n(3秒后自动关闭)")  # QMessageBox的提示文字
                info_box.setStandardButtons(QMessageBox.Ok)
                info_box.button(QMessageBox.Ok).animateClick(3000)  # 3秒后后自动关闭
                info_box.exec_()
                print("\33[1;36m网络正常连通")
                return True

    # 登录函数
    def login(self, event):
        url = 'http://10.10.9.4/eportal/InterFace.do?method=login'
        if self.service[0] == '1':
            s = '%E7%A7%BB%E5%8A%A8'
        elif self.service[0] == '2':
            s = '%E8%81%94%E9%80%9A'
        elif self.service[0] == '3':
            s = '%E7%94%B5%E4%BF%A1'
        data = {
            'userId': self.user[0],
            'password': self.password[0],
            'service': s,
            'queryString': 'wlanuserip%3D2f0c7f6d25d11e1385c70af498077889%26wlanacname%3D451c3f30a97da29045f86d957e89984c%26ssid%3D%26nasip%3D017a864d081217ffa61950f8cb86f6e4%26snmpagentip%3D%26mac%3D4dd78feaa3c341e17c4291eaefb4df3b%26t%3Dwireless-v2%26url%3D2c0328164651e2b4f13b933ddf36628bea622dedcc302b30%26apmac%3D%26nasid%3D451c3f30a97da29045f86d957e89984c%26vid%3D22fde3eefcd4789e%26port%3Ddb52feedfee4bd80%26nasportid%3D5b9da5b08a53a540e26b350a596c2af8e0f8ef9c165ac3524f8c07b8439cc01b',
            'operatorPwd': '',
            'operatorUserId': '',
            'validcode': '',
            'passwordEncrypt': 'false',
        }
        headers = {
            'Host': '10.10.9.4',
            'Origin': 'http://10.10.9.4',
            'Referer': 'http://10.10.9.4/eportal/index.jsp?wlanuserip=2f0c7f6d25d11e1385c70af498077889&wlanacname=451c3f30a97da29045f86d957e89984c&ssid=&nasip=017a864d081217ffa61950f8cb86f6e4&snmpagentip=&mac=4dd78feaa3c341e17c4291eaefb4df3b&t=wireless-v2&url=2c0328164651e2b4f13b933ddf36628bea622dedcc302b30&apmac=&nasid=451c3f30a97da29045f86d957e89984c&vid=22fde3eefcd4789e&port=db52feedfee4bd80&nasportid=5b9da5b08a53a540e26b350a596c2af8e0f8ef9c165ac3524f8c07b8439cc01b',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        flag = 0
        exit_flag = 0
        try:
            response = requests.post(url, data=data, headers=headers).status_code
            """作用是向网页发送请求数据, 且需要提供网址, data和header三个数据"""
            flag = 1 # 请求未出错
            if "{}".format(response) == '200':
                info_box = QMessageBox()
                info_box.setWindowTitle("恭喜(oﾟ▽ﾟ)o  ")  # QMessageBox标题
                info_box.setText("登录请求已发送! 是否继续操作?\n(3秒后自动退出程序)")  # QMessageBox的提示文字
                info_box.addButton(QPushButton('Yes', info_box), QMessageBox.YesRole)
                info_box.setStandardButtons(QMessageBox.No)
                info_box.button(QMessageBox.No).animateClick(3000)  # 3秒后后自动关闭
                api = info_box.exec_()
                if api == 65536:  # 未选择或选择了不继续操作
                    exit_flag = 1
            else:
                QMessageBox.critical(self, "出错啦!o(╥﹏╥)o","出现该错误常见原因如下:\n1. 用户名或密码输入错误\n2. 选择了错误的运营商\n3.该校园网连接的设备上限了\n4.已连接成功, 请稍等片刻!(〃'▽'〃)")
        except:
            if flag == 0:
                QMessageBox.critical(self, "出错啦!o(╥﹏╥)o","请求发送失败, 请尝试重新连接或在认证页面连接..\n(可能wifi或网线未连接到校园网, 导致无法认证)")
            else:
                pass
        if exit_flag == 1:
            sys.exit()


    # 断连函数
    def logout(self, event):
        url = 'http://10.10.9.4/eportal/InterFace.do?method=logout'
        data = {
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        flag = 0
        try:
            response = requests.post(url, data=data, headers=headers).status_code
            """作用是向网页发送请求数据, 且需要提供网址, data和header三个数据"""
            # 一个8字节的数据包
            flag = 1
            if "{}".format(response) == '200':
                info_box = QMessageBox()
                info_box.setWindowTitle("恭喜!")  # QMessageBox标题
                info_box.setText("成功发送请求!(￣▽￣)~*")  # QMessageBox的提示文字
                info_box.setStandardButtons(QMessageBox.Yes)
                info_box.button(QMessageBox.Yes).animateClick(2000)  # 2秒后后自动关闭
                info_box.exec_()
                print("\33[1;36m断连成功")
            else:
                QMessageBox.critical(self, "出错啦!", "请重试(╥╯^╰╥)")
        except:
            if flag == 0:
                QMessageBox.critical(self, "出错啦!", "请重试(╥╯^╰╥)")
            else:
                pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MyWindow()
    # print(str(sys.argv[1:]))
    if not str(sys.argv[1:]) == '[]':
        flag_temp = list(sys.argv[1:])
        flag = flag_temp[0]
        # print(flag)
    else:
        flag = 'xxx'
    if flag == "autorun":  # 如果是开机自启 只显示登录请求窗口
        if not win.user[0] == '首次使用请点击断连, 然后点击登录以验证信息是否正确':  # 判断用户是否第一次使用
            win.login(win)
        win.show()
        sys.exit(app.exec_())
    else:
        win.show()
        if not win.user[0] == '首次使用请点击断连, 然后点击登录以验证信息是否正确':  # 判断用户是否第一次使用
            win.login(win)
        sys.exit(app.exec_())
