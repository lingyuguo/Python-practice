#! /usr/bin/env python
#-*-coding:utf-8-*-

import requests
import json


def get_token():
        url='https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid' : 'wx4c879f1cbd778cc7' ,
                  'corpsecret':'y8qAg29VO39ENWbY2zdjogioDouydHJlE_QGh3uiS54'}
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        return data["access_token"]

def send_msg():
        url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+get_token()
        values = """{"touser" : "@ll" ,
                "toparty":"6",
                "msgtype":"text",
                "agentid":"1000002",
                "text":{"content":"%s"},
               "safe":"0"
               }""" %(str("Congratulations to you! Test success"))
        data = json.loads(values)
        req = requests.post(url, values)

if __name__ == '__main__':
        send_msg()
