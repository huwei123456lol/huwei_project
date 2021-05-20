from django.shortcuts import render, HttpResponse
from concurrent.futures import ThreadPoolExecutor
import threading
from urllib.parse import quote, unquote
import socket
import time
import os
# Create your views here.


# 思路: 点击一个选项跳转到帮助界面，并主动和客户端连接
def get_connect(request):
    userinfo = request.session.get('info')
    username = userinfo.get('username')
    password = userinfo.get('password')
    hostname = socket.gethostname()
    address = socket.gethostbyname(hostname)
    # 这里客户端需要用到线程池
    server_thread = threading.Thread(target=server_connect, args=address)
    server_thread.start()
    client_pool = ThreadPoolExecutor(max_workers=10)
    client_pool.submit(client_connect, address)
    total = []
    # 获取聊天记录
    with open('temp.txt', 'r+', encoding='utf-8') as f:
        data = f.readline()
        total.append(data)
        f.close()
    os.remove('temp.txt')
    return HttpResponse(total)


# 自定义函数，用来做数据链接的服务端
# 创建一个临时文件，这个文件的内容包含双方间的通信
def server_connect(address):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((address, 8080))
    server.listen()
    while True:
        s, connect_address = server.accept()
        start = time.time()
        with open('temp.txt', 'a+', encoding='utf-8') as f:
            s.send(quote("有什么需要帮忙的吗？@"+connect_address).encode('utf-8'))
            f.write('有什么需要帮忙的吗？\n')
            data = unquote(s.recv(1024).decode('utf-8'))     # 获取客户端传送过来的消息
            f.write(data+'\n')
            if data.find('歌曲', 0, len(data)):
                s.send(quote('歌曲有什么解释的！你可以换个问题问我？@'+connect_address).encode('utf-8'))
                f.write('歌曲有什么解释的！你可以换个问题问我？\n')
            elif data.find('音乐', 0, len(data)):
                s.send(quote('音乐是人的天使，享受它，爱上它，你就会拥有全世界！@'+connect_address).encode('utf-8'))
                f.write('音乐是人的天使，享受它，爱上它，你就会拥有全世界!\n')
            else:
                s.send(quote('超出了我的范围，请你换个话题！@'+connect_address).encode('utf-8'))
                f.write('超出了我的范围，请你换个话题！\n')
            f.write('\n')
            if time.time()-start >= 24000 and not s.recv(1024).decode('utf-8'):
                f.close()
                s.close()   # 关闭链接


# 自定义函数，用来进行数据链接的客户端
def client_connect(address):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((address, 8080))
    # 这里可以弄成循环语句
    client.send(quote('你能告诉我什么是音乐吗？').encode('utf-8'))
    data = unquote(client.recv(1024).decode('utf-8'))
    print(data)
    client.close()
