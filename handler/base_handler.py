
class BaseRequestHandler:

    def __init__(self, server, request, client_address):
        self.server = server
        self.request = request
        self.client_address = client_address

    def handle(self):
        pass


class StreamRequestHandler(BaseRequestHandler):

    def __init__(self, server, request, client_address):
        BaseRequestHandler.__init__(self, server, request, client_address)
        # 读写分离为两个描述符，分别有读权限和写权限
        self.rfile = self.request.makefile('rb')
        self.wfile = self.request.makefile('wb')
        self.wbuf = []      # 写缓冲区

    # 编码: 网络字节流msg ——> UTF-8字节码
    def encode(self, msg):
        if not isinstance(msg, bytes):
            msg = bytes(msg, encoding='utf-8')
        return msg

    # 解码：UTF-8字节码msg ——> 网络字节流
    def decode(self, msg):
        if isinstance(msg, bytes):
            msg = msg.decode()
        return msg

    # 读消息
    def read(self, length):
        msg = self.rfile.read(length)
        return self.decode(msg)

    # 读行消息，默认长度为一个HTTP报文德长度，即65536B
    def readline(self, length=65536):
        msg = self.rfile.readline(length).strip()
        return self.decode(msg)

    # 写消息
    def write_content(self, msg):
        msg = self.encode(msg)
        self.wbuf.append(msg)

    # 发送消息
    def send(self):
        for line in self.wbuf:
            self.wfile.write(line)
        self.wfile.flush()
        self.wbuf = []

    # 关闭连接
    def close(self):
        self.wfile.close()
        self.rfile.close()
