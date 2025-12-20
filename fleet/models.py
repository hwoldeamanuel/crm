from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from app_admin.models import FieldOffice
from user.models import Profile
from datetime import datetime
from django.db.models import Max, Avg,Sum,Count


class Fleet(models.Model):
    field_office = models.ForeignKey(FieldOffice, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='assigned_to')
    tag_number = models.CharField(max_length = 255, null=True, blank=True)
    vehicle_type = models.CharField(max_length = 255, null=True, blank=True)
    chassis_number = models.CharField(max_length = 255, null=True, blank=True)
    year_make = models.CharField(max_length = 255, null=True, blank=True)
    ownership = models.CharField(max_length = 255, null=True, blank=True)
    driver = models.CharField(max_length = 255, null=True, blank=True)
    
    make = models.CharField(max_length = 255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    lin_code =  models.CharField(max_length = 255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,  null=True,  blank=True)
    modified_at = models.DateTimeField(auto_now_add=True,  null=True,  blank=True)
    old_id = models.PositiveIntegerField(null=True, blank=True)
   

    vehicle_pic = models.ImageField(upload_to ='documents/', null=True, blank=True) 

    class Meta:
        unique_together = ('field_office', 'tag_number')
    
    def get_total_kmpl(self):
        total_fuel = Fleet_Expense.objects.filter(expense_type = 'Fuel cost', fleet = self).aggregate(Sum('expense_volume'))['expense_volume__sum']
        total_km   = Fleet_Log.objects.filter(fleet = self).aggregate(Sum('km_driven'))['km_driven__sum']
        if total_fuel is not None and total_km is not None and total_fuel > 0 and total_km > 0:
            return total_km/total_fuel
        else:
            return None
    def get_avail(self):
        day_total =  Log_Report.objects.filter(id = self.id).aggregate(Sum('day_total'))['day_total__sum']
        day_available =  Log_Report.objects.filter(id = self.id).aggregate(Sum('day_available'))['day_available__sum']
        day_use =  Log_Report.objects.filter(id = self.id).aggregate(Sum('day_available'))['day_available__sum']
        if day_total is not None and day_available is not None and day_total > 0 and day_available > 0:
            return (day_available/day_total)*100
        else:
            return None
    def get_usage(self):
      
        day_available =  Log_Report.objects.filter(id = self.id).aggregate(Sum('day_available'))['day_available__sum']
        day_use =  Log_Report.objects.filter(id = self.id).aggregate(Sum('day_use'))['day_use__sum']
       
        if day_use is not None and day_available is not None  and day_available > 0:
          
            return (day_use/day_available)*100
        else:
            return None
    def get_avg_kd(self):
      
        km_driven =  Log_Report.objects.filter(id = self.id).aggregate(Avg('km_driven'))['km_driven__avg']
        
       
        if km_driven is not None:
          
            return km_driven
        else:
            return None

    def __str__(self):
        return str(self.id)




class Fleet_Expense(models.Model):
    fleet = models.ForeignKey(Fleet, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='fleet_expense')
    tag_number = models.CharField(max_length = 255, null=True, blank=True)
    field_office = models.ForeignKey(FieldOffice,on_delete= models.DO_NOTHING, null=True, blank=True)
    month_expense =  models.CharField(max_length = 255, null=True, blank=True)
    year_expense =  models.IntegerField(null=True, blank=True)
    expense_type =  models.CharField( max_length=255, null=True, blank=True)
    expense_volume = models.FloatField(null=True, blank=True)
    expense_value = models.FloatField(null=True, blank=True)
    volume_unit =  models.CharField(max_length = 255, null=True, blank=True)
    expense_start_date = models.DateField(null=True, blank=True)

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        self.expense_start_date = datetime.strptime(self.month_expense + ' 1 ' + str(self.year_expense), '%B %d %Y')
        super(Fleet_Expense, self).save(*args, **kwargs)
   

    def __str__(self):
        return str(self.id)
   
class Generator(models.Model):
    field_office = models.ForeignKey(FieldOffice,on_delete= models.DO_NOTHING, null=True, blank=True)
    title =  models.CharField(max_length = 255, null=True, blank=True)
    make =  models.CharField(max_length = 255, null=True, blank=True)
    hour_liter =  models.FloatField(null=True, blank=True)
    person_in_charge =  models.CharField(max_length = 255, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    old_id =  models.IntegerField(null=True, blank=True)
    generator_pic = models.ImageField(upload_to ='documents/', null=True, blank=True) 

    def __str__(self):
        return str(self.id)

class Generator_Report(models.Model):
    generator= models.ForeignKey(Generator,on_delete= models.DO_NOTHING, null=True, blank=True)
    month_report =  models.CharField(max_length = 255, null=True, blank=True)
    year_report =  models.IntegerField(null=True, blank=True)
    operated_time_hr =  models.FloatField(null=True, blank=True)
    fuel_used_lt = models.FloatField(null=True, blank=True)
    fuel_cost_br = models.FloatField(null=True, blank=True)
    repair_cost_br = models.FloatField(null=True, blank=True)
    report_start_date = models.DateField(null=True, blank=True)
    gen_log_sheet = models.FileField(null=True,  blank=True, upload_to='documents/')

    
    #def save(self,*args, **kwargs):
    #    super().save(*args, **kwargs)
    #    self.report_start_date = datetime.strptime(self.month_report + ' 1 ' + str(self.year_report), '%B %d %Y')
    #   super(Generator_Report, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.id)




class Test(models.Model):
    field_office = models.ForeignKey(FieldOffice, on_delete= models.DO_NOTHING, null=True,  blank=True)
    tag_number = models.CharField(max_length = 255, null=True, blank=True)
    vehicle_type = models.CharField(max_length = 255, null=True, blank=True)
    chassis_number = models.CharField(max_length = 255, null=True, blank=True)
    year_make = models.CharField(max_length = 255, null=True, blank=True)
    ownership = models.CharField(max_length = 255, null=True, blank=True)
    driver = models.CharField(max_length = 255, null=True, blank=True)
    
    make = models.CharField(max_length = 255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    lin_code =  models.CharField(max_length = 255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,  null=True,  blank=True)
    modified_at = models.DateTimeField(auto_now_add=True,  null=True,  blank=True)
   

    vehicle_pic = models.ImageField(upload_to ='documents/', null=True, blank=True) 

    class Meta:
        managed = False
        db_table = 'test'


class Missing_Log(models.Model):
    id = models.IntegerField(primary_key=True)
    field_office = models.ForeignKey(FieldOffice, on_delete= models.DO_NOTHING, null=True,  blank=True)
    tag_number = models.CharField(max_length = 255, null=True, blank=True)
    vehicle_type = models.CharField(max_length = 255, null=True, blank=True)
    ownership = models.CharField(max_length = 255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    generate_series = models.DateField(null=True, blank=True)
    month = models.CharField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    year2 = models.IntegerField(null=True, blank=True)




    class Meta:
        managed = False
        db_table = 'missing_log'


class Missing_Expense(models.Model):
    id = models.IntegerField(primary_key=True)
    field_office = models.ForeignKey(FieldOffice, on_delete= models.DO_NOTHING, null=True,  blank=True)
    tag_number = models.CharField(max_length = 255, null=True, blank=True)
    vehicle_type = models.CharField(max_length = 255, null=True, blank=True)
    ownership = models.CharField(max_length = 255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    generate_series = models.DateField(null=True, blank=True)
    expense_start_date = models.DateField(null=True, blank=True)
    fuel_cost = models.CharField(max_length = 255, null=True, blank=True)
    cost_spares = models.CharField(max_length = 255, null=True, blank=True)
    cost_labour = models.CharField(max_length = 255, null=True, blank=True)
    cost_consumables = models.CharField(max_length = 255, null=True, blank=True)
    rental_and_tax = models.CharField(max_length = 255, null=True, blank=True)
    rental_fees = models.CharField(max_length = 255, null=True, blank=True)
    tax_insurance = models.CharField(max_length = 255, null=True, blank=True)
    month = models.CharField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)



    class Meta:
        managed = False
        db_table = 'missing_expense'



class Missed_Expense(models.Model):
    id = models.IntegerField(primary_key=True)
    field_office = models.ForeignKey(FieldOffice, on_delete= models.DO_NOTHING, null=True,  blank=True)
    tag_number = models.CharField(max_length = 255, null=True, blank=True)
    vehicle_type = models.CharField(max_length = 255, null=True, blank=True)
    ownership = models.CharField(max_length = 255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    generate_series = models.DateField(null=True, blank=True)
    expense_start_date = models.DateField(null=True, blank=True)
    fuel_cost = models.CharField(max_length = 255, null=True, blank=True)
    cost_spares = models.CharField(max_length = 255, null=True, blank=True)
    cost_labour = models.CharField(max_length = 255, null=True, blank=True)
    cost_consumables = models.CharField(max_length = 255, null=True, blank=True)
    rental_and_tax = models.CharField(max_length = 255, null=True, blank=True)
    rental_fees = models.CharField(max_length = 255, null=True, blank=True)
    tax_insurance = models.CharField(max_length = 255, null=True, blank=True)
    month = models.CharField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    fleet_id = models.IntegerField(null=True, blank=True)



    class Meta:
        managed = False
        db_table = 'expenses'


class Log_Report(models.Model):
    id = models.IntegerField(primary_key=True)
    field_office = models.ForeignKey(FieldOffice, on_delete= models.DO_NOTHING, null=True,  blank=True)
    tag_number = models.CharField(max_length = 255, null=True, blank=True)
    vehicle_type = models.CharField(max_length = 255, null=True, blank=True)
    ownership = models.CharField(max_length = 255, null=True, blank=True)
    month_log = models.CharField(max_length = 255, null=True, blank=True)
    year_log = models.IntegerField(null=True, blank=True)
    km_driven = models.FloatField(null=True, blank=True)
    day_use = models.IntegerField(null=True, blank=True)
    day_available = models.IntegerField(null=True, blank=True)
    day_total = models.IntegerField(null=True, blank=True)
    log_start_date = models.DateField(null=True, blank=True)
   


    class Meta:
        managed = False
        db_table = 'log_report'


class Expense_Report(models.Model):
    id = models.IntegerField(primary_key=True)
    field_office = models.ForeignKey(FieldOffice, on_delete= models.DO_NOTHING, null=True,  blank=True)
    tag_number = models.CharField(max_length = 255, null=True, blank=True)
    vehicle_type = models.CharField(max_length = 255, null=True, blank=True)
    ownership = models.CharField(max_length = 255, null=True, blank=True)
    expense_start_date = models.DateField(null=True, blank=True)
    month_expense = models.CharField(max_length = 255, null=True, blank=True)
    year_expense = models.IntegerField(null=True, blank=True)
    total_cost = models.FloatField(null=True, blank=True)
    spare_cost = models.FloatField(null=True, blank=True)
    fuel_cost = models.FloatField(null=True, blank=True)
    consumable_cost = models.FloatField(null=True, blank=True)
    rental_and_tax_cost = models.FloatField(null=True, blank=True)
    labour_cost = models.FloatField(null=True, blank=True)
    rental_cost = models.FloatField(null=True, blank=True)
    tax_cost = models.FloatField(null=True, blank=True)




    class Meta:
        managed = False
        db_table = 'expense_report'




class Fleet_Log(models.Model):
    fleet = models.ForeignKey(Fleet, on_delete= models.DO_NOTHING, null=True,  blank=True, related_name='fleet_assigned')
    tag_number = models.CharField(max_length = 255, null=True, blank=True)
    field_office = models.ForeignKey(FieldOffice,on_delete= models.DO_NOTHING, null=True, blank=True)
    month_log =  models.CharField(max_length = 255, null=True, blank=True)
    year_log =  models.IntegerField(null=True, blank=True)
    start_km = models.FloatField(null=True, blank=True)
    end_km = models.FloatField(null=True, blank=True)
    day_in_use = models.IntegerField(null=True, blank=True)
    day_idle = models.IntegerField(null=True, blank=True)
    day_in_workshop = models.IntegerField(null=True, blank=True)
    workshop_visit = models.IntegerField(null=True, blank=True)
    log_sheet = models.FileField(null=True,  blank=True, upload_to='documents/')
    log_start_date = models.DateField(null=True, blank=True)
    km_driven = models.FloatField(null=True, blank=True)

    
    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        self.log_start_date = datetime.strptime(self.month_log + ' 1 ' + str(self.year_log), '%B %d %Y')
        self.km_driven = self.end_km - self.start_km
        super(Fleet_Log, self).save(*args, **kwargs)
    
    def __str__(self):
        return str(self.id)
