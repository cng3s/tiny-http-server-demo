
import os
import json

from urllib import parse
from handler.base_http_handler import BaseHTTPRequestHandler

RESOURCES_PATH = os.path.join(
    os.path.abspath(os.path.dirname(__name__)),
    '..\\resources')


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, server, request, client_address):
        BaseHTTPRequestHandler.__init__(self, server, request, client_address)

    def do_GET(self):
        found, resource_path = self.get_resources(self.path)
        if not found:
            self.write_error(404)
            self.send()
        else:
            with open(resource_path, 'rb') as f:
                fs = os.fstat(f.fileno())
                length = str(fs[6])
                self.write_response(200)
                self.write_header('Content-Length', length)
                # 防止跨域攻击
                self.write_header('Access-Control-Allow-Origin',
                                  'http://%s:%d' % (self.server.server_address[0],
                                                    self.server.server_address[1]))
                self.end_headers()
                while True:
                    buf = f.read(1024)
                    if not buf:
                        break
                    self.write_content(buf)

    # 判断并获取资源
    def get_resources(self, path):
        # 1.从链接中获取相对路径并拼装为绝对路径
        url_result = parse.urlparse(path)
        resource_path = str(url_result[2])
        if resource_path.startswith('/'):
            resource_path = resource_path[1:]
        resource_path = os.path.join(RESOURCES_PATH, resource_path)
        # 2.若绝对路径存在则返回True和拼装后的绝对路径
        if os.path.exists(resource_path) and os.path.isfile(resource_path):
            return True, resource_path
        return False, resource_path

    def do_POST(self):
        # 从请求中取出数据
        body = json.loads(self.body)
        print(body)
        username = body['username']
        password = body['password']
        # 数据校验
        if username == 'chneg33' and password == '123456':
            response = {'message': 'success', 'code': 0}
        else:
            response = {'message': 'failed', 'code': -1}
        response = json.dumps(response)
        # 组成应答报文
        self.write_response(200)
        self.write_header('Content-Length', len(response))
        self.write_header('Access-Control-Allow-Origin',
                          'http://%s:%d' % (self.server.server_address[0],
                                            self.server.server_address[1]))
        self.end_headers()
        self.write_content(response)