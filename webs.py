#!/usr/bin/python
# -*- coding: utf-8 -*- 
import string
import re
import os,time,sys,socket,threading,array,re,fcntl,struct

def hex2str(num):
        e="%x"%num
        e=str(e)
        e='0'+e if len(e)==1 else e
        return e


def str2hex(char):
    num=string.atoi(char, 16)
    return num

def hex_split(stri):
    m=len(stri)%2
    stri='0'+stri if m!=0 else stri 
    le=len(stri)//2
    li=[]
    str1=stri[::2]
    str2=stri[1::2]
    for i in range(le):
        li.append(str1[i]+str2[i])
    return li 

def find_num(str):
    nums=''
    for i in str:
        nums=nums+i if i.isdigit() else nums
    return int(nums)

def space_num(str):
    return len(str)-len(str.replace(' ', ''))
   
def make_challenge(key1,key2,key3):
    num1=find_num(key1)//space_num(key1) if find_num(key1)%space_num(key1)==0 else -1
    num2=find_num(key2)//space_num(key2) if find_num(key2)%space_num(key2)==0 else -1
    #print num2,num1
    if (num1<0) or (num2<0):
        raise 
    else:
        string=hex_split(str("%x"%num1))+hex_split(str("%x"%num2))+map(hex2str,map(ord,key3))
        return map(str2hex,string)
    
def make_respond(header):
    print get_keys(header)
    key1,key2,key3=get_keys(header)
    challenge=make_challenge(key1,key2,key3)
    print challenge
    import hashlib
    s=''.join(map(chr,challenge))
    m=hashlib.md5(s)
    sum=m.hexdigest()
    return ''.join(map(chr,map(str2hex,hex_split(sum))))


def get_keys(handinfo):
    read_re=re.findall(r'Sec-WebSocket-Key1: (.*)\n',handinfo)
    key1=read_re[0].strip()
    read_re=re.findall(r'Sec-WebSocket-Key2: (.*)',handinfo)
    key2=read_re[0].strip()
    read_re=re.findall(r'\r\n\r\n(.*)',handinfo,re.S)
#    print read_re
#    raise
    key3=read_re[0].strip()
    return key1,key2,key3

header="""GET /demo HTTP/1.1
Host: example.com
Connection: Upgrade
Sec-WebSocket-Key2: 12998 5 Y3 1  .P00
Sec-WebSocket-Protocol: sample
Upgrade: WebSocket
Sec-WebSocket-Key1: 4 @1  46546xW%0l 1 5
Origin: http://example.com

^n:ds[4U"""

class websocket( ):
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.allreport = ''
        
    def handshake(self,s):
        ip=self.ip
        port=self.port
        header=s.recv(4096)
        print repr(header)
        resp=make_respond(header)
        read_re=re.search('http.*\d*\.\d*\.\d*\.\d*',header)
        orign=read_re.group(0) if read_re != None else ''
        #buffer= array.array('c', '\0' * 4096)
        back='''HTTP/1.1 101 Web Socket Protocol Handshake\r
Upgrade: WebSocket\r
Connection: Upgrade\r
Sec-WebSocket-Origin: %s\r
Sec-WebSocket-Location: ws://%s:%s/\r
Sec-WebSocket-Protocol: sample\r\n\r
%s\r
'''.strip()%(orign,ip,port,resp)
        print repr(back)
        s.send(back)
        #log_file=open('1','rw',0)
            #s.recv_into(buffer)
            #print buffer
            #print repr(s.recv(4096))
        #time.sleep(5)
        s.send('\x00%s\xff'%'haha')
        return s
    
    def handle(self,t):
        self.handl=self.handshake(t)
        self.send('dad')
        
    def send(self,msg):
        self.handl.send('\x00%s\xff'%msg)
        
    def create(self):
        s = socket.socket()
        ip=self.ip
        port=self.port
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.ip, self.port));
        s.listen(1);
        while 1:
            t,_ = s.accept();
            try:
                threading.Thread(target = self.handle, args = (t,)).start()
            except 'Broken pipe':
                continue

a=websocket('192.168.9.83',12345)
a.create()
#print make_respond(header)


