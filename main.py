import time

from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
import requests

app = Flask(__name__)

# 微信公众号配置信息，需要替换为你自己的
TOKEN = "047f71d7e599c539"
CHATGPT_API_URL = "http://127.0.0.1:5000/chatgpt"

@app.route('/wx', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        # 验证服务器有效性
        echostr = request.args.get('echostr', '')
        if check_signature(request):
            return echostr
        else:
            return "Invalid signature."
    elif request.method == 'POST':
        # 处理用户消息
        xml_data = request.data
        root = ET.fromstring(xml_data)
        msg_type = root.find('MsgType').text
        user_openid = root.find('FromUserName').text
        content = root.find('Content').text

        # 调用 ChatGPT 接口获取回复
        chatgpt_reply = get_chatgpt_reply(content)

        # 生成回复消息
        reply = generate_reply(user_openid, chatgpt_reply)

        return make_response(reply)

def check_signature(request):
    # 验证服务器有效性，比较签名是否一致
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')

    token = TOKEN
    tmp_list = [token, timestamp, nonce]
    tmp_list.sort()
    tmp_str = ''.join(tmp_list).encode('utf-8')
    tmp_str = hashlib.sha1(tmp_str).hexdigest()

    return tmp_str == signature

def get_chatgpt_reply(prompt):
    # 调用 ChatGPT 接口获取回复
    data = {
        "prompt": prompt,
        "max_tokens": 1024,
        "temperature": 0.7
    }
    response = requests.post(CHATGPT_API_URL, json=data)
    if response.status_code == 200:
        return response.json().get('response', '')
    else:
        return ""

def generate_reply(to_user, content):
    # 生成回复消息
    reply_template = """<xml>
    <ToUserName><![CDATA[{}]]></ToUserName>
    <FromUserName><![CDATA[{}]]></FromUserName>
    <CreateTime>{}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{}]]></Content>
    </xml>"""
    create_time = int(time.time())
    return reply_template.format(to_user, 'bookshelf001', create_time, content)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
