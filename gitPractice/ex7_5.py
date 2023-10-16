from flask import Flask
app = Flask(__name__)

@app.route('/')
def func():
    return "<h2>초기화면입니다요~!</h2>"

@app.route('/<name>/')
def hello(name):
    if name == 'kitae':
        str = "<h2>Hello, Kitae</h2>"
    elif name == 'jmlee':
        str = "<h2>Hello, Jmlee</h2>"
    else:
        str = "<h2>조심! URL이 잘못되었습니다.</h2>"
    return str

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug=True)

with app.app_context():
    print(app.url_map)