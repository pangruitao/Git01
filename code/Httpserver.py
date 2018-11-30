#多线程Httpserver网络服务器
#封装Httpserver类
#属性,方法
from socket import *
import sys
from threading import Thread
import re, time
from setting import *
#WebFrame通信函数
#返回客户端要请求的文件内容
def connect_frame(METHOD, PATH_INFO):
    s = socket() #创建一个socket
    try:
        s.connect(frame_address)#连接框架服务器
    except:
        print("Connect err")
        return
    s.send(METHOD.encode())
    time.sleep(0.1)
    s.send(PATH_INFO.encode()) #发送请求文件路径
    resp = s.recv(4096).decode() #接收结果
    if not resp:
        return "404"
    else:
        s.close()
        return resp #返回文件内容

#封装Httpserver类
class HTTPServer(object):
    def __init__(self, address):
        self.address = address
        self.create_socket() #创建socket
        self.bind(address)  #绑定

    #创建套接字,用于监听的
    def create_socket(self): #创建socket
        self.sockfd = socket()
        self.sockfd.setsockopt(
            SOL_SOCKET,SO_REUSEADDR,1
        )

    def bind(self, address):
        self.ip = address[0]
        self.port = address[1]
        self.sockfd.bind(address)

    def server_foever(self):
        self.sockfd.listen(10)
        print("Server start on", self.port)
        while True:
            connfd,addr = self.sockfd.accept()
            print("Connect from", addr)

            handle_client = Thread(target = self.handle, args = (connfd,))#创建处理的线程
            handle_client.setDaemon(True)
            handle_client.start() #启动线程

    #定义具体处理客户端请求的函数
    def handle(self, connfd):
        #接受来自客户端的数据
        request = connfd.recv(4096)
        if not request:  #没读到数据
            connfd.close()  #关闭socket
            return
        
        #将请求数据按换行符进行拆分
        request_lines = request.splitlines()
        #获取请求行
        request_line = request_lines[0].decode("utf-8")
        print(request_line)
        #请求行的合法性
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH_INFO>/\S*)'
        try:
            p = re.match(pattern, request_line)
            env = p.groupdict()
            print(env)
        except: #请求错误,直接返回错误
            response = "HTTP/1.1 500 SERVER ERROR\r\n"
            response += "\r\n"  #空行,包头,和包体的分隔符
            response += "Server error"
            connfd.send(response.encode())#发送响应
            connfd.close() #关闭通信socket
            return
        #正常数据处理 GET /index.html HTTP/1.1
        content = connect_frame(**env)#调用另外的服务器处理
        response = ""
        if content == "404":#请求的文件未找到
            header = "HTTP/1.1 404 Not Foung\r\n"
            header += "\r\n"
            body = "Sorry, not found the page"
            response = header + body
        else:#文件找到,正常返回
            header = "HTTP/1.1 200 OK \r\n"
            header += "\r\n"

            print(header)
            print(content)

            response = header + content #将文件内容作为body部分
        connfd.send(response.encode())
        connfd.close()

if __name__ == "__main__":
    httpserver = HTTPServer(ADDR)
    httpserver.server_foever() #