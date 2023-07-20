import requests

# 接口地址
url = "http://127.0.0.1:5000/chatgpt"

# 请求参数
data = {
    "prompt": "你好，ChatGPT！",
    "max_tokens": 100,
    "temperature": 0.7
}

# 发送 POST 请求
response = requests.post(url, json=data)

# 打印响应结果
print(response.json())
