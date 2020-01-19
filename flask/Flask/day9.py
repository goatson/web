"""
from flask import Flask  #conda install flask 설치

app = Flask(__name__) #

#127.0.0.1:5000/
@app.route("/")  # / 생략가능
def home():
    return "<html><body><hr />문기성<hr/></body></html>"


#127.0.0.1:5000/index
@app.route("/index")
def index():
    return "index page"

if __name__ == '__main__':
    app.run(debug=True)  #서버 구동    

#크롬에서 127.0.0.1:5000
"""
#아이디 폰번호

from flask import Flask,render_template, redirect, request #conda install flask 설치

app = Flask(__name__) #from flask import Flask,render_template, redirect, request #conda install flask 설치

#127.0.0.1:5000/
@app.route("/")  # / 생략가능
def home():
    a1 = [1,2,3,4,5,6,7,8,9,10]
    return render_template('home.html', title="손흥민", num='7', team="토트넘", a1=a1)


#127.0.0.1:5000/index
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/join", methods=['GET'])
def join():
    return render_template('join.html')    

@app.route("/join", methods=['POST'])     #주소창으로 접속 불가  = 클릭해야 이동
def join_post():
    a = request.form['id']  # 'id' => <input type="text" name="id">
    b = request.form['pw']
    c = request.form['name']
    d = request.form['tel1']
    e = request.form['tel2']
    f = request.form['tel3']
    g = request.form['email1']
    h = request.form['email2']
    
    a1 = [a,b,c,d,e,f,g,h] #리스트로 만들기
    print(a1)



    #사용자가 입력한 정보를 받아서
    #DB에 넣고 페이지를 index 페이지로 전환시킴  #개발자가 DB 저장하기 위한 시간 버는 과정
    return redirect('index')


#127.0.0.1:5000/login
@app.route("/login", methods=['GET'])
def login_get():
    return render_template('login.html')  

@app.route("/login", methods=['POST'])
def login_post():
    return redirect("/")


#127.0.0.1:5000/ex01
@app.route("/ex01", methods=['GET'])
def ex01():
    return render_template("ex01.html")


#127.0.0.1:5000/ex01_1?n1=4&n2=5
@app.route("/ex01_1", methods=['GET'])
def ex01_1():
   
    n1 = request.args.get('n1',0)
    n2 = request.args.get('n2',0)
    n3 = request.args.get('n3',0)
    a1 = [n1, n2, n3, int(n1)+int(n2)+int(n3)]
    
    return render_template("ex01_1.html", a1=a1)    


@app.route("/ex02", methods=['GET'])
def ex02():
    return render_template("ex02.html")

@app.route("/ex02_1", methods=['GET'])
def ex02_1():
    m1 = request.args.get('m1',0)
    m2 = request.args.get('m1',0)
    b1 = [m1, m2, int(m1)*int(m2)]

    return render_template('ex02_1.html', b1=b1)
    



if __name__ == '__main__':
    app.run(debug=True)  #서버 구동    