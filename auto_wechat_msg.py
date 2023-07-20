from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# 替换为你的 ChatGPT 访问密钥
api_key = "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"
openai.api_key = api_key


@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    try:
        # 获取请求中的参数
        data = request.get_json()
        prompt = data['prompt']
        max_tokens = data.get('max_tokens', 100)
        temperature = data.get('temperature', 0.7)

        # 调用 ChatGPT
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )

        return jsonify({"response": response['choices'][0]['text'].strip()})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

