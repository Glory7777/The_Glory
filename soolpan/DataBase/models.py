from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tal(models.Model): #class 변경 필요 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True, verbose_name='제품명')
    company = models.CharField(max_length=256, blank=True, null=True, verbose_name='제조사')
    mtrl = models.CharField(max_length=256, blank=True, null=True, verbose_name='원재료') 
    std = models.CharField(max_length=256, blank=True, null=True, verbose_name='용량/도수')
    dsc = models.CharField(max_length=512, blank=True, null=True, verbose_name='상세설명')
    img = models.CharField(max_length=256, blank=True, null=True, verbose_name='이미지')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "traditional_liq"
        verbose_name = "전통주"
        verbose_name_plural = "전통주들"
            

    #규격,도수,전통주명,제조사,주원료

class Comment(models.Model):
    tal = models.ForeignKey(Tal,related_name='comments' ,on_delete=models.CASCADE, verbose_name='술')
    name = models.CharField(max_length=80, verbose_name='이름')
    body = models.TextField(verbose_name='본문')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')

    def __str__(self):
        return f'{self.name}--{self.body}'
    
    class Meta:
        db_table = "comment_data"
        verbose_name='댓글'
        verbose_name_plural='댓글들'