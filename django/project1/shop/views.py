from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from base64 import b64encode

from .models import Item
from .models import Student  #model 추가

import pandas as pd
import matplotlib.pyplot as plt  #그래프 그리기
from matplotlib import font_manager, rc  #한글 적용 폰트 설정
import io   #그래프를 byte로 변경
import base64  #웹에 출력하기 위해서

from django.db.models import Max, Min, Avg, Count, Sum

# auth 관련 모듈
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


# print(Student.objects)


@csrf_exempt
def auth_join(request) :
    if request.method == "GET" :
        return render(request, 'shop/auth_join.html')
    elif request.method == "POST" :
        id = request.POST['username']
        pw = request.POST['password']
        na = request.POST['first_name']
        em = request.POST['email']

        obj = User.objects.create_user(
            username=id,
            first_name = na,
            password = pw,
            email = em)
        obj.save()  #INSERT와 같음
        
        return redirect("/shop/auth_index")

@csrf_exempt
def auth_index(request):
    if request.method == "GET":
        return render(request, "shop/auth_index.html")


@csrf_exempt
def auth_login(request):
    if request.method == "GET" :
        return render(request, "shop/auth_login.html")
    elif request.method == "POST" :
        id = request.POST['username']
        pw = request.POST['password']

        user = authenticate(request, username=id, password=pw)  #SELECT 역할
        if user is not None :
            login(request, user) # 로그인 처리
            return render(request, 'shop/alert.html',
                {"msg":"로그인 성공", "url":"/shop/auth_index"})  #redirect와 같다(trick)
            # return redirect("/shop/auth_index")
        else :
            return redirect("/shop/auth_login")
        

def auth_logout(request):
    logout(request)
    return redirect("/shop/auth_index")

@csrf_exempt
def auth_edit(request) :
    if request.method == "GET" :
        if not request.user.is_authenticated : #로그인 여부확인
            return redirect("/shop/auth_login")
        else :    
            user = User.objects.get(username=request.user)  
            print(user)  
            return render(request, 'shop/auth_edit.html',{"user":user})
    elif request.method == "POST" :
        id = request.POST['username']
        na = request.POST['first_name']
        em = request.POST['email']

        user = User.objects.get(username=id)
        user.first_name = na
        user.email = em
        user.save()
        return redirect("/shop/auth_index")  
        #user.password = "바꿀"X
        # user.set_password('1234') #비밀번호 변경 함수



@csrf_exempt
def auth_pw(request) :
    if request.method == "GET" :
        if not request.user.is_authenticated : #로그인 여부 확인
            return redirect("/shop/auth_login")
        else :
            return render(request, 'shop/auth_pw.html')
    elif request.method == "POST" :
        # 1. pw1 pw2를 받음
        # 2. id와 pw1을 이용해서 로그인 request.user
        # 3. 성공하면 pw2로 변경
        id = request.user  #세션
        # print(request.user) #son (username 출력)
        # print(request.user.username) #son (username 출력)
        # print(request.user.id) #28 (ID출력)
        # print(request.user.first_name) #흥민 (first name 출력)
        pw1 = request.POST['pw1']
        pw2 = request.POST['pw2']
        # pw3 = request.POST['pw3']
        
        user = authenticate(request, username=id, password=pw1) #SELECT역할
        if user is not None :
            user.set_password(pw2)
            user.save()
            return redirect("/shop/auth_index")
        else:
            return redirect("shop/auto_pw")

        print(user.username)
        # user.set_password(pw2)
        # user.save()


@csrf_exempt
def update_multi(request):
    if request.method == "GET":
        # one = Student.objects.get(id="id_1") #id가 id_1인 것 한개
        # print(type(one)) # => one.id  one.name
        # return render(request, 'shop/update_multi.html',{"abc":one})
        
        # [ (한줄), (한줄), (한줄) ]
        rows = Student.objects.all().order_by('id')[:10] #10개만
        # print( type(rows[0]) )  #첫번째 것 꺼내서 type확인
        # ['a','b',34]  one.0 one.1 one.2
        # ('a','b',45)  one.0 one.1 one.2
        # {"id":"a", "name":"b", "age":34}  one.id one.name one.age
        # Studunt object type => one.id, one.name one.age
        return render(request, 'shop/update_multi.html',{"abc":rows})
    
    elif request.method == "POST":
        id = request.POST.getlist("a[]")
        na = request.POST.getlist('b[]')
        ag = request.POST.getlist('c[]')


        objs = []
        for i in range(0, len(id), 1) :
        #UPDATE SHOP_STUDENT SET NAME=%s, AGE=%s WHERE ID=%s
            obj = Student.objects.get(id=id[i])
            obj.name = na[i]
            obj.age = ag[i]
            # obj.save()
            objs.append(obj)
        Student.objects.bulk_update(objs, ["name","age"])
        
        return redirect("/shop/update_multi")

@csrf_exempt
def insert_multi(request):
    if request.method == "GET":
        return render(request, 'shop/insert_multi.html')
    elif request.method == "POST":
        id1 = request.POST.getlist("id[]")  #중복된 name값
        na1 = request.POST.getlist("na[]")
        ag1 = request.POST.getlist("ag[]")

        objs = []       
        for i in range(len(id1)-1, -1 , -1) :
            # print(id1[i], na1[i], ag1[i])
            obj = Student(id=id1[i], name=na1[i], age=ag1[i])
            objs.append(obj)
            # obj.save()

        Student.objects.bulk_create(objs) # batch commit
                    
        return redirect("/shop/insert_multi")


@csrf_exempt
def delete_multi(request) :
    if request.method == "GET" :
        rows = Student.objects.all()  #전체 조회
        print("deletemulti", type(rows[0]),rows[0] ) # one.id, one.name

        rows1 = Student.objects.raw("SELECT * FROM SHOP_STUDENT")
        # print( type(rows1[0]) )
        return render(request, 'shop/delete_multi.html', {"data":rows1})

    elif request.method == "POST" :
        chk = request.POST.getlist("chk[]")
        print(chk)
        #Student.objects.filter(id__in=[삭제하고자 하는 id 리스트])
        Student.objects.filter(id__in=chk).delete() # 다중 삭제
        return redirect("/shop/delete_multi")



def select1(request):
    # SELECT SUM(age) FROM SHOP_STUDENT
    a = Student.objects.aggregate(Sum('age'))  #나이 합
    print(a["age__sum"]) # 딕셔너리 키를 바꿀 수 없음

    # 딕셔너리 타입으로 반환
    # SELECT MAX(age) FROM SHOP_STUDENT
    obj = Student.objects.aggregate(max1=Max('age'))
    print(obj['max1'])  # 딕셔너리 키를 max1로 바꿈

    # obj1 = Student.objects.raw("SELECT * FROM SHOP_STUDENT WHERE age <= 20")
    obj1 = Student.objects.filter(age__lte=20)
    print(obj1)

    # html 파일을 만들지 않고 출력
    return HttpResponse("select1 page")

def dataframe(request):
    obj = Student()
    obj.id='MB'
    obj.age=72
    obj.name='이명박'
    obj.save()

    # obj1 = Student(id='PJH'', age=68, name='박근혜')  #Insert
    # obj1.save()

    data = list(Student.objects.all().values())
    df = pd.DataFrame(data)
    print(df)
    data1 = df.values.tolist()  #df to list로 변경  [ [],[],[] ]   ###시험문제 tolist()  createX

    return render(request, 'shop/dataframe.html',
                           {"key":df.to_html(classes='table'),
                            "key1":data1
                            }
                            )

def itemdataframe(request):
    # obj = Item()
    # obj.id='MB'
    # obj.age=72
    # obj.name='이명박'
    # obj.save()

    # obj1 = Student(id='PJH'', age=68, name='박근혜')  #Insert
    # obj1.save()
    ord = int(request.GET.get("order", 1))

    if ord == 1 :
        #"SELECT * FROM SHOP_ITEM ORDER BY itm_no ASC"
        data = list(Item.objects.all().values().order_by('itm_no'))
        
        df = pd.DataFrame(data)
        # print(df)   
        # data1 = df.values.tolist()

    if ord == 2 :
        data = list(Item.objects.all().values().order_by('-itm_no'))  
        # [ {"itm_no" :78, "itm_name":8, "itm_content" : 1256 }, { : }, { : }, {"itm_no" :78, "itm_name":8 }, { : }, { : } ]
        #print(type(data[0])) 
    

        df = pd.DataFrame(data)     
        # print(df)   
        # data1 = df.values.tolist()

    # return redirect('/shop/itemdataframe')

    return render(request, 'shop/itemdataframe.html',
                            { "key":df.to_html(classes='table'), "data":data} 
                            )           



                            
    #html에서 사용방법
    #{% for a in data %}
        #{ {a.itm_no} }
    #{% endfor %}

    # d = list(Item.objects.all().values().order_by('-itm_no'))
    # df_d=pd.DataFrame(d)
    # data_d = df_d.values.tolist()

    # a = list(Item.objects.all().values().order_by('itm_no'))
    # df_a = pd.DataFrame(a)
    # print(df)
    # data_a = df_a.values.tolist()

    

    # data = list(Item.objects.all().values())
    # df = pd.DataFrame(data)
    # print(df)
    # data1 = df.values.tolist()  #df to list로 변경  [ [],[],[] ]   ###시험문제 tolist()  createX

    


@csrf_exempt
def itemdataframe_a(request):
    #SELECT * FROM SHOP_ITEM ORDER BY itm_no DESC
    data = list(Item.objects.all().values().order_by('-itm_no'))
    df = pd.DataFrame(data)
    print(df)
    data1 = df.values.tolist()

    return render(request, 'shop/itemdataframe_a.html',
                           {"key":df.to_html(classes='table'),
                            "a":data1})


@csrf_exempt
def itemdataframe_b(request):
    #SELECT * FROM SHOP_ITEM ORDER BY itm_no ASC
    data = list(Item.objects.all().values().order_by('itm_no'))
    df = pd.DataFrame(data)
    print(df)
    data1 = df.values.tolist()

    return render(request, 'shop/itemdataframe_b.html',
                           {"key":df.to_html(classes='table'),
                            "b":data1})



@csrf_exempt
def graph(request):
    # cursor = connection.cursor()     #cursor 얻기
    # sql = "SELECT * FROM SHOP_STUDENT ORDER BY ID DESC"
    # cursor.execute(sql)
    # rows=cursor.fetchall()
    # print(rows)


    # SELECT * FROM STUDENT
    rows = Student.objects.all()  #QuerySet:Dictionary 개념 [ [], [], []]
    x = [10,20,30,40,50,60,70]
    y = [0,0,0,0,0,0,0]
    for t in rows:
        print("{},{},{}".format(t.id, t.name, t.age))
        if 0<= t.age <=19 :
            y[0] += 1
        elif 20 <= t.age <=29 :
            y[1] += 1
        elif 30 <= t.age <=39 :
            y[2] += 1
        elif 40 <= t.age <=49 :
            y[3] += 1
        elif 50 <= t.age <=59 :
            y[4] += 1
        elif 60 <= t.age <=69 :
            y[5] += 1
        elif 70 <= t.age <=69 :
            y[6] += 1

    #한글 폰트 사용하기
    font_name = font_manager.FontProperties(fname="C:/Windows/Fonts/gulim.ttc").get_name()
    rc('font', family=font_name)
    
    plt.bar(x, y)
    plt.title('Messi % SON')
    plt.xlabel('kang-in')
    plt.ylabel('이승우')
    plt.draw()  #그래프 그리기
    img = io.BytesIO()  #그린 그래프를 byte로 변경
    plt.savefig(img, format="png")  #png포맷으로 변경
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()  #그래프 종료
    return render(request, 'shop/graph.html',
        {"graph1":'data:image/png;base64,{}'.format(graph_url)} )

        #graph.html에서 출력시
        #<img src="{{graph1}}"  /> 태그 사용


@csrf_exempt
def itemgraph(request):
    # cursor = connection.cursor()     #cursor 얻기
    # sql = "SELECT * FROM SHOP_STUDENT ORDER BY ID DESC"
    # cursor.execute(sql)
    # rows=cursor.fetchall()
    # print(rows)


    # SELECT * FROM STUDENT
    rows = Student.objects.all()  #QuerySet:Dictionary 개념 [ [], [], []]
    x = [100,1000,10000,100000,1000000,10000000]
    y = [0,0,0,0,0,0]
    for t in rows:
        print("{},{},{}".format(t.id, t.name, t.age))
        if 0<= t.age <=19 :
            y[0] += 1
        elif 20 <= t.age <=29 :
            y[1] += 1
        elif 30 <= t.age <=39 :
            y[2] += 1
        elif 40 <= t.age <=49 :
            y[3] += 1
        elif 50 <= t.age <=59 :
            y[4] += 1
        elif 60 <= t.age <=69 :
            y[5] += 1
        elif 70 <= t.age <=69 :
            y[6] += 1

    #한글 폰트 사용하기
    font_name = font_manager.FontProperties(fname="C:/Windows/Fonts/gulim.ttc").get_name()
    rc('font', family=font_name)
    
    plt.bar(x, y)
    plt.title('Messi % SON')
    plt.xlabel('kang-in')
    plt.ylabel('이승우')
    plt.draw()  #그래프 그리기
    img = io.BytesIO()  #그린 그래프를 byte로 변경
    plt.savefig(img, format="png")  #png포맷으로 변경
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()  #그래프 종료
    return render(request, 'shop/graph.html',
        {"graph1":'data:image/png;base64,{}'.format(graph_url)} )

        #graph.html에서 출력시
        #<img src="{{graph1}}"  /> 태그 사용


@csrf_exempt
def graphinsert(request):
    if request.method == "GET":
        return render(request, 'shop/graphinsert.html')
    elif request.method == "POST":
        id = request.POST['id']
        age = request.POST['age']
        na = request.POST['na']
        
        obj = Student(id=id, age=age, name=na)
        obj.save()  #INSERT
        return redirect('/shop/index')



@csrf_exempt
def index(request):
    if request.method == "GET":
        return render(request, 'shop/index.html')
    
@csrf_exempt
def insert(request):
    if request.method == "GET":
        return render(request, 'shop/insert.html')
    elif request.method == "POST":
        na = request.POST['na']
        co = request.POST['co']
        pr = request.POST['pr']
        qt = request.POST['qt']
        # messi = request.POST['messi']

        obj = Item(itm_name=na, itm_content=co, itm_price=pr, itm_qty=qt)
        obj.save()  #INSERT
        return redirect('/shop/select')

    
@csrf_exempt
def select(request):
    if request.method == "GET" :
        rows = Item.objects.all()
        #rows = Item.objects.raw("SELECT * FROM SHOP_ITEM ORDER BY ITM_NO DESC")
        return render(request, 'shop/select.html', {"rows":rows})



@csrf_exempt
def update(request):
    if request.method == "GET" :
        no = request.GET.get("no", 0)  #request.GET['no']
        a = Item.objects.get(itm_no=no)  #조건에 맞는 객체 얻기
        return render(request, 'shop/update.html', {"one" : a})

    elif request.method == "POST":
        b = Item.objects.get(itm_no=request.POST['no'])
        b.itm_name = request.POST['na']
        b.itm_content = request.POST['co']
        b.itm_price = request.POST['pr']
        b.itm_qty = request.POST['qt']
                
        b.save()
        return redirect('/shop/select')


def delete(request):
    if request.method == "GET" :
        no = request.GET.get('no', 0)
        obj = Item.objects.get(itm_no=no)
        obj.delete()
        # print(obj.query)
        return redirect('/shop/select')
        
