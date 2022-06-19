
from socket import *
import threading,sys,json,re

HOST = '192.168.56.1'  ##
PORT=8023
BUFSIZ = 1024  ##缓冲区大小  1K
ADDR = (HOST,PORT)

tcpCliSock = socket(AF_INET,SOCK_STREAM)
tcpCliSock.connect(ADDR)
userAccount = None
def register():
    myre = r"^[_a-zA-Z]\w{0,}"
    #正则验证用户名是否合乎规范
    accout = input('输入您的账号: ')
    if not re.findall(myre, accout):
        print('账户违规!')
        return None
    password1  = input('请输入密码: ')
    password2 = input('请确认密码: ')
    if not (password1 and password1 == password2):
        print('密码违规!')
        return None
    global userAccount
    userAccount = accout
    return (accout,password1)

class inputdata(threading.Thread):
    def run(self):
        while True:
            sendto = input('to>>:')
            msg = input('msg>>:')
            dataObj = {'to':sendto,'msg':msg,'froms':userAccount}
            datastr = json.dumps(dataObj)
            tcpCliSock.send(datastr.encode('utf-8'))


class getdata(threading.Thread):
    def run(self):
        while True:
            data = tcpCliSock.recv(BUFSIZ)
            dataObj = json.loads(data.decode('utf-8'))
            print('{} -> {}'.format(dataObj['froms'],dataObj['msg']))


def main():
    while True:
        regInfo = register()
        if  regInfo:
            datastr = json.dumps(regInfo)
            tcpCliSock.send(datastr.encode('utf-8'))
            break
    myinputd = inputdata()
    mygetdata = getdata()
    myinputd.start()
    mygetdata.start()
    myinputd.join()
    mygetdata.join()


if __name__ == '__main__':
    main()