from django import forms


from django import forms
from .models import Travel_Request, Estimated_Cost, Finance_Code, RequestSubmit, SubmitApproval_B, SubmitApproval_F, SubmitApproval_S
from app_admin.models import Travel_Cost, Fund, Lin_Code, Submission_Status, Approvalf_Status
from django.contrib.auth.models import User
from django_select2 import forms as s2forms
from program.models import TravelUserRoles, Program
from user.models import Profile
from django.db.models import Q



class TravelRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['departure_date'].widget = forms.widgets.DateInput(
          
            attrs={
               'type': 'date',
                'class': 'form-control input-xs'
              
                
                
                }
            )
  
        self.fields['return_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 
                'class': 'form-control input-xs'
                }
            )
        self.fields['destination'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control input-xs', 'rows':'1'  }    )
        self.fields['purpose'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control input-xs', 'rows':'2'  }    )
        self.fields['business'].widget =forms.widgets.CheckboxInput(attrs={'type':'checkbox', 'class': 'form-control-sm icheckbox_flat-green1 '})
    
        #self.fields['business'].widget = forms.widgets.CheckboxInput(attrs={'type':'checkbox', 'class': 'form-control-sm icheckbox_flat-green1 iradio_flat-green1' })
        self.fields['relocation'].widget = forms.widgets.CheckboxInput(attrs={'type':'checkbox', 'class': 'form-control-sm icheckbox_flat-green1 iradio_flat-green1' })
        self.fields['randr'].widget = forms.widgets.CheckboxInput(attrs={'type':'checkbox', 'class': 'form-control-sm icheckbox_flat-green1 iradio_flat-green1' })
        self.fields['other'].widget = forms.widgets.CheckboxInput(attrs={'type':'checkbox', 'class': 'form-control-sm icheckbox_flat-green1 iradio_flat-green1' })
        myfield=['destination',
            'purpose',
            'departure_date',
            'return_date', 
           
            ]
        for field in myfield:
            self.fields[field].required = True 
    class Meta:
        model = Travel_Request
        fields=['destination',
            'purpose',
            'departure_date',
            'return_date', 
            'business',
            'randr',
            'relocation',
            'other',
            ]

        exclude=  ['user']

class TravelCostForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
         trequest = kwargs.pop('trequest', None)
         super(TravelCostForm, self).__init__(*args, **kwargs)
        
         if trequest:
             ty = Estimated_Cost.objects.filter(travel_request_id=trequest.id).values('type')
            

         self.fields['type'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select input-xs',  'data-width': '100%'})
         if self.instance is not None and self.instance.pk is not None:
               self.fields['type'].choices = [
                        (travel_cost.id, travel_cost.name) for travel_cost in Travel_Cost.objects.filter(id=self.instance.type_id)
                    ]
         elif ty:
               self.fields['type'].choices = [
                        (travel_cost.id, travel_cost.name) for travel_cost in Travel_Cost.objects.filter(id__lt=6).exclude(id__in=ty)
                    ]
             
         else:
               self.fields['type'].choices = [
                        (travel_cost.id, travel_cost.name) for travel_cost in Travel_Cost.objects.all().exclude(id = 6)
                    ]
         self.fields['description'].widget = forms.widgets.TextInput(attrs={'type':'text', 'class': 'form-control form-control-sm input-xs' }    )
         self.fields['number_unit_day'].widget = forms.widgets.NumberInput(attrs={'type':'number', 'class': 'form-control form-control-sm input-xs' }    )
         self.fields['unit_cost'].widget = forms.widgets.NumberInput(attrs={'type':'number', 'class': 'form-control form-control-sm input-xs'  }    )
         myfield=['type',
            'description',
            'number_unit_day',
            'unit_cost', 
            
            ]
         for field in myfield:
             self.fields[field].required = True 
    
     class Meta:
         model = Estimated_Cost
         fields=['type',
            'description',
            'number_unit_day',
            'unit_cost', 
            
            ]

         exclude = ['travel_request',]

class TravelCostFormp(forms.ModelForm):
     def __init__(self, *args, **kwargs):
         trequest = kwargs.pop('trequest', None)
         super(TravelCostFormp, self).__init__(*args, **kwargs)
        
         if trequest:
             ty = Estimated_Cost.objects.filter(travel_request_id=trequest.id).values('type')
            

         self.fields['type'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select input-xs',  'data-width': '100%'})
         if self.instance is not None and self.instance.pk is not None:
               self.fields['type'].choices = [
                        (travel_cost.id, travel_cost.name) for travel_cost in Travel_Cost.objects.filter(id=self.instance.type_id)
                    ]
         elif ty:
               self.fields['type'].choices = [
                        (travel_cost.id, travel_cost.name) for travel_cost in Travel_Cost.objects.filter(id=6).exclude(id__in=ty)
                    ]
             
         else:
               self.fields['type'].choices = [
                        (travel_cost.id, travel_cost.name) for travel_cost in Travel_Cost.objects.filter(id=6)
                    ]
         self.fields['description'].widget = forms.widgets.TextInput(attrs={'type':'text', 'class': 'form-control form-control-sm input-xs' }    )
         self.fields['number_unit_day'].widget = forms.widgets.NumberInput(attrs={'type':'number', 'class': 'form-control form-control-sm input-xs' }    )
         self.fields['unit_cost'].widget = forms.widgets.NumberInput(attrs={'type':'number', 'class': 'form-control form-control-sm input-xs'  }    )
         myfield=['type',
            'description',
            'number_unit_day',
            'unit_cost', 
            
            ]
         for field in myfield:
             self.fields[field].required = True 
    
     class Meta:
         model = Estimated_Cost
         fields=['type',
            'description',
            'number_unit_day',
            'unit_cost', 
            
            ]

         exclude = ['travel_request',]

class FinanceCodeForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
 
         self.fields['dept'].widget = forms.widgets.NumberInput(attrs={'type':'number', 'class': 'form-control  input-xs', 'data-width': '100%' }    )
         self.fields['fund'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select input-xs',  'data-width': '100%'})
         self.fields['lin_code'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select input-xs',  'data-width': '100%'})
         self.fields['value'].widget = forms.widgets.NumberInput(attrs={'type':'number', 'class': 'form-control form-control-sm input-xs'}    )
         myfield=['fund',
            'lin_code',
            'value',
            'dept',
          
            
            ]
         self.fields['fund'].queryset = Fund.objects.all()
         self.fields['dept'].initial =  23738
         self.fields['dept'].widget.attrs['readonly'] = True

         self.fields['lin_code'].queryset = Lin_Code.objects.none()
       
         if 'fund' in self.data:
              try:
                  fund = int(self.data.get('fund'))
                  print(fund)
                  self.fields['lin_code'].queryset = Lin_Code.objects.filter(fund_id=fund).order_by('name')
              except (ValueError, TypeError):
                  pass  # invalid input from the client; ignore and fallback to empty City queryset
         elif self.instance.pk:
             self.fields['lin_code'].queryset = self.instance.fund.lin_code_set.order_by('name')
        
         for field in myfield:
             self.fields[field].required = True 
    
     class Meta:
         model = Finance_Code
         fields=['fund','lin_code',   'value',
            'dept',
            ]

         exclude = ['travel_request',]

class RequestSubmitForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
         user = kwargs.pop('user', None)
         sid = kwargs.pop('sid', None)
         super().__init__(*args, **kwargs)

         self.fields['status'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
         self.fields['budget_holder'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
         self.fields['finance_reviewer'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
         self.fields['security_reviewer'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
         self.fields['submission_note'].widget = forms.widgets.Textarea(attrs={'type':'text', 'class': 'form-control form-control-sm', 'rows':'1' }    )
         if user:
             profile = Profile.objects.get(user_id=user.id)
            #program = Program.objects.get(travel_users_role=profile)
             program = Program.objects.filter(travel_users_role=profile, traveluserroles__is_initiator=True)
           
             self.fields['budget_holder'].queryset =  TravelUserRoles.objects.filter(program__in=program, is_budget_holder=True).exclude(profile=profile)
             self.fields['finance_reviewer'].queryset =  TravelUserRoles.objects.filter(program__in=program, is_finance_reviewer=True).exclude(profile=profile)
             self.fields['security_reviewer'].queryset =  TravelUserRoles.objects.filter(program__in=program, is_security_reviewer=True).exclude(profile=profile)
        
         self.fields['status'].choices = [
            (submission_status.id, submission_status.name) for submission_status in Submission_Status.objects.filter(id=sid)
        ]
         self.fields['status'].widget.attrs['readonly'] = True
         myfield = ['status', 'budget_holder','finance_reviewer', 'security_reviewer',]
         for field in myfield:
             self.fields[field].required = True 
     class Meta:
         model = RequestSubmit
         fields=['submission_note','status', 'budget_holder','finance_reviewer', 'security_reviewer',]
        
class RequestCancelForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
         user = kwargs.pop('user', None)
         sid = kwargs.pop('sid', None)
         super().__init__(*args, **kwargs)

         self.fields['status'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
         self.fields['budget_holder'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
         self.fields['finance_reviewer'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
         self.fields['security_reviewer'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
         self.fields['submission_note'].widget = forms.widgets.Textarea(attrs={'type':'text', 'class': 'form-control form-control-sm', 'rows':'1' }    )
         if user:
             profile = Profile.objects.get(user_id=user.id)
            #program = Program.objects.get(travel_users_role=profile)
             program = Program.objects.filter(travel_users_role=profile, traveluserroles__is_initiator=True)
           
             self.fields['budget_holder'].queryset =  TravelUserRoles.objects.filter(program__in=program, is_budget_holder=True).exclude(profile=profile)
             self.fields['finance_reviewer'].queryset =  TravelUserRoles.objects.filter(program__in=program, is_finance_reviewer=True).exclude(profile=profile)
             self.fields['security_reviewer'].queryset =  TravelUserRoles.objects.filter(program__in=program, is_security_reviewer=True).exclude(profile=profile)
        
         self.fields['status'].choices = [
            (submission_status.id, submission_status.name) for submission_status in Submission_Status.objects.filter(id=sid)
        ]
         self.fields['status'].widget.attrs['readonly'] = True
         myfield = ['status', 'budget_holder','finance_reviewer', 'security_reviewer',]
         for field in myfield:
             self.fields[field].required = True 
     class Meta:
         model = RequestSubmit
         fields=['submission_note','status', 'budget_holder','finance_reviewer', 'security_reviewer',]
         exclude = ['travel_request',]


class ApprovalForm_B(forms.ModelForm):
     def __init__(self, *args, **kwargs):
         aid = kwargs.pop('aid', None)
         super().__init__(*args, **kwargs)
         self.fields['approval_status'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
         
         self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'text', 'class': 'form-control form-control-sm', 'rows':'1' }    )
         self.fields['approval_status'].choices = [
            (approval_status.id, approval_status.name) for approval_status in Approvalf_Status.objects.filter(id=aid)
        ]
        
         self.fields['approval_status'].required = True 
         self.fields['approval_note'].required = True 
         self.fields['approval_status'].widget.attrs['readonly'] = True

     class Meta:
         model = SubmitApproval_B
         fields=['approval_note','approval_status']
         exclude = ['user','submitrequest']

class ApprovalForm_F(forms.ModelForm):
     def __init__(self, *args, **kwargs):
         aid = kwargs.pop('aid', None)
         super().__init__(*args, **kwargs)
         self.fields['approval_status'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
         
         self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'text', 'class': 'form-control form-control-sm', 'rows':'1' }    )
         self.fields['approval_status'].choices = [
            (approval_status.id, approval_status.name) for approval_status in Approvalf_Status.objects.filter(id=aid)
        ]
        
         self.fields['approval_status'].required = True 
         self.fields['approval_note'].required = True 
         self.fields['approval_status'].widget.attrs['readonly'] = True

     class Meta:
         model = SubmitApproval_F
         fields=['approval_note','approval_status']
         exclude = ['user','submitrequest']

class ApprovalForm_S(forms.ModelForm):
     def __init__(self, *args, **kwargs):
         aid = kwargs.pop('aid', None)
         super().__init__(*args, **kwargs)
         self.fields['approval_status'].widget =  forms.widgets.Select(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
         
         self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'text', 'class': 'form-control form-control-sm', 'rows':'1' }    )
         self.fields['approval_status'].choices = [
            (approval_status.id, approval_status.name) for approval_status in Approvalf_Status.objects.filter(id=aid)
        ]
        
         self.fields['approval_status'].required = True 
         self.fields['approval_note'].required = True 
         self.fields['approval_status'].widget.attrs['readonly'] = True

     class Meta:
         model = SubmitApproval_S
         fields=['approval_note','approval_status']
         exclude = ['user','submitrequest']