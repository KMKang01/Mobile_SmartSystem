from flask import Flask, render_template, request
# 플라스크의 기능, 렌더링 기능, request 객체를 활용하기 위해 phone.py에 import
app = Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html')
# 처음 접속했을 때 보여지는 화면

@app.route('/store/', methods=['GET'])
def store():
        name = request.args.get('name')
        tel = request.args.get('tel')
        # 데이터를 GET 방식으로 주고받기 때문에 request.args() 메소드를 이용
        file = open('./data/phonebook.txt', 'a')
        # data 디렉토리에 phonebook.txt가 없으면 생성하고, 있으면 이어붙임.
        data = "%s,%s\n" % (name, tel)
        # 이름과 전화번호를 콤마로 구분하여 저장
        file.write(data)
        file.close()

        return render_template('index.html', msg='저장되었습니다.')
        # render_template 메소드를 활용하여 index.html를 렌더링하고, index.html에 msg를 전달
# 이름과 전화번호를 입력하여 전화번호부에 저장하는 함수

@app.route('/search', methods=['POST'])
def search():
        name = request.form['name']
        # 데이터를 POST 방식으로 주고받기 때문에 request.form() 메소드를 이용
        phonebook = dict()
        # index.html에 수정될 내용을 전달할 딕셔너리 생성
        file = open('./data/phonebook.txt', 'r')
        for line in file.readlines():
            tmp=line.split(",",1)
            phonebook[tmp[0]]=tmp[1]
        tel = phonebook.get(name)
        msg = '검색되었습니다.'
        if(phonebook.get(name)!=True):
               msg = '없는 이름입니다.'
        file.close()

        return render_template('index.html', msg = msg, name = name, tel = tel)
        # render_template 메소드를 활용하여 index.html를 렌더링하고, index.html에 msg, name, tel을 전달
# 이름을 입력하면 전화번호를 찾아주는 함수

@app.route('/view', methods=['GET'])
def view():
        phonebook = dict()
        # view.html에 전달할 딕셔너리 생성
        file = open('./data/phonebook.txt', 'r')
        for line in file.readlines():
            tmp=line.split(",",1)
            phonebook[tmp[0]]=tmp[1]

        return render_template('view.html', dict = phonebook)
        # render_template 메소드를 활용하여 view.html를 렌더링하고, view.html에 dict를 전달
# 전화번호부를 보여주는 함수

@app.route('/init/', methods=['GET'])
def init():
       file = open('./data/phonebook.txt', 'w')
       # phonebook.txt를 w(쓰기 모드)로 오픈함.
       file.close()
       # 쓰기 모드로 오픈한 경우 파일 내용을 모두 지운 후 만들기 때문에 파일을 초기화하는 역할을 수행
       return render_template('index.html', msg='초기화되었습니다')
       # render_template 메소드를 활용하여 index.html를 렌더링하고, index.html에 msg를 전달
# 전화번호부 파일 초기화

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=True)