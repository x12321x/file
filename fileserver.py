#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueYining
#   Date    :   2018/6/6
#   Desc    :   阻塞 server

import socket
import time
import sys
import os
import struct

# 设置server端IP地址及端口号
SERVER_ADDRESS = (HOST, PORT) = '192.168.92.8', 6666
# 设置请求队列大小
REQUEST_QUEUE_SIZE = 5

'''===========================此部分为响应client request==========================='''

def handle_request(client_connection, client_address):

    print 'Accept new connection from {0}'.format(client_address)
    '''*****************此部分为响应client request*****************'''
    
    # 通过发送TCP数据，告诉client已成功连接到server
    client_connection.send('Hi, Welcome to the server!')

    '''******************此部分为实现文件传输******************'''

    while True:
        # 接受TCP套接字的数据，数据以字符串形式返回
        data = client_connection.recv(1024)
        
        # 如果传输来的字符为n或者为空，断开连接
        if data == 'n' or data == 'N' or not data:
            print '{0} connection close'.format(client_address)
            
            # 发送TCP数据，告诉client断开连接
            client_connection.send('Connection closed!')
            break

        else:
            # 定义文件大小。
            # 128s表示文件名为128bytes长，l表示一个int或log文件类型
            fileinfo_size = struct.calcsize('128sl')
            
            # 接受TCP套接字的数据，数据以字符串形式返回
            buf = client_connection.recv(fileinfo_size)
            
            # 如果不加这个if，第一个文件传输完成后会自动走到下一句，
            # 需要拿到文件大小信息才可以继续执行
            if buf:
                # 根据格式化字符串128sl，从缓冲区buf中解包。
                filename, filesize = struct.unpack('128sl', buf)
                # 解出文件名，去掉C语言中的字符串\00结束
                fn = filename.strip('\00')
                new_filename = os.path.join('./', 'new_' + fn)
                print 'file new name is {0}, filesize if {1}'.format(new_filename,
                                                                     filesize)

                recvd_size = 0  # 定义已接收文件的大小
                fp = open(new_filename, 'wb') # 向新建文件写入数据
                print 'start receiving...'

                # 如果已接收文件大小不等于传输文件大小
                while not recvd_size == filesize: 
                    # 如果比1024大，则每次接受1024
                    if filesize - recvd_size > 1024:
                        data = client_connection.recv(1024)
                        recvd_size += len(data)
                    # 不足1024时
                    else:
                        data = client_connection.recv(filesize - recvd_size)
                        recvd_size = filesize
                    fp.write(data) # 写文件
                fp.close() # 关闭文件

                print 'end receive...'
                time.sleep(5) # 模拟阻塞事件

        client_connection.send('Hello, {0} is arrived!'.format(filename))


'''===========================此部分为server主要内容==========================='''

def server():
     '''**************此部分为创建套接字并连接到远端**************'''
    
    # 先正常执行try中的socket，若出错则执行except中的指令
    
    try:
        # 定义socket类型，创建套接字
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # 防止socket server重启后端口被占用
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # 绑定需要监听的Ip和端口号
        listen_socket.bind(SERVER_ADDRESS)
        
        # 开始监听TCP传入连接。
        listen_socket.listen(REQUEST_QUEUE_SIZE)
    
    except socket.error as msg:
        print msg
        sys.exit(1)


    '''*****************此部分为等待client响应*****************'''
    
    print 'Waiting connection...'


    '''******************此部分为实现字符串传输******************'''

    while True:
        # 接受TCP连接并返回（conn,address）
        # conn是新的套接字对象，可以用来接收和发送数据。
        # address是连接客户端的地址。
        client_connection, client_address = listen_socket.accept()
        
        #调用响应request函数
        handle_request(client_connection, client_address)
        
        #关闭套接字
        client_connection.close()  

if __name__ == '__main__':
    server()
