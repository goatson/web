from datetime import timedelta
from  flask import Flask, render_template, redirect, request ,session
import day10_model as md

app = Flask(__name__) #객체 생성
app.secret_key = b'fefe#$$%4_F#f3f33fffA'  #세션 생성시 salt 값 / 암호화 할 때 만드는 키 값이 솔트
#암호화 하기위해 첨가물

#세션 시간 설정
@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(seconds=900)
#세션은 일정시간 지나면 자료삭제(30분 후 로그아웃)

member = md.memberModel()
board = md.boardModel()


@app.route("/index", methods=['GET'])
def index():
    return render_template('index.html')

#127.0.0.1:5000/login
@app.route("/login", methods=['GET'])
def login_get():
    return render_template('login.html')   

@app.route("/login", methods=['POST'])
def login_post():
    a = request.form['id']  
    b = request.form['pw']
    a1 = [a, b] # 아이디와 암호 값을 a1리스트에 추가
    mone = member.login(a1)
    # print(mone)
    if not mone :
        print("로그인 실패")
    else:
        print("로그인 성공")  
        session['userid'] = mone[0]  # 자료형 딕셔너리 {"userid":"a"}
        session['username'] = mone[1] #{"userid":"a", "username":"이름"}
    return redirect("index")

@app.route("/logout", methods=['GET'])
def logout():
    session.pop('userid', None)
    session.pop('username', None)
    return redirect('index')

#127.0.0.1:5000/join
@app.route("/join", methods=['GET'])
def join():
    return render_template('join.html')   

@app.route("/join", methods=['POST'])
def join_post():
    a = request.form['id']  # 'id' => <input type="text" name="id"
    b = request.form['pw']
    c = request.form['pw1']
    d = request.form['name']
    e = request.form['tel1']
    f = request.form['tel2']
    g = request.form['tel3']
    h = request.form['email1']
    i = request.form['email2']

    if b != c : 
        return redirect('join?chk=error')   
    else :
        pass
        
    
    a1 = [a, b, d, ( e + "-" + f + "-" + g), (h+"@"+i)] #리스트로 만들기
    member.join(a1)  
    return redirect('join_ok')   


@app.route("/join_ok", methods=['GET'])
def join_ok():
    return render_template('join_ok.html')


@app.route("/memberdel", methods=['GET'])
def memberdel_get():
    return render_template('memberdel.html')

@app.route("/memberdel", methods=['POST'])
def memberdel_post():
    a = request.form['id']  # 'id' => <input type="text" name="id"
    b = request.form['pw']

    a1 = [a, b]
    ret=member.delete(a1)

    if ret ==1:
        return redirect('memberdel_ok')
    elif ret ==0:
        return redirect('memberdel')

@app.route("/memberdel_ok", methods=['GET'])
def memberdel_ok():
    return render_template('memberdel_ok.html')    



@app.route("/memberlist", methods=['GET'])
def memberlist():
    data = member.memberlist()
    return render_template('memberlist.html', key = data)



@app.route("/boardw", methods=['GET'])
def boardw():   
    return render_template('boardw.html')    

@app.route("/boardw", methods=['POST'])
def boardw_post():   
    # a = request.args.get('ti',0)
    # b = request.args.get('co',0)
    # c = request.args.get('wr',0)
    a = request.form['ti']
    b = request.form['co']
    c = request.form['wr']

    a1 = [a, b, c]
    board.write(a1)
    # print(a1)
    #day10_model.py파일에  boardModel 클래스 생성 후 write 메소드 호출
    
    return redirect('board')
    

@app.route("/board", methods=['GET'])
def board_get():
    no = [ request.args.get('type', 'brd_title'), request.args.get('text', '') ]
    
    data = board.boardlist(no)
    session['boardhit'] = 1  #조회수 증가 방지용
    return render_template('board.html', key=data)

@app.route("/boardc", methods=['GET'])
def boardc_get():
    no = [ request.args.get('no', 0) ] # 리스트로 만듬 => [7]

    if 'boardhit' in session:
        if session['boardhit'] == 1 :
            board.boardhit(no) #조회수 1증가시키기
            session['boardhit'] = 0

    one = board.boardone(no) #상세내용 #model의 boardone함수 호출( 1,ㅁ,ㅁ,ㅁ,ㅁ )
    prev = board.boardprev(no)    #이전글 (1) prev[0]
    next = board.boardnext(no)    #다음글
    
    page = [one, prev, next]  #[( , , , ), (), ()]

    return render_template('boardc.html', key=page)  
    


#127.0.0.1:5000/boardd    ?no=3&n=67n
@app.route("/boardd", methods=['GET']) 
def boardd():   
    no = [ request.args.get('no', 0) ]
    board.boarddel(no)
    return redirect('board') #127,0,0,1:5000/board
    # return render_template('boardd.html')  # redner => no=78되있는데 목록으로 나올수도  
    # return render_template('board.html', key=data)


@app.route("/boarde", methods=['GET'])
def boarde_get():   
    no = [ request.args.get('no', 0) ]  #주소창에서 no 받음
    one = board.boardone(no)  #글번호를 넘겨서 해당 게시물 1개 가져옴
        
    return render_template('boarde.html', key=one)   #html로 내용 전달함


@app.route("/boarde", methods=['POST'])
def boarde_post():
    a = request.form['no']
    b = request.form['ti']
    c = request.form['co']
    a1 = [a, b, c]

    board.boardupdate(a1)
    # UPDATE BOARD SET BRD_TITLE=:2, BRD_CONTENT=:3 WHERE BRD_ID=:1
    return redirect("boardc?no=" + str(a))
    # return redirect('index')





# @app.route("/boarde", methods=['POST']) 
# def boardin_post():
    
#     no = request.args.get('no', 0) # 리스트로 만듬 => [7]
#     a = request.form['ti']
#     b = request.form['co']
    
#     a1 = [a, b, no]

#     board.boarde(a1)
#     # print(a1)
#     #day10_model.py파일에  boardModel 클래스 생성 후 write 메소드 호출
           
#     return redirect('board')



# @app.route("/boardin", methods=['POST'])
# def boardin():   
#     # a = request.args.get('ti',0)
#     # b = request.args.get('co',0)
    
#     a = request.form['ti']
#     b = request.form['co']
    

#     a1 = [a, b]
#     board.boardin(a1)
#     # print(a1)
#     #day10_model.py파일에  boardModel 클래스 생성 후 write 메소드 호출
    
#     return redirect('board')


if __name__ == '__main__':
    app.run(debug=True) # 서버 구동