#!/usr/bin/env python
# -*- coding:utf-8 -*-
#   
#   Author  :   XueYining
#   Date    :   2018/6/6

import socket
import time
import os
import sys
import struct

# 设置server端IP地址及端口号
SERVER_ADDRESS = (HOST, PORT) = '192.168.92.8', 6666 

def client():

    '''**************此部分为创建套接字并连接到远端**************'''
    
    # 先正常执行try中的socket，若出错则执行except中的指令
    try:
        # 定义socket类型，创建套接字
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 连接到远端的套接字
        s.connect(('192.168.92.8', 6666))
    except socket.error as msg:
        print msg
        sys.exit(1)


    '''*****************此部分为等待server响应*****************'''
    
    print 'Client is Waiting response...'   
    # 接受TCP套接字的数据，数据以字符串形式返回
    print s.recv(1024)


    '''******************此部分为实现文件传输******************'''
    while True:
        data = raw_input('Do you want to send a file? (y/n): ')
        # 发送TCP数据。将data中的数据发送到连接的套接字。
        s.send(data)

        # 如果data不为n，即还要继续传输文件
        if data != 'n':
            filepath = raw_input('please input file path: ')
            # 判断路径是否为文件
            if os.path.isfile(filepath):
                # 定义文件大小。
                # 128s表示文件名为128bytes长，l表示一个int或log文件类型
                fileinfo_size = struct.calcsize('128sl')
                # 定义文件头信息，包含文件名和文件大小
                # 并根据‘128sl’进行封装
                fhead = struct.pack('128sl', os.path.basename(filepath),
                                    os.stat(filepath).st_size)
                # 发送TCP数据。将fhead中的数据发送到连接的套接字。
                s.send(fhead)
                print 'client filepath: {0}'.format(filepath)

                #打开文件
                fp = open(filepath, 'rb')
                while 1:
                    # 读取文件
                    data = fp.read(1024)
                    # 如果本次读取为空，则文件传输完毕，终止循环
                    if not data:
                        print '{0} file send over...'.format(filepath)
                        break
                    # 发送TCP数据。将data中的数据发送到连接的套接字。
                    s.send(data)

        print 'Client is Waiting response...'
        # 接受TCP套接字的数据，数据以字符串形式返回
        print s.recv(1024)

        #如果data为n，则不再传输文件，终止循环
        if data == 'n':
            break
    
if __name__ == '__main__':
    client()
