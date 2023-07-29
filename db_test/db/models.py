from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    
    size = models.CharField(max_length=256, blank=True, null=True, verbose_name="규격")    
    perecent = models.IntegerField(max_length=256, blank=True, null=True, verbose_name="도수")
    name = models.CharField(max_length=256, blank=True, null=True, verbose_name="전통주명")
    company = models.CharField(max_length=256, blank=True, null=True, verbose_name="제조사")
    mtrl = models.CharField(max_length=256, blank=True, null=True, verbose_name="주원료")   
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "traditional_liq"
        verbose_name = "전통주"
        verbose_name_plural = "전통주들"
        
    
    

    #규격,도수,전통주명,제조사,주원료