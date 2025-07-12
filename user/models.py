from django.db import models
from django.contrib.auth.models import User
from portfolio.models import Portfolio
from app_admin.models import FieldOffice
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,related_name='profile')
    first_name = models.CharField(max_length=100,null=True, blank=True)
    last_name = models.CharField(max_length=100,null=True, blank=True)
    job_title =  models.CharField(max_length=100,null=True, blank=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='portfolio')
    contact_number = models.CharField(max_length=12, null=True, blank=True)
    field_office = models.ForeignKey(FieldOffice, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='ff')
    emp_id =  models.PositiveIntegerField(null=True, blank=True)
    reports_to = models.ForeignKey(
        User,
        related_name='inferiors',
       
        on_delete=models.DO_NOTHING,null=True, blank=True
    )
    

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)
    def full_name(self):
        return str(self.first_name) + " " + str(self.last_name)