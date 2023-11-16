from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return ''

app.run(host='0.0.0.0', port=8080, debug=True) # 나중에 호스트 서버와 연결