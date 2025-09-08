from django.db import models
from django.db import models
from django.contrib.auth.models import User
from program.models import TravelUserRoles
from app_admin.models import Travel_Cost, Fund, Lin_Code, Approvalf_Status, Submission_Status
from django.db.models import Sum
from django.db.models import Q
from django.db.models.functions import ExtractDay
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save, pre_delete,pre_save
from django.dispatch import receiver

# Create your models here.
 
# Create your models here.
class Travel_Request(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True, related_name='requested_by')
    destination = models.TextField(null=True,  blank=True)
    purpose = models.TextField(null=True,  blank=True)
    departure_date = models.DateField(null=True, blank=True)
    return_date = models.DateField(null=True, blank=True)
   
    business = models.BooleanField(default=True)
    randr = models.BooleanField(default=False)
    relocation = models.BooleanField(default=False)
    other = models.BooleanField(default=False)
    other_specify = models.TextField(null=True,  blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
        
    
    def __str__(self):
        return str(self.id)
    def get_finance_total(self):
        return Finance_Code.objects.filter(travel_request=self).aggregate(Sum('value'))['value__sum']
    def get_cost_total(self):
        return Estimated_Cost.objects.filter(travel_request=self).aggregate(Sum('total_cost'))['total_cost__sum']
    def get_tcost_total(self):
        return Estimated_Cost.objects.filter(Q(travel_request=self)  & ~Q(type=6)).aggregate(Sum('total_cost'))['total_cost__sum']
    def get_tcostp_total(self):
        return Estimated_Cost.objects.filter(Q(travel_request=self)  & Q(type=6)).aggregate(Sum('total_cost'))['total_cost__sum']
    def travel_days(self):
        return  (self.return_date - self.departure_date).days
    def travel_days2(self):
        return  ((self.return_date - self.departure_date).days + 1)
    def pd_days(self):
        return  Estimated_Cost.objects.filter(Q(travel_request=self)  & Q(type=6)).aggregate(Sum('number_unit_day'))['number_unit_day__sum']
    def acc_days(self):
        return  Estimated_Cost.objects.filter(Q(travel_request=self)  & Q(type=3)).aggregate(Sum('number_unit_day'))['number_unit_day__sum']
class Estimated_Cost(models.Model):
  
    travel_request =  models.ForeignKey(
        Travel_Request, on_delete=models.CASCADE, null=True, blank=True)
    type =  models.ForeignKey(Travel_Cost,null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(null=True,  blank=True)
    number_unit_day = models.IntegerField(null=True, blank=True)
    unit_cost = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=2)
    total_cost = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=2)


    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        self.total_cost = self.unit_cost * self.number_unit_day
        super(Estimated_Cost, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)
    class Meta:
        ordering = ('type',)
    
   

class Finance_Code(models.Model):
  
    travel_request =  models.ForeignKey(
        Travel_Request, on_delete=models.CASCADE, null=True, blank=True)
    dept =  models.IntegerField(null=True, blank=True, default=23738)
    fund = models.ForeignKey(Fund,null=True, blank=True, on_delete=models.CASCADE)
    lin_code = models.ForeignKey(Lin_Code,null=True, blank=True, on_delete=models.CASCADE)
    value = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=2)
   


    def __str__(self):
        return str(self.id)
    
class RequestSubmit(models.Model):

    travel_request =  models.OneToOneField(Travel_Request, on_delete=models.CASCADE)
    submission_date = models.DateTimeField(auto_now=True, null=True,   blank=True)
    status = models.ForeignKey(Submission_Status,null=True,  blank=True, on_delete=models.CASCADE)
    submission_note = models.TextField(null=True,  blank=True)
 
    budget_holder = models.ForeignKey(TravelUserRoles, on_delete=models.CASCADE,null=True,  blank=True, related_name='budget_holder')
    finance_reviewer = models.ForeignKey(TravelUserRoles, on_delete=models.CASCADE,null=True,  blank=True, related_name='finance_reviewer')
    security_reviewer = models.ForeignKey(TravelUserRoles, on_delete=models.CASCADE,null=True,  blank=True, related_name='security_reviewer')

   
    class Meta:
        ordering = ('-submission_date',)

    
    def __str__(self):
        return str(self.id)

class SubmitApproval_B(models.Model):
    
    user = models.ForeignKey(TravelUserRoles, on_delete=models.CASCADE)
    submitrequest = models.OneToOneField(RequestSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalf_Status, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    
class SubmitApproval_F(models.Model):
    
    user = models.ForeignKey(TravelUserRoles, on_delete=models.CASCADE)
    submitrequest = models.OneToOneField(RequestSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
    approval_status = models.ForeignKey(Approvalf_Status, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
    
class SubmitApproval_S(models.Model):
    
    user = models.ForeignKey(TravelUserRoles, on_delete=models.CASCADE)
    submitrequest = models.OneToOneField(RequestSubmit, on_delete=models.CASCADE)
    approval_date = models.DateTimeField(auto_now_add=True, null=True,   blank=True)
    approval_note = models.TextField(null=True,  blank=True)
   
    approval_status = models.ForeignKey(Approvalf_Status, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
   
    
   