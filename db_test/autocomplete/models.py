from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Tal(models.Model): #class 변경 필요 
    
    size = models.CharField(max_length=256, blank=True, null=True)    
    per = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=256, blank=True, null=True)
    company = models.CharField(max_length=256, blank=True, null=True)
    mtrl = models.CharField(max_length=256, blank=True, null=True)   
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "traditional_liq2"
        verbose_name = "전통주"
        verbose_name_plural = "전통주들"
            

    #규격,도수,전통주명,제조사,주원료