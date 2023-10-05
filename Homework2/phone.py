from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/store/', methods=['GET'])
def store():
        name = request.args.get('name')
        tel = request.args.get('tel')

        file = open('./data/phonebook.txt', 'a')
        data = "%s,%s\n" % (name, tel)
        file.write(data)
        file.close()

        return render_template('index.html', msg='저장되었습니다.')
# 이름과 전화번호를 입력하여 전화번호부에 저장하는 함수

@app.route('/search', methods=['POST'])
def search():
        name = request.form['name']
        phonebook = dict()
        file = open('./data/phonebook.txt', 'r')
        for line in file.readlines():
            tmp=line.split(",",1)
            phonebook[tmp[0]]=tmp[1]
        tel = phonebook.get(name)
        file.close()

        return render_template('index.html', msg='검색되었습니다.', name = name, tel = tel)
# 이름을 입력하면 전화번호를 찾아주는 함수

@app.route('/view', methods=['GET'])
def view():
        phonebook = dict()
        file = open('./data/phonebook.txt', 'r')
        for line in file.readlines():
            tmp=line.split(",",1)
            phonebook[tmp[0]]=tmp[1]

        return render_template('view.html', dict = phonebook)
# 전화번호부를 보여주는 함수

@app.route('/init/', methods=['GET'])
def init():
       file = open('./data/phonebook.txt', 'w')
       file.close()
       return render_template('index.html', msg='초기화되었습니다')
# 전화번호부 파일 초기화

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=True)

'''
       CSS로 좀 더 꾸미기.
       추가할 만한 기능은 뭐가 있지?
'''