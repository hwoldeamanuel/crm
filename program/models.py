from django.db import models
from django.contrib.auth.models import User
import datetime
from app_admin.models import Region, Zone, Woreda
from portfolio.models import Portfolio
from user.models import Profile
 
# Create your models here.
class Program(models.Model):
    Four = 1
    Three = 2
    
    
    Approval_Team = (
        (Four, 'Four'),
        (Three, 'Three'),
       
       
        )
    title = models.CharField(max_length=100)
    working_title = models.CharField(max_length=255, null=True, blank=True)
    users_role =  models.ManyToManyField(User, through='UserRoles' ,blank=True)
    travel_users_role =  models.ManyToManyField(Profile, through='TravelUserRoles',related_name='traveluserroles' ,blank=True)
    carm_users_role =  models.ManyToManyField(Profile, through='CarmUserRoles', related_name='carmuserroles' ,blank=True)
    fund_code = models.CharField(max_length=200, unique=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    donor = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    portfolio = models.ForeignKey(Portfolio, null=True, blank=True,on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    no_approval_team = models.PositiveSmallIntegerField(choices=Approval_Team,blank=True, null=True)

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
    def __str__(self):
        return self.title

class ImplementationArea(models.Model):
    program =  models.ForeignKey(
        Program, on_delete=models.CASCADE, null=True, blank=True)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, null=True, blank=True)
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, null=True, blank=True)
    woreda = models.ForeignKey(
        Woreda, on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        unique_together = ('program', 'woreda')
        
        ordering = ('-region',)
        
    def __str__(self):
        return str(self.woreda)
    
class UserRoles(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    program = models.ForeignKey(Program, on_delete=models.DO_NOTHING)
    is_pcn_initiator = models.BooleanField(default=False)
    is_pcn_mel_approver = models.BooleanField(default=False)
    is_pcn_technical_approver = models.BooleanField(default=False)
    is_pcn_program_approver = models.BooleanField(default=False)
    is_pcn_finance_approver = models.BooleanField(default=False)
    is_pacn_initiator = models.BooleanField(default=False)
    is_pacn_mel_approver = models.BooleanField(default=False)
    is_pacn_technical_approver = models.BooleanField(default=False)
    is_pacn_program_approver = models.BooleanField(default=False)
    is_pacn_finance_approver = models.BooleanField(default=False)
    approval_budget_min_usd = models.FloatField(null=True, blank=True)
    approval_budget_max_usd = models.FloatField(null=True, blank=True)

    
    def __str__(self):
        return str(self.user)
    
 
class Indicator(models.Model):
    Output = 1
    Outcome = 2
    Impact = 3
    
    LEVEL = (
        (Output, 'Output'),
        (Outcome, 'Outcome'),
        (Impact, 'Impact'),
       
        )
    Numeric = 1
    Percentage = 2
    Other = 3
    
    UNIT = (
        (Numeric, 'Numeric'),
        (Percentage, 'Percentage'),
        (Other, 'Other'),
       
        )
    program =  models.ForeignKey(
        Program, on_delete=models.CASCADE, null=True, blank=True)
    indicator_no = models.CharField(max_length=200)
    indicator_title = models.CharField(max_length=255)
    indicator_level = models.PositiveSmallIntegerField(choices=LEVEL,blank=True, null=True)
    indicator_unit = models.PositiveSmallIntegerField(choices=UNIT, blank=True, null=True)
    indicator_baseline =  models.PositiveIntegerField(blank=True, null=True)
    indicator_target_LoP =  models.PositiveIntegerField(blank=True, null=True)
    
    
    def __str__(self):
        return self.indicator_title


class TravelUserRoles(models.Model):
    profile = models.ForeignKey(Profile, related_name='travel_profile', on_delete=models.DO_NOTHING)
    program = models.ForeignKey(Program,related_name='travel_program', on_delete=models.DO_NOTHING)
    is_initiator = models.BooleanField(default=False)
    is_budget_holder = models.BooleanField(default=False)
    is_finance_reviewer = models.BooleanField(default=False)
    is_security_reviewer = models.BooleanField(default=False)
   

    
    def __str__(self):
        return str(self.profile)
    

class CarmUserRoles(models.Model):
    profile = models.ForeignKey(Profile, related_name='carm_profile', on_delete=models.DO_NOTHING)
    program = models.ForeignKey(Program,related_name='carm_program', on_delete=models.DO_NOTHING)
    is_officer = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
   
   

    
    def __str__(self):
        return str(self.profile)