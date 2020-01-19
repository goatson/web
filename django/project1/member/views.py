from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from base64 import b64encode


def index(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM member")
    row = cursor.fetchall()
    print(row)

    # return HttpResponse("index page")
    return render(request, 'member/index.html')


@csrf_exempt
def join(request):
    if request.method == "GET":
        return render(request, "member/join.html")
    elif request.method == "POST" :
        a = request.POST['id']
        b = request.POST['pw']
        # c = request.POST['pw1']
        d = request.POST['name']
        e = request.POST['tel1']
        f = request.POST['tel2']
        g = request.POST['tel3']
        h = request.POST['email1']
        i = request.POST['email2']

        # if b != c : 
        #     return redirect('join?chk=error')   
        # else :
        #     pass

        a1 = [a, b, d, ( e + "-" + f + "-" + g), (h+"@"+i)] #리스트로 만들기
        cursor = connection.cursor()
        sql = """
            INSERT INTO MEMBER
            (MEM_ID, MEM_PW, MEM_NAME, MEM_TEL, MEM_EMAIL, MEM_DATE) 
             VALUES(%s, %s, %s, %s, %s, SYSDATE)
             """
        cursor.execute(sql, a1)
        connection.commit()

        return redirect("/member/index")  # 주소창 입력후 엔터키
                                         # 화면은 바꾸지만 주소창 유지 


@csrf_exempt
def list(request):
    cursor = connection.cursor()     #cursor 얻기
    sql = "SELECT * FROM MEMBER ORDER BY MEM_ID DESC"
    cursor.execute(sql)             #SQL문 수행
    rows = cursor.fetchall()        #결과값 받기
    print(rows)  #[(),(),()]

    return render(request, "member/list.html", {"data":rows})  #!!!! "  " 는 무엇?




@csrf_exempt
def edit(request):
    if request.method == "GET" :
        id = request.GET.get('id',0)  #5가 들어감
        cursor = connection.cursor()
        print(id)
        sql = "SELECT * FROM MEMBER WHERE MEM_ID=%s"
        cursor.execute(sql, [id])  #SQL 문 수행
        one = cursor.fetchone()    #결과값 받기
        #DB에서 해당 게시물 1개 가져옴
        return render(request, 'member/edit.html', {"one" : one})

    elif request.method == "POST" :
        a = request.POST['id']
        b = request.POST['pw']
        c = request.POST['name']
        a1 = [b, c, a]

        cursor = connection.cursor()
        sql = "UPDATE MEMBER SET MEM_PW=%s, MEM_NAME=%s WHERE MEM_ID=%s"
        cursor.execute(sql, a1)
        
        return redirect("/member/index")


@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, 'member/login.html')

    if request.method == "POST":
        id = request.POST['id']
        pw = request.POST['pw']
        a1=[id, pw]
        # print(a1)
        cursor = connection.cursor()
        sql = "SELECT MEM_ID, MEM_NAME FROM MEMBER WHERE MEM_ID=%s AND MEM_PW=%s"
        cursor.execute(sql, a1)  
        mone = cursor.fetchone()   #( ID, PW )
        # print(mone)
        
        if mone :   # 이미 비교 끝
            #a = request.session['userid']  다른 views에서 꺼낼 때
            request.session['userid'] = mone[0]     # 세션에 값 넣기  
            request.session['username'] = mone[1]
            # print(request.session['login'])
            print("로그인 성공")  
        else :
            print("로그인 실패")
        
        return redirect("/member/index" )


@csrf_exempt
def logout(request):
    if request.method == "GET":
        del request.session['userid']    # 세션에 값 지우기
        del request.session['username']  # del a["ret"]
        print("로그아웃 되었습니다.")
        return redirect("/member/index")


# @csrf_exempt
# def memberdel(requset):
#     if 

