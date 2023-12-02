# Flask 모듈을 이용하여 웹 서버를 구축하고, 실시간으로 사용자의 입력에 반응할 수 있도록 함.

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html') 
# templates 디렉토리의 index.html 파일을 render_template 함수를 이용해 웹 페이지를 보다 동적으로 만듦.

app.run(host='0.0.0.0', port=8080, debug=True)