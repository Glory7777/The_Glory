from django.db import models
from spUser.models import SpUser
from DataBase.models import Tal

# Create your models here.


class Favorite(models.Model):
    name = models.ForeignKey(
        SpUser, on_delete=models.CASCADE, verbose_name='사용자')
    post = models.ForeignKey(Tal, on_delete=models.CASCADE, verbose_name='술정보')
    like = models.IntegerField(verbose_name='좋아요')
    register_date = models.DateTimeField(
        auto_now_add=True, verbose_name="등록일자")

    def __str__(self):
        return str(self.name) + " " + str(self.post)

    class Meta:
        db_table = "favorite_database"
        verbose_name = "관심주류"
        verbose_name_plural = "관심주류들"
