import tkinter
import socket, threading
import json
from tkinter import filedialog
import time
import os
import sys

win = tkinter.Tk()  # 创建主窗口
win.title('模拟服务器')
win.geometry("400x400+200+20")
users = {}  # 用户字典，也可以连接数据库
ipStr = "127.0.0.1"
PORT = 8080

class ChatServer(threading.Thread):

    def __init__(self, port = 8080):
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
    def connect(self, ck, ca):
        userName = ck.recv(1024)
        userName = userName.decode('utf-8')
        users[userName] = ck
        print(users)
        printStr = "" + userName + "连接ChatServer\n"
        text.insert(tkinter.INSERT, printStr)

        # 在线列表
        listbox.delete(0, tkinter.END)
        listbox.insert(tkinter.END, '在线列表')
        for k in users.keys():
            listbox.insert(tkinter.END, k)

        while True:
            data = ck.recv(1024)
            data = data.decode('utf-8')
            if data[0] == '#':
                name = data.split(' ')[1]
                fileName = r'./cache/' + name
                with open(fileName, 'wb') as f:
                    while True:
                        data2 = ck.recv(1024)
                        if data2 == 'EOF'.encode('utf-8'):
                            break
                        f.write(data2)
                        data2 = ''
                    f.close()
                friendList = ck.recv(1024)
                userStr = ck.recv(1024)
                userStr = userStr.decode('utf-8')
                time.sleep(0.1)
                # if mes[0] == '``#'.encode():
                #     break
                print(friendList.decode('utf-8'))
                friendList = friendList.decode('utf-8')
                friendList = friendList.split(" ")
                # print('列表 ：' + friendList)
                print('文件名： ' + name + ' ' + userStr)
                fileName = './cache/' + name
                for friend in friendList:
                    users[friend].send(('# ' + name + ' ' + userStr).encode())
                with open(fileName, 'rb') as f:
                    while True:
                        a = f.read(1024)
                        if not a:
                            break
                        for fd in friendList:
                            users[fd].send(a)
                        a = ''
                    f.close()
                time.sleep(0.1)
                for friend in friendList:
                    print(friend + '已发送EOF')
                    users[friend].send(('EOF').encode('utf-8'))
                print('发送文件')
            elif data[0] == '`':
                name = data.split(' ')[1]
                fileName = r'./cache/' + name
                with open(fileName, 'wb') as f:
                    while True:
                        data2 = ck.recv(1024)
                        if data2 == 'EOF'.encode('utf-8'):
                            break
                        f.write(data2)
                        data2 = ''
                    f.close()
                friendList = ck.recv(1024)
                userStr = ck.recv(1024)
                userStr = userStr.decode('utf-8')
                time.sleep(0.1)
                # if mes[0] == '``#'.encode():
                #     break
                print(friendList.decode('utf-8'))
                friendList = friendList.decode('utf-8')
                friendList = friendList.split(" ")
                # print('列表 ：' + friendList)
                print('文件名： ' + name + userStr)
                fileName = './cache/' + name
                users[userName].send(('` ' + name + ' ' + userStr).encode())
                for friend in friendList:
                    users[friend].send(('` ' + name + ' ' + userStr).encode())
                with open(fileName, 'rb') as f:
                    while True:
                        a = f.read(1024)
                        if not a:
                            break
                        users[userName].send(a)
                        for fd in friendList:
                            users[fd].send(a)

                        a = ''
                    f.close()
                time.sleep(0.1)
                users[userName].send(('EOF').encode('utf-8'))
                for friend in friendList:
                    print(friend + '已发送EOF')
                    users[friend].send(('EOF').encode('utf-8'))
                print('发送图片')
            elif data[0] == '!':
                name = data.split(' ')[1]
                del users[name]
                # 在线列表
                listbox.delete(0, tkinter.END)
                listbox.insert(tkinter.END, '在线列表')
                for k in users.keys():
                    listbox.insert(tkinter.END, k)
                printStr = "" + userName + "断开连接\n"
                text.insert(tkinter.INSERT, printStr)

            else:

                infolist = data.split(":")
                friendList = infolist[0].split(" ")
                print(123)
                for friend in friendList:
                    users[friend].send((userName + ":" + infolist[1]).encode('utf-8'))

    def run(self):
        self.s.bind((ipStr, int(self.port)))
        self.s.listen(10)
        printStr = "ChatServer启动成功\n"
        text.insert(tkinter.INSERT, printStr)
        while True:
            ck, ca = self.s.accept()
            t = threading.Thread(target = self.connect, args = (ck, ca))
            t.start()
        self.s.close()



if __name__ == '__main__':
    global text
    text = tkinter.Text(win)
    text.place(x = 0, y = 30, width = 270, height = 350)


    cserver = ChatServer(PORT)
    cserver.start()

    labeltext = tkinter.Label(win, text='连接消息')
    labeltext.place(x = 0, y = 0, width = 60, height = 30)

    # 在线列表
    listbox = tkinter.Listbox(win)
    listbox.place(x=270, y=30, width=130, height=350)

    win.mainloop()



