from django import forms
from fleet.models import Fleet, Fleet_Log, Fleet_Expense, Generator_Report, Generator
import datetime 
from dateutil.relativedelta import relativedelta
from datetime import datetime
import pandas as pd
from django.shortcuts import get_object_or_404

class FleetForm(forms.ModelForm):
      def __init__(self, *args, **kwargs):
           super(FleetForm, self).__init__(*args, **kwargs)
           self.fields['start_date'].widget = forms.widgets.DateInput(
          
            attrs={
               'type': 'date',
                'class': 'form-control'
              
                
                
                }
            )
           self.fields['end_date'].widget = forms.widgets.DateInput(
          
            attrs={
               'type': 'date',
                'class': 'form-control'
              
                
                
                }
            )
        
           CHOICES1 =   (
            ('',''),
            ('Vehicle', 'Vehicle'),
            ('MotorCycle', 'MotorCycle'),
     
             )
         
           CHOICES2 =   (
        ('',''),
        ('Mercy Corps', 'Mercy Corps'),
        ('Rental', 'Rental'),
     
        )
       
        
        

       
           self.fields['vehicle_type'].widget = forms.widgets.Select(choices=CHOICES1)
           self.fields['ownership'].widget = forms.widgets.Select(choices=CHOICES2)
           self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'placeholder':'description'   }    )    
           myfield = ['tag_number',
            'field_office','vehicle_type',    
            'ownership',  
              'start_date',    
              'end_date',

            ]
           for field in myfield:
                 self.fields[field].required = True 
      class Meta:
           model = Fleet
           fields = ['tag_number','field_office','vehicle_type','ownership', 'start_date','end_date','lin_code','vehicle_pic','chassis_number','description','make','year_make', 'driver']
         

class FleetLogForm(forms.ModelForm):
      
      def __init__(self, *args, **kwargs):
            fleet = kwargs.pop('fleet', None)
            super(FleetLogForm, self).__init__(*args, **kwargs)

            CHOICES1 =   (
            ('',''),
            ('January', 'January'),
            ('February', 'February'),
            ('March', 'March'),
            ('April', 'April'),
            ('May', 'May'),
            ('June', 'June'),
            ('July', 'July'),
            ('August', 'August'),
            ('September', 'September'),
            ('October', 'October'),
        
            ('November', 'November'),
        
            ('December', 'December'),
        
            )


            CHOICES2 =   (
            ('',''),
            (2023, 2023),
            (2024, 2024),
            (2025, 2025),
               (2026, 2026),
            (2027, 2027),
         
            
            )

            self.fields['month_log'].widget = forms.widgets.Select(choices=CHOICES1)
            self.fields['year_log'].widget = forms.widgets.Select(choices=CHOICES2)
           
             
             
            self.fields['fleet'].choices = [
                        (fleet.id, fleet.id) for fleet in Fleet.objects.filter(id=fleet)
                    ]
            self.fields['fleet'].widget.attrs['readonly'] = True
            self.fields['month_log'].required = True 
            self.fields['year_log'].required = True 
            self.fields['start_km'].required = True 
            self.fields['end_km'].required = True 
            self.fields['day_in_use'].required = True 
            self.fields['day_idle'].required = True 
            self.fields['day_in_workshop'].required = True 
            self.fields['workshop_visit'].required = True 

        
      class Meta:
            model = Fleet_Log
            fields = ['fleet','month_log','year_log','start_km','end_km','day_in_use','day_idle','day_in_workshop','workshop_visit','log_sheet']

      def clean(self):
           cleaned_data = super().clean()
           month = self.cleaned_data.get('month_log')
           year = self.cleaned_data.get('year_log')
           fleet = self.cleaned_data.get('fleet')
           day1 = self.cleaned_data.get('day_in_use')
           day2 = self.cleaned_data.get('day_idle')
           day3 = self.cleaned_data.get('day_in_workshop')
           day4 = self.cleaned_data.get('workshop_visit')
           end_km = self.cleaned_data.get('end_km')
           total_days = day1 + day2 + day3 + day4

           start_km = self.cleaned_data.get('start_km')
           start_date = datetime.strptime(month + ' 1 ' + str(year), '%B %d %Y')
           last_month_date =  start_date- relativedelta(months=1)
           if Fleet_Log.objects.filter(fleet=fleet, log_start_date=last_month_date).exists():
                 last_log = Fleet_Log.objects.get(fleet=fleet, log_start_date=last_month_date)
                 prev_end_km = last_log.end_km
           else:
                 prev_end_km = start_km
            
           numdays = (start_date + pd.DateOffset(months=1) - pd.DateOffset(days=1)).day
          

           if Fleet_Log.objects.filter(fleet=fleet, log_start_date=start_date).exists():
                 self._errors['month_log'] = self.error_class(['Log Already Exists'])
           elif (start_km != prev_end_km):
                 self._errors['start_km'] = self.error_class(['Start Km not match Prior End KM'])
           elif (total_days != numdays):
                 self._errors['day_in_use'] = self.error_class(['Check number of days'])
           elif (end_km < start_km):
                 self._errors['end_km'] = self.error_class(['Check start end km'])
            
           elif (start_date > datetime.today()):
                 self._errors['month_log'] = self.error_class(['Not valid date'])
           return cleaned_data

class FleetLogFormEdit(forms.ModelForm):
      def __init__(self, *args, **kwargs):
            fleet = kwargs.pop('fleet', None)
            super(FleetLogFormEdit, self).__init__(*args, **kwargs)

            CHOICES1 =   (
            ('',''),
            ('January', 'January'),
            ('February', 'February'),
            ('March', 'March'),
            ('April', 'April'),
            ('May', 'May'),
            ('June', 'June'),
            ('July', 'July'),
            ('August', 'August'),
            ('September', 'September'),
            ('October', 'October'),
        
            ('November', 'November'),
        
            ('December', 'December'),
        
            )


            CHOICES2 =   (
            ('',''),
            (2023, 2023),
            (2024, 2024),
            (2025, 2025),
               (2026, 2026),
            (2027, 2027),
         
            
            )

            self.fields['month_log'].widget = forms.widgets.Select(choices=CHOICES1)
            self.fields['year_log'].widget = forms.widgets.Select(choices=CHOICES2)
           
             
             
            self.fields['fleet'].choices = [
                        (fleet.id, fleet.id) for fleet in Fleet.objects.filter(id=fleet)
                    ]
            self.fields['fleet'].widget.attrs['readonly'] = True
            self.fields['fleet'].required = True 
            self.fields['month_log'].required = True 
            self.fields['year_log'].required = True 
            self.fields['start_km'].required = True 
            self.fields['end_km'].required = True 
            self.fields['day_in_use'].required = True 
            self.fields['day_idle'].required = True 
            self.fields['day_in_workshop'].required = True 
            self.fields['workshop_visit'].required = True 

        
      class Meta:
            model = Fleet_Log
            fields = ['fleet','month_log','year_log','start_km','end_km','day_in_use','day_idle','day_in_workshop','workshop_visit','log_sheet']

      def clean(self):
           cleaned_data = super().clean()
           month = self.cleaned_data.get('month_log')
           year = self.cleaned_data.get('year_log')
           fleet = self.cleaned_data.get('fleet')
           end_km = self.cleaned_data.get('end_km')
           day1 = self.cleaned_data.get('day_in_use')
           day2 = self.cleaned_data.get('day_idle')
           day3 = self.cleaned_data.get('day_in_workshop')
           day4 = self.cleaned_data.get('workshop_visit')
           total_days = day1 + day2 + day3 + day4

           start_km = self.cleaned_data.get('start_km')
           start_date = datetime.strptime(month + ' 1 ' + str(year), '%B %d %Y')
           last_month_date =  start_date- relativedelta(months=1)
           if Fleet_Log.objects.filter(fleet=fleet, log_start_date=last_month_date).exists():
                 last_log = Fleet_Log.objects.get(fleet=fleet, log_start_date=last_month_date)
                 prev_end_km = last_log.end_km
           else:
                 prev_end_km = start_km
            
           numdays = (start_date + pd.DateOffset(months=1) - pd.DateOffset(days=1)).day
          

         
           if (start_km != prev_end_km):
                 self._errors['start_km'] = self.error_class(['Start Km not match Prior End KM'])
           elif (total_days != numdays):
                 self._errors['day_in_use'] = self.error_class(['Check number of days'])
           elif (end_km < start_km):
                 self._errors['end_km'] = self.error_class(['Check start end km'])
           elif (start_date > datetime.today()):
                 self._errors['month_log'] = self.error_class(['Not valid date'])
        
           return cleaned_data
      

class FleetExpenseFormEdit(forms.ModelForm):
      def __init__(self, *args, **kwargs):
            fleet = kwargs.pop('fleet', None)
            super(FleetExpenseFormEdit, self).__init__(*args, **kwargs)

            self.fields['fleet'].choices = [
                        (fleet.id, fleet.id) for fleet in Fleet.objects.filter(id=fleet)
                    ]
            self.fields['fleet'].widget.attrs['readonly'] = True
            CHOICES1 =   (
             ('',''),
            ('January', 'January'),
            ('February', 'February'),
            ('March', 'March'),
            ('April', 'April'),
            ('May', 'May'),
            ('June', 'June'),
            ('July', 'July'),
            ('August', 'August'),
            ('September', 'September'),
            ('October', 'October'),
        
            ('November', 'November'),
        
            ('December', 'December'),
        
            )


            CHOICES2 =   (
            ('',''),
            (2023, 2023),
            (2024, 2024),
            (2025, 2025),
               (2026, 2026),
            (2027, 2027),
         
            
            )
            CHOICES3 =   (
            ('',''),
            ('Costs of consumables','Costs of consumables'),
            ('Fuel cost', 'Fuel cost'),
            ('Rental fees, Tax, insurance, miscs','Rental fees, Tax, insurance, miscs'),
            ('Cost of labour', 'Cost of labour'),
            ('Cost of Spares' , 'Cost of Spares'),
            ('Rental fees','Rental fees'),
            ('Tax, Insurance, miscs', 'Tax, Insurance, miscs')
            )
            CHOICES4 =   (
            ('',''),
            ('Kg','Kg'),
            
            ('gal', 'gal'),
       
            ('Litre', 'Litre'),
            ('Pcs','Pcs'),
            ('Other' , 'Other'),
            
            )





            self.fields['month_expense'].widget = forms.widgets.Select(choices=CHOICES1)
            self.fields['year_expense'].widget = forms.widgets.Select(choices=CHOICES2)
            self.fields['expense_type'].widget = forms.widgets.Select(choices=CHOICES3)
            self.fields['volume_unit'].widget = forms.widgets.Select(choices=CHOICES4)
            self.fields['fleet'].required = True 
            self.fields['month_expense'].required = True 
            self.fields['year_expense'].required = True 
            self.fields['expense_type'].required = True 
            self.fields['expense_volume'].required = True 
            self.fields['expense_value'].required = True 
            self.fields['volume_unit'].required = True 

      class Meta:
            model = Fleet_Expense
            fields = ['fleet','month_expense','year_expense','expense_type','expense_volume','volume_unit', 'expense_value']
      def clean(self):
           cleaned_data = super().clean()
           month = self.cleaned_data.get('month_expense')
           year = self.cleaned_data.get('year_expense')
           

           
           start_date = datetime.strptime(month + ' 1 ' + str(year), '%B %d %Y')
           
          
           if (start_date > datetime.today()):
                 self._errors['month_expense'] = self.error_class(['Not valid date'])
        
           return cleaned_data
      

class FleetExpenseForm(forms.ModelForm):
      def __init__(self, *args, **kwargs):
            fleet = kwargs.pop('fleet', None)
            super(FleetExpenseForm, self).__init__(*args, **kwargs)

            self.fields['fleet'].choices = [
                        (fleet.id, fleet.id) for fleet in Fleet.objects.filter(id=fleet)
                    ]
            self.fields['fleet'].widget.attrs['readonly'] = True
         
          
            CHOICES3 =   (
                        ('',''),
                        ('Costs of consumables','Costs of consumables'),
                        ('Fuel cost', 'Fuel cost'),
            
                        ('Cost of labour', 'Cost of labour'),
                        ('Cost of Spares' , 'Cost of Spares'),
                        ('Rental fees','Rental fees'),
                        ('Tax, Insurance, miscs', 'Tax, Insurance, miscs')
                         )
            CHOICES1 =   (
            ('',''),
            ('January', 'January'),
            ('February', 'February'),
            ('March', 'March'),
            ('April', 'April'),
            ('May', 'May'),
            ('June', 'June'),
            ('July', 'July'),
            ('August', 'August'),
            ('September', 'September'),
            ('October', 'October'),
        
            ('November', 'November'),
        
            ('December', 'December'),
        
            )


            CHOICES2 =   (
            ('',''),
            (2023, 2023),
            (2024, 2024),
            (2025, 2025),
               (2026, 2026),
            (2027, 2027),
         
            
            )
       
            CHOICES4 =   (
            ('',''),
            ('Kg','Kg'),
            
            ('gal', 'gal'),
       
            ('Litre', 'Litre'),
            ('Pcs','Pcs'),
            ('Other' , 'Other'),
            
            )

            self.fields['month_expense'].widget = forms.widgets.Select(choices=CHOICES1)
            self.fields['year_expense'].widget = forms.widgets.Select(choices=CHOICES2)
            self.fields['expense_type'].widget = forms.widgets.Select(choices=CHOICES3)
            self.fields['volume_unit'].widget = forms.widgets.Select(choices=CHOICES4)
            self.fields['fleet'].required = True 
            self.fields['month_expense'].required = True 
            self.fields['year_expense'].required = True 
            self.fields['expense_type'].required = True 
            self.fields['expense_volume'].required = True 
            self.fields['expense_value'].required = True 
            self.fields['volume_unit'].required = True 

      class Meta:
            model = Fleet_Expense
            fields = ['fleet','month_expense','year_expense','expense_type','expense_volume','volume_unit', 'expense_value']
     
      def clean(self):
            cleaned_data = super().clean()
            month = self.cleaned_data.get('month_expense')
            year = self.cleaned_data.get('year_expense')
            fleet = self.cleaned_data.get('fleet')
            expense_type = self.cleaned_data.get('expense_type')
           
        
            start_date = datetime.strptime(month + ' 1 ' + str(year), '%B %d %Y')
           
          
            if (start_date > datetime.today()):
                  self._errors['month_expense'] = self.error_class(['Not valid date'])

            elif Fleet_Expense.objects.filter(fleet=fleet, month_expense=month, year_expense=year, expense_type=expense_type).exists():
                  self._errors['month_expense'] = self.error_class(['Expense Already Exists'])
           
            return cleaned_data
      

class GeneratorForm(forms.ModelForm):
      def __init__(self, *args, **kwargs):
            super(GeneratorForm, self).__init__(*args, **kwargs)
           

            self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'placeholder':'description'   }    )    
            my_fields =   ['title','make','hour_liter','person_in_charge', 'field_office']
            for field in my_fields:
                  self.fields[field].required = True 
      class Meta:
           model = Generator
           fields = ['title','make','hour_liter','person_in_charge', 'field_office','description']


class GeneratorReportForm(forms.ModelForm):
      def __init__(self, *args, **kwargs):
            generator = kwargs.pop('generator', None)
            super(GeneratorReportForm, self).__init__(*args, **kwargs)
           
            self.fields['generator'].choices = [
                        (generator.id, generator.id) for generator in Generator.objects.filter(id=generator)
                    ]
            self.fields['generator'].widget.attrs['readonly'] = True
            CHOICES1 =   (
            ('',''),
            ('January', 'January'),
            ('February', 'February'),
            ('March', 'March'),
            ('April', 'April'),
            ('May', 'May'),
            ('June', 'June'),
            ('July', 'July'),
            ('August', 'August'),
            ('September', 'September'),
            ('October', 'October'),
        
            ('November', 'November'),
        
            ('December', 'December'),
        
            )


            CHOICES2 =   (
            ('',''),
            (2023, 2023),
            (2024, 2024),
            (2025, 2025),
               (2026, 2026),
            (2027, 2027),
         
            
            )
            self.fields['month_report'].widget = forms.widgets.Select(choices=CHOICES1)
            self.fields['year_report'].widget = forms.widgets.Select(choices=CHOICES2)
            my_fields =   ['generator','month_report', 'year_report','operated_time_hr', 'fuel_used_lt','fuel_cost_br','repair_cost_br']
            for field in my_fields:
                  self.fields[field].required = True 
      class Meta:
            model = Generator_Report
            fields = ['generator','month_report', 'year_report','operated_time_hr', 'fuel_used_lt','fuel_cost_br','repair_cost_br','gen_log_sheet']
      
      def clean(self):
            cleaned_data = super().clean()
            month = self.cleaned_data.get('month_report')
            year = self.cleaned_data.get('year_report')
            generator = self.cleaned_data.get('generator')
                     
        
          

            if Generator_Report.objects.filter(generator=generator, month_report=month, year_report=year).exists():
                 self._errors['month_report'] = self.error_class(['Report already Exists'])
           
        
            return cleaned_data
      
class GeneratorReportFormEdit(forms.ModelForm):
      def __init__(self, *args, **kwargs):
            generator = kwargs.pop('generator', None)
            super(GeneratorReportFormEdit, self).__init__(*args, **kwargs)
           
            self.fields['generator'].choices = [
                        (generator.id, generator.id) for generator in Generator.objects.filter(id=generator)
                    ]
            self.fields['generator'].widget.attrs['readonly'] = True
            CHOICES1 =   (
            ('',''),
            ('January', 'January'),
            ('February', 'February'),
            ('March', 'March'),
            ('April', 'April'),
            ('May', 'May'),
            ('June', 'June'),
            ('July', 'July'),
            ('August', 'August'),
            ('September', 'September'),
            ('October', 'October'),
        
            ('November', 'November'),
        
            ('December', 'December'),
        
            )


            CHOICES2 =   (
            ('',''),
            (2023, 2023),
            (2024, 2024),
            (2025, 2025),
            (2026, 2026),
            (2027, 2027),
            
            )
            self.fields['month_report'].widget = forms.widgets.Select(choices=CHOICES1)
            self.fields['year_report'].widget = forms.widgets.Select(choices=CHOICES2)
            my_fields =   ['generator','month_report', 'year_report','operated_time_hr', 'fuel_used_lt','fuel_cost_br','repair_cost_br']
            for field in my_fields:
                  self.fields[field].required = True 
      class Meta:
            model = Generator_Report
            fields = ['generator','month_report','gen_log_sheet', 'year_report','operated_time_hr', 'fuel_used_lt','fuel_cost_br','repair_cost_br']


#(icn.pk, icn) for icn in Icn.objects.filter(id=icn.id)
CHOICES1 =   (
           
            ('January', 'January'),
            ('February', 'February'),
            ('March', 'March'),
            ('April', 'April'),
            ('May', 'May'),
            ('June', 'June'),
            ('July', 'July'),
            ('August', 'August'),
            ('September', 'September'),
            ('October', 'October'),
        
            ('November', 'November'),
        
            ('December', 'December')
        
            )


CHOICES2 =   (
           
            (2023, 2023),
            (2024, 2024),
            (2025, 2025),
            (2026, 2026),
            (2027, 2027),
         
            )

class MissingLogForm(forms.Form):
      field_office = forms.ChoiceField( required=False)
      month = forms.ChoiceField()
      year = forms.ChoiceField()

      def __init__(self, *args, **kwargs):
            super(MissingLogForm, self).__init__(*args, **kwargs)
            self.fields['month'].required = True 
            self.fields['year'].required = True 

