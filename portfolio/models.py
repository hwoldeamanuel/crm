from django.db import models
from app_admin.models import Portfolio_Type, Portfolio_Category, Region, Zone, Woreda
# Create your models here.

    
    
class Portfolio(models.Model):  
   
    title = models.CharField(max_length=250)
    title_short = models.CharField( max_length=100)
    type =  models.ForeignKey(Portfolio_Type, on_delete=models.CASCADE)
    category =  models.ForeignKey(Portfolio_Category, on_delete=models.CASCADE)
    start_date = models.DateField(null=True, blank=True)
    
    logo = models.ImageField(upload_to ='documents/', null=True, blank=True) 
    description = models.TextField(null=True, blank=True)
    address_url = models.URLField(max_length = 200, null=True, blank=True) 
    
    def __str__(self):
        return self.title_short


class FieldOffice(models.Model):
    name = models.CharField(max_length=100)
    portfolio =  models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name='officeregion', null=True, blank=True)
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, related_name='officezone', null=True, blank=True)
    woreda = models.ForeignKey(
        Woreda, on_delete=models.CASCADE, related_name='officeworeda', null=True, blank=True)

    def __str__(self):
        return self.name
    


