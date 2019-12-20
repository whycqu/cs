import socket, threading
import json
import time
import os
import sys


users = {}  # 用户字典，也可以连接数据库
ipStr = "193.112.241.197"
PORT = 80

class ChatServer(threading.Thread):

    def __init__(self, port = 80):
        super().__init__()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = port
    def connect(self, ck, ca):
        userName = ck.recv(1024)
        userName = userName.decode('utf-8')
        users[userName] = ck
        print(users)


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
        while True:
            ck, ca = self.s.accept()
            t = threading.Thread(target = self.connect, args = (ck, ca))
            t.start()
        self.s.close()



if __name__ == '__main__':


    cserver = ChatServer(PORT)
    cserver.start()



