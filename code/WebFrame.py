# 框架服务器
from socket import *
from setting import *
#静态网页的位置
STATTC_DIR = './static'

class WebFrame(object):
    def __init__(self):#构造函数
        self.sockfd = socket() #创建监听socket
        self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.sockfd.bind(frame_address)

    #启动服务器:监听,接收连接请求
    def start(self):
        self.sockfd.listen(5) #监听
        print("WebFrame start")
        while True:
            connfd,addr = self.sockfd.accept()
            method = connfd.recv(128).decode()
            path_info = connfd.recv(1024).decode()
            self.handle(connfd, method, path_info)

    def handle(self,connfd,method,path_info):
        if method == "POST":
            pass
        elif method == "GET":
            if path_info == "/":
                resp = self.get_html("/index.html")
            else:
                resp = self.get_html(path_info)

        connfd.send(resp.encode())#发回文件内容
        connfd.close()#关闭socket
    
    def get_html(self, path_info):
        full_path = STATTC_DIR + path_info
        print("full_path:", full_path)
        try:
            fd = open(full_path) #打开文件
        except:
            resp = '404'
            print("open file err")
        else:
            resp = fd.read()#读文件内容
            fd.close()
        return resp

if __name__ == "__main__":
    webframe = WebFrame()
    webframe.start() #启动WebFrame服务器
