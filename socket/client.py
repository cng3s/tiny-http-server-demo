
import socket

def client():
    # 1. 创建套接字
    s = socket.socket()
    # 2. 连接
    IP = "127.0.0.1"
    PORT = 6666
    s.connect((IP, PORT))
    # 3. 处理信息
    s.send(b'Hello World!')
    msg = s.recv(1024)
    print('From server: %s' % msg)

if __name__ == '__main__':
    client()