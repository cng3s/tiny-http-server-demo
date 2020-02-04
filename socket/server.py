
import socket

def server():
    # 1. 创建套接字
    s = socket.socket()
    # 2. 绑定套接字
    IP = '127.0.0.1'
    PORT = 6666
    s.bind((IP, PORT))
    # 3. 监听套接字
    s.listen(5)
    # 4. 处理套接字
    while True:
        c, addr = s.accept()
        print('Connect Client: ', addr)
        msg = c.recv(2048)
        print('From Client: %s' % msg)
        c.send(msg)
    pass

if __name__ == '__main__':
    server()