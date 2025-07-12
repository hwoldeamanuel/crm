from django.db import models
from app_admin.models import Portfolio_Type, Portfolio_Category, Region, Zone, Woreda
from portfolio.models import Portfolio
from program.models import Program
# Create your models hedfd
import datetime
from django.contrib.auth.models import User
    
class Partnership(models.Model):  
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    partership_type =  models.TextField(null=True, blank=True)
    agreement_type =  models.TextField(null=True, blank=True)
    total_budget = models.FloatField(null=True, blank=True)
    subAwar_code = models.TextField(null=True, blank=True)
    start_date =  models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    
    
    def __str__(self):
        return self.portfolio
    
    def get_date_diff(self):
        if self.start_date and self.end_date:
             dt1 = self.start_date
             dt2 = self.end_date
             dt = datetime.date.today()
             if abs((dt2-dt1).days) > 0 and abs((dt2-dt1).days) > 0:
                  diff = str(round((abs((dt-dt1).days)/abs((dt2-dt1).days))*100,0))+'%'
             else:
                  diff = 0
             
             return  diff


class Contribution(models.Model):  
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    partnership = models.ForeignKey(Partnership, on_delete=models.CASCADE)
    source = models.TextField(null=True, blank=True)
    kind =  models.TextField(null=True, blank=True)
    amount =  models.FloatField(null=True, blank=True)


     
    def __str__(self):
        return self.partnership
    

class Monitoring(models.Model):  
    partnership = models.ForeignKey(Partnership, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    start_date =  models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    submission_date = models.DateField(null=True, blank=True)
    desciption = models.TextField(null=True, blank=True)
    report_att = models.FileField(null=True,  blank=True, upload_to='documents/')
    status = models.BooleanField(null=True,blank=True, default=False)
        
    def __str__(self):
        return self.partnership

class Payment(models.Model):  
    partnership = models.ForeignKey(Partnership, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    start_date =  models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    desciption = models.TextField(null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    
        
    def __str__(self):
        return self.partnership