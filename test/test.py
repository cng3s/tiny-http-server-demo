import threading
import socket
import time

from handler.base_handler import StreamRequestHandler
from handler.base_http_handler import BaseHTTPRequestHandler
from server.socket_server import TCPServer
from server.base_http_server import BaseHTTPServer


# 测试BaseRequestHandler
class TestBaseRequestHandler(StreamRequestHandler):

    # 具体的处理逻辑
    # 通过time.sleep(1)模拟可以发现服务器处理并发请求的性能非常之差
    # 原因是TCPServer ——> server_forever ——> while循环中是排序逐个处理请求
    # 而当客户端处理请求的1s时间内，服务器端是阻塞在process_request中
    # 而process_request又阻塞在handler.handle()中
    # 此时服务器端无法处理其他请求服务，只能等待客户端处理好请求并返回
    def handle(self):
        msg = self.readline()
        print('Server recv msg: ' + msg)
        time.sleep(1)  # 模拟假设每个客户端处理请求都需要1s的时间
        self.write_content(msg)
        self.send()


# 测试SocketServer(TCPServer)
class SocketServerTest:

    def run_server(self):
        tcp_server = TCPServer(('127.0.0.1', 8888), TestBaseRequestHandler)
        tcp_server.serve_forever()

    def client_connect(self):
        client = socket.socket()
        client.connect(('127.0.0.1', 8888))
        client.send(b'Hello TCPServer\r\n')
        msg = client.recv(1024)
        print("Client recv msg: " + msg.decode())

    # 生成num个客户端并连接SocketServer
    def gen_clients(self, num):
        clients = []
        for i in range(num):
            # 使用多线程模拟创建多个客户端
            client_thread = threading.Thread(target=self.client_connect)
            clients.append(client_thread)
        return clients

    def run(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

        clients = self.gen_clients(10)
        for client in clients:
            client.start()

        server_thread.join()
        for client in clients:
            client.join()


class BaseHTTPRequestHandlerTest:

    def run_server(self):
        BaseHTTPServer(('127.0.0.1', 9999), BaseHTTPRequestHandler).serve_forever()

    def run(self):
        self.run_server()


if __name__ == '__main__':
    # SocketServerTest().run()
    BaseHTTPRequestHandlerTest().run()