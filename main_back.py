import time
from gettext import gettext
import requests

from flask import Flask, make_response, request
import xml.etree.cElementTree as ET
import hashlib

app = Flask(__name__)

CHATGPT_API_URL = "http://127.0.0.1:5000/chatgpt"  # ChatGPT 接口地址，根据实际部署修改

@app.route('/wx', methods=['GET', 'POST'])
def wechat():  # 1、 获取携带的 signature、timestamp、nonce、echostr
    if request.method == 'GET':
        signature = request.args.get("signature", "")

        timestamp = request.args.get("timestamp", "")

        nonce = request.args.get("nonce", "")

        echostr = request.args.get("echostr", "")
        print(signature, timestamp, nonce, echostr)

        token = "047f71d7e599c539"  # 这里是你写的那个token值

        data = [token, timestamp, nonce]

        data.sort()  # 3、三个参数拼接成一个字符串并进行sha1加密

        temp = ''.join(data)

        sha1 = hashlib.sha1(temp.encode('utf-8'))

        hashcode = sha1.hexdigest()
        print(hashcode)  # 4、对比获取到的signature与根据上面token生成的hashcode，如果一致，则返回echostr，对接成功

        if hashcode == signature:
            return echostr
        else:
            return "error"
    else:
        xmlData = ET.fromstring(request.stream.read())
        msg_type = xmlData.find('MsgType').text
        if msg_type == 'text':
            if xmlData.find('Content').text == '暗号':
                ToUserName = xmlData.find('ToUserName').text
                FromUserName = xmlData.find('FromUserName').text
                # Content = xmlData.find('Content').text
                Content = '对应暗号：<a style="color:red;" src="http://d-dlpay.top">0000</a>\n百度链接：<a src="http://www.baidu.com">喂</a>'
                reply = '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
                '''
                response = make_response(reply % (FromUserName, ToUserName, str(int(time.time())), Content))
                response.content_type = 'application/xml'
                return response
            else:
                t = '正在输入....'
                return gettext(xmlData, t)

def get_chatgpt_response(prompt):
    # 调用 ChatGPT 接口获取回复
    data = {
        "prompt": prompt,
        "max_tokens": 100,
        "temperature": 0.7
    }

    response = requests.post(CHATGPT_API_URL, json=data, headers={"Content-Type": "application/json"})
    return response.json()["response"]

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)  # 这里开放8080端口
