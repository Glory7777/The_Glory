from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from spUser.models import SpUser
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(SpUser, on_delete=models.CASCADE, verbose_name="작성자")
    title = models.CharField(max_length=128, verbose_name="제목")
    text = models.TextField(verbose_name="본문")
    image = models.ImageField(upload_to="posts/", null=True, blank=True, verbose_name="이미지")
    #pip install pillow
    created_date = models.DateTimeField(default=timezone.now, verbose_name="작성일")
    #게시물이 데이터베이스에 생길 때 자동으로 현재 시간으로 설정
    published_date = models.DateTimeField(null=True, blank=True, verbose_name="게시일")
    # 게시물이 공개된 날짜와 시간을 저장, 이 필드는 null 허용

        # null=True, null 허용 / blank=True, 폼을 검증하라는 뜻 
    
    def __str__(self):
        return self.title

    #게시물 날짜와 시간을 설정하고, 그 정보를 데이터베이스에 반영
    def published(self):
        self.published_date = timezone.now()
        self.save()
        
    class Meta:  
        db_table = "img_blog"
        verbose_name = "나의 술자랑"
        verbose_name_plural = "나의 술자랑들"