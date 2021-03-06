
import socket
import threading

class TCPServer:

    def __init__(self, server_addr, handler_class):
        self.server_address = server_addr
        self.HandlerClass = handler_class
        self.socket = socket.socket(
            socket.AF_INET,         # 协议类
            socket.SOCK_STREAM,     # 使用tcp server字节流
        )
        self.is_shutdown = False

    # 服务器启动
    def serve_forever(self):
        self.socket.bind(self.server_address)
        self.socket.listen(10)
        while not self.is_shutdown:
            # 1. 接收请求
            request, client_addr = self.get_request()
            # 2. 处理请求
            try:
                #self.process_request(request, client_addr)
                self.process_request_multithread(request, client_addr)
            except Exception as e:
                print(e)


    # 接收请求
    def get_request(self):
        return self.socket.accept()

    # 处理请求 多线程中关闭连接的请求放在process_request中
    # 处理完请求后子线程就关闭连接而不占用主线程
    def process_request(self, request, client_addr):
        handler = self.HandlerClass(self, request, client_addr)
        handler.handle()
        # 关闭连接
        self.close_request(request)

    def process_request_multithread(self, request, client_addr):
        t = threading.Thread(target=self.process_request,
                             args=(request, client_addr))
        t.start()

    # 关闭请求
    def close_request(self, request):
        request.shutdown(socket.SHUT_WR)
        request.close()

    # 关闭服务器
    def shutdown(self):
        self.is_shutdown = True
