# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
# import openai
import requests
import json


app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
  user_input = request.json.get('message')
  # 调用 OpenAI API 或其他逻辑
  response = invoke_llm(user_input)  # 假设你有一个函数来处理 LLM 请求
  print(response)
  return jsonify({'response': response})



def invoke_llm(message):
  # 设置 API URL 和 API 密钥
  url = "https://api2.aigcbest.top/v1/chat/completions"
  api_key = "sk-igzJkocZvGiw0AfnQT3zyrjOCLDC6FfCkbTPd274UDcJiCRO"  # 替换为你的实际 API 密钥

  # 设置请求头
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}",
  }

  # 设置请求体
  data = {
      "model": "gpt-4o-mini",
      "messages": [{"role": "user", "content": message}],
      "temperature": 0.7,
      "max_tokens": 2048,  # 设置最大 tokens 数量，可以根据需要调整
  }

  # 发送 POST 请求
  response = requests.post(url, headers=headers, data=json.dumps(data))

  # 检查响应状态
  if response.status_code == 200:
    # 打印响应内容
    return response.json()['choices'][0]['message']['content']
  else:
    print("Error:", response.status_code, response.text)

if __name__ == '__main__':
    app.run(debug=True)
