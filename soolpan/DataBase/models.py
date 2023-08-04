from django.db import models

# Create your models here.
class Tal(models.Model): #class 변경 필요 
    
    size = models.CharField(max_length=256, blank=True, null=True, verbose_name="용량")    
    per = models.IntegerField(blank=True, null=True, verbose_name="도수")
    name = models.CharField(max_length=256, blank=True, null=True, verbose_name='제품명')
    company = models.CharField(max_length=256, blank=True, null=True, verbose_name='제조사')
    mtrl = models.CharField(max_length=256, blank=True, null=True, verbose_name='원재료')   
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "traditional_liq"
        verbose_name = "전통주"
        verbose_name_plural = "전통주들"
            

    #규격,도수,전통주명,제조사,주원료