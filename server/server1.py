from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
  user_input = request.json.get('message')
  # user_input = '苹果的好处'
  return Response(invoke_llm(user_input), content_type='text/plain; charset=utf-8')

def invoke_llm(message):
  url = "https://api2.aigcbest.top/v1/chat/completions"
  api_key = "sk-igzJkocZvGiw0AfnQT3zyrjOCLDC6FfCkbTPd274UDcJiCRO"

  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}",
  }

  data = {
      "model": "gpt-4o-mini",
      "messages": [{"role": "user", "content": message}],
      "temperature": 0.7,
      "max_tokens": 2048,
      "stream": True  # 启用流式传输
  }

  response = requests.post(url, headers=headers, data=json.dumps(data), stream=True)

  if response.status_code == 200:
    for line in response.iter_lines():
      if line:
        line = line.decode('utf-8')  # 先解码成字符串
        if line.startswith("data: "):  # 只处理包含 "data: " 的行
          try:
            json_data = json.loads(line[6:])  # 去掉前面的 "data: " 并解析 JSON
            chunk = json_data.get('choices', [{}])[0].get('delta', {}).get('content', '')
            if chunk:
              print(chunk, end='', flush=True)  # 逐字输出
          except json.JSONDecodeError:
            continue
  else:
    print("Error:", response.status_code, response.text)


if __name__ == '__main__':
  # test_input = "苹果的好处"  # 直接测试的文本
  # print("AI 回答：")
  # invoke_llm(test_input)  # 直接在终端运行
  app.run(debug=True, threaded=True)
