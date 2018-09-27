#!/usr/bin/python

import itchat
import threading
import time
import sys

weixin_islogin = False
weixin_recv_queue = []
weixin_recv_queue_lock = threading.Lock()

weixin_self_username = ""

@itchat.msg_register(itchat.content.TEXT)
def weixin_recv_text(msg):
    global weixin_recv_queue, weixin_recv_queue_lock
    weixin_recv_queue_lock.acquire()
    weixin_recv_queue.append(msg)
    weixin_recv_queue_lock.release()

def weixin_send_text(text, username):
    itchat.send(text, username)

def weixin_login_callback():
    global weixin_islogin
    friends = itchat.get_friends(update=True)[0:]
    global weixin_self_username
    weixin_self_username = friends[0]["UserName"]
    weixin_islogin = True
    print ("您已登陆微信")

def weixin_logout_callback():
    global weixin_islogin
    weixin_islogin = False
    print ("您已退出微信")

def weixin_login():
    itchat.auto_login(hotReload=True,
        loginCallback=weixin_login_callback, exitCallback=weixin_logout_callback)
    
def weixin_run():
    itchat.run()
    
def weixin_friends():
#    a=0
    return itchat.get_friends(update=True)
#    for user in friends:
#        print (str(a)+":"+str(user).split(",")[3]+str(user).split(",")[2])
#        a+=1
        
class WeiXin(threading.Thread):
    def __init__(self):
        super().__init__()
    
    def run(self):
        weixin_login()
        weixin_run()

class Shell:
    friends = []
    def is_send_by_me(self, msg):
        global weixin_self_username
        return msg["FromUserName"] == weixin_self_username
    
    def print_friends(self):
        a = 0
        for user in self.friends:
#            strs = str(user).split(",")
            nickname = user["NickName"]
            username = user["UserName"]
            print (str(a)+":" + "nickname=" + nickname + ", username=" + username)
            a+=1
    
    def show_msg(self):
        global weixin_recv_queue, weixin_recv_queue_lock
        weixin_recv_queue_lock.acquire()
        recv_queue = weixin_recv_queue
        weixin_recv_queue = []
        weixin_recv_queue_lock.release()

        for m in recv_queue:
            if (not self.is_send_by_me(m)):
                print ("[{}, {}]\n  {}".format(m["User"]["NickName"], m["FromUserName"], m["Content"]))
            #print (m)
        

    def run(self):
        print("--------------微信聊天--------------")
        global weixin_islogin
        print("正在登陆微信 ...")
        while weixin_islogin == False:
            time.sleep(2)

        while True:
            command = input("> ")
            if command == "exit":
                break
            if command == "update":
                self.friends = weixin_friends()
            if command == "msg":
                self.show_msg()
            if command == "send":
                self.print_friends()
                print("请选择好友聊天,并输入UserName")
                username = input("username=")
                text = input("text=")
                weixin_send_text(text, username)
            



if __name__ == '__main__':
    t = WeiXin()
    t.start()
    
    s = Shell()
    s.run()   
