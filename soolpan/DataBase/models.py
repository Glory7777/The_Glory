from django.db import models
from spUser.models import SpUser
# Create your models here.
class Tal(models.Model): #class 변경 필요 
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256, blank=True, null=True, verbose_name='제품명')
    company = models.CharField(max_length=256, blank=True, null=True, verbose_name='제조사')
    mtrl = models.CharField(max_length=256, blank= True, null=True, verbose_name='원재료') 
    std = models.CharField(max_length=256, blank=True, null=True, verbose_name='용량/도수')
    dsc = models.CharField(max_length=512, blank=True, null=True, verbose_name='상세설명')
    img = models.CharField(max_length=256, blank=True, null=True, verbose_name='이미지')
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "traditional_liq"
        verbose_name = "전통주"
        verbose_name_plural = "전통주들"

class Comment(models.Model):
    post = models.ForeignKey(Tal, related_name="comments",on_delete=models.CASCADE, verbose_name="포스트")  #rel_name을 가지고서 views에서 사용, 역참조
    #포린키는 다:1관계 키, 즉, 1개의 글에 여러개의 댓글이 달림, 1개의 아이디로 여러 글을 쓸 수 있기 위해 사용되는 키
    name = models.ForeignKey(SpUser, related_name="userEmail",on_delete=models.CASCADE, verbose_name="이름")
    body = models.TextField(verbose_name="댓글")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    
    def __str__(self) -> str:
        return f'ID: {self.name}'

    class Meta:    
        db_table = "Comments_data"            
        verbose_name = "댓글"
        verbose_name_plural = "댓글들"            

    #규격,도수,전통주명,제조사,주원료
