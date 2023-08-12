from django.db import models
from spUser.models import SpUser
from DataBase.models import Tal

# Create your models here.


class Favorite(models.Model):
    name = models.ForeignKey(
        SpUser, on_delete=models.CASCADE, verbose_name='사용자')
    post = models.ForeignKey(Tal, related_name="rel_name_tal", on_delete=models.CASCADE, verbose_name='술정보')
    like = models.IntegerField(verbose_name='좋아요')
    register_date = models.DateTimeField(
        auto_now_add=True, verbose_name="등록일자")

    def __str__(self):
        return str(self.name) + " " + str(self.post)
    
    #중요 포린키를 타고 다른 모델의 attr을 끌고와서 할당하는 메소드
    def get_tal_image_url(self):
        if self.post and hasattr(self.post, 'img'):
            return self.post.img.url
        return None
    
    def get_tal_like(self):
        if self.post and hasattr(self.post, 'like'):
            return self.post.like
        return None
    
    class Meta:
        db_table = "favorite_database"
        verbose_name = "관심주류"
        verbose_name_plural = "관심주류들"
