from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from base64 import b64encode

# from .models import Item

#127.0.0.1:8000/member/index
def index(request):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM board")
    row = cursor.fetchall()
    print(row)

    # return HttpResponse("index page")
    return render(request, 'board/index.html')

# Create your views here.




@csrf_exempt
def write(request):
    if request.method == "GET":
        return render(request, "board/write.html")
    elif request.method == "POST":
        ti = request.POST['ti']     #<input type name="ti"
        co = request.POST['co']     #<textarea name="co"
        img = request.FILES['img']  #<input type name="fi"
        wr = request.POST['wr']     #<input type nate="wr"

        a1 = [ti, co, img.read(), wr]
        # print(a1)

        cursor = connection.cursor()
        sql = """
            INSERT INTO BOARD
            (BRD_NO, BRD_TITLE, BRD_CONTENT, BRD_IMG, BRD_WRITER, BRD_HIT, BRD_DATE) 
             VALUES(SEQ_BOARD_NO.NEXTVAL, %s, %s, %s, %s, 1, SYSDATE)   
             """
        cursor.execute(sql, a1)
        # connection.commit()

        return redirect("/board/index")

# @csrf_exempt
# def join(request):
#     if request.method == "GET":
#         return render(request, "board/join.html")
#     elif request.method == "POST" :
#         a = request.POST['id']
#         b = request.POST['pw']
#         # c = request.POST['pw1']
#         d = request.POST['name']
#         e = request.POST['tel1']
#         f = request.POST['tel2']
#         g = request.POST['tel3']
#         h = request.POST['email1']
#         i = request.POST['email2']

#         # if b != c : 
#         #     return redirect('join?chk=error')   
#         # else :
#         #     pass

#         a1 = [a, b, d, ( e + "-" + f + "-" + g), (h+"@"+i)] #리스트로 만들기
#         cursor = connection.cursor()
#         sql = """
#             INSERT INTO MEMBER
#             (MEM_ID, MEM_PW, MEM_NAME, MEM_TEL, MEM_EMAIL, MEM_DATE) 
#              VALUES(%s, %s, %s, %s, %s, SYSDATE)
#              """
#         cursor.execute(sql, a1)
#         connection.commit()

#         return redirect("/board/index")  # 주소창 입력후 엔터키
#                                          # 화면은 바꾸지만 주소창 유지 


@csrf_exempt
def list(request):
    cursor = connection.cursor()     #cursor 얻기
    sql = "SELECT * FROM BOARD ORDER BY BRD_NO DESC"
    cursor.execute(sql)             #SQL문 수행
    rows = cursor.fetchall()        #결과값 받기
    print(rows)  #[(),(),()]

    return render(request, "board/list.html", {"data":rows})  #!!!! "  " 는 무엇?


@csrf_exempt
#127.0.0.1:8000/board/content?no=5
def content(request) :
    no = request.GET.get("no", 0)  #5가 들어감
    print(no)
    cursor = connection.cursor()
    sql = "SELECT * FROM BOARD WHERE BRD_NO=%s"
    cursor.execute(sql, [no])    # SQL문 수행
    one = cursor.fetchone()      # 결과값 받기
    print(one)                   # (   )
    # 0  ~  6
    if one[6] :
        data = one[6].read()         # 이미지파일    
        image = b64encode(data).decode("utf-8")
    else :
        file = open("./static/img/default.jpg", "rb")
        data = file.read()
        image = b64encode(data).decode("utf-8")

    return render(request, 'board/content.html', {"one":one,"image":image})






@csrf_exempt
def delete(request):
    if request.method == "POST" :
        no = request.POST['no']
        cursor = connection.cursor()
        sql = "DELETE FROM BOARD WHERE BRD_NO=%s"
        cursor.execute(sql, [no])
        return redirect("/board/list")


@csrf_exempt
def edit(request):
    if request.method == "GET" :
        no = request.GET.get('no',0)  #5가 들어감
        cursor = connection.cursor()
        sql = "SELECT * FROM BOARD WHERE BRD_NO=%s"
        cursor.execute(sql, [no])  #SQL 문 수행
        one = cursor.fetchone()    #결과값 받기
        #DB에서 해당 게시물 1개 가져옴
        return render(request, 'board/edit.html', {"one" : one})
    
    elif request.method == "POST" :
        #DB UPDATE
        a = request.POST['no']  #5가 들어감    
        b = request.POST['ti']   
        c = request.POST['co']
        a1 = [b,c,a]

        cursor = connection.cursor()
        sql = "UPDATE BOARD SET BRD_TITLE=%s, BRD_CONTENT=%s WHERE BRD_NO=%s"
        cursor.execute(sql, a1)
        return redirect("/board/list")



def son(request) :
    return render(request, 'board/son.html')