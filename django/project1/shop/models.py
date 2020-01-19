from django.db import models


class Student(models.Model) :
    objects = models.Manager()
    id     = models.CharField(max_length=30, primary_key=True)
    age    = models.IntegerField()
    name   = models.CharField(max_length=30)
    
    def __str__(self):
        return str(self.id+","+str(self.age)+","+self.name)
        
        #객체가 들어갔을때 출력되는 용도



class Item(models.Model):
    objects     = models.Manager()  #VS code오류 제거용
    itm_no      = models.AutoField(primary_key=True)
    itm_name    = models.CharField(max_length=100) #VARCHAR2 100
    itm_content = models.TextField()  # CLOB
    itm_price   = models.IntegerField() #NUMBER
    itm_qty     = models.IntegerField() #NUMBER
    itm_date    = models.DateTimeField(auto_now_add=True)  # DATE
    # ballon_dor  = models.CharField(max_length=100) #VARCHAR2 100

    def __str__(self):
        return str(self.itm_no) #문자만 가능

        
