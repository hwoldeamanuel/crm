from django import forms

from program.models import Indicator, UserRoles
from partnership.models import Partnership
from django import forms
from .models import Program, ImplementationArea, UserRoles, TravelUserRoles
from django.contrib.auth.models import User
from user.models import Profile
from django_select2 import forms as s2forms


from app_admin.models import Country as Country, Region, Zone, Woreda
from portfolio.models import Portfolio






class AddProgramForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'placeholder':'description'   }    )

    class Meta:
        model = Program
        fields=['title',
            'fund_code',
            'description',
            'start_date', 
            'end_date',
            'donor',
            'working_title',
            ]

        exclude=  ['users_role']

class EditProgramForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'placeholder':'description'   }    )
        

    class Meta:
        model = Program
        fields=['title',
            'fund_code',
            'description',
            'start_date', 
            'end_date',
            'donor',
            ]

        exclude=  ['users_role']

      

class AddProgramAreaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        program = kwargs.pop('program', None)
        super(AddProgramAreaForm, self).__init__(*args, **kwargs)
        
        if program:
            program = program.pk
            self.fields['program'].queryset = Program.objects.filter(id=program)
            self.fields['program'].initial = Program.objects.filter(id=program).first()
        
        self.fields['region'].queryset = Region.objects.all()
       

        self.fields['zone'].queryset = Zone.objects.none()
        self.fields['woreda'].queryset = Woreda.objects.none()
        if 'region' in self.data:
            try:
                region = int(self.data.get('region'))
                self.fields['zone'].queryset = Zone.objects.filter(region_id=region).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['zone'].queryset = self.instance.region.zone_set.order_by('name')

        self.fields['woreda'].queryset = Woreda.objects.none()
        if 'zone' in self.data:
            try:
                zone = int(self.data.get('zone'))
                self.fields['woreda'].queryset = Woreda.objects.filter(zone_id=zone).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['woreda'].queryset = self.instance.zone.woreda_set.order_by('name')
        
        self.fields['program'].disabled = True
        
        



        myfield = ['region',
            'zone','woreda',    
            'program',     

            ]
        for field in myfield:
            self.fields[field].required = True 

    
    class Meta:
            model = ImplementationArea
            fields=['region',
            'zone',
            'woreda',
            'program',
            ]
    def clean(self):
        cleaned_data = super().clean()
        program = self.cleaned_data.get('program')
        woreda = self.cleaned_data.get('woreda')

        if ImplementationArea.objects.filter(program=program, woreda=woreda).exists():
            self._errors['woreda'] = self.error_class(['Already Exist'])
        return cleaned_data       

class EditProgramAreaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        program = kwargs.pop('program', None)
        super(EditProgramAreaForm, self).__init__(*args, **kwargs)
        
        if program:
            program = program.pk
            self.fields['program'].queryset = Program.objects.filter(id=program)
            self.fields['program'].initial = Program.objects.filter(id=program).first()
        
        self.fields['region'].queryset = Region.objects.all()
       

        self.fields['zone'].queryset = Zone.objects.none()
        self.fields['woreda'].queryset = Woreda.objects.none()
        if 'region' in self.data:
            try:
                region = int(self.data.get('region'))
                self.fields['zone'].queryset = Zone.objects.filter(region_id=region).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['zone'].queryset = self.instance.region.zone_set.order_by('name')

        self.fields['woreda'].queryset = Woreda.objects.none()
        if 'zone' in self.data:
            try:
                zone = int(self.data.get('zone'))
                self.fields['woreda'].queryset = Woreda.objects.filter(zone_id=zone).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['woreda'].queryset = self.instance.zone.woreda_set.order_by('name')
        
        self.fields['program'].disabled = True
        
        



        myfield = ['region',
            'zone','woreda',    
            'program',     

            ]
        for field in myfield:
            self.fields[field].required = True 

    
    class Meta:
            model = ImplementationArea
            fields=['region',
            'zone',
            'woreda',
            'program',
            ]
    def clean(self):
        cleaned_data = super().clean()
        program = self.cleaned_data.get('program')
        woreda = self.cleaned_data.get('woreda')

        if ImplementationArea.objects.filter(program=program, woreda=woreda).count() > 1:
            self._errors['woreda'] = self.error_class(['Already Exist'])
        return cleaned_data  
    
class NewAreaForm(forms.ModelForm):
     
     class Meta:
        model = ImplementationArea
        fields=['region',
            'zone',
            'woreda',
            ]
        exclude=  ['program']
        


class BaseAutocompleteSelect(s2forms.ModelSelect2Widget):
    class Media:
        js = ("admin/js/vendor/jquery/jquery.min.js",)

    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.attrs = {"style": "width: 300px"}

    def build_attrs(self, base_attrs, extra_attrs=None):
        base_attrs = super().build_attrs(base_attrs, extra_attrs)
        base_attrs.update(
            {"data-minimum-input-length": 0, "data-placeholder": self.empty_label}
        )
        return base_attrs

class CoAuthorsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "users__icontains"
       
    ]

    


      

class ProgramForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
        myfield = ['title',
            'fund_code',
            'description',
            'start_date', 
            'end_date',
            'donor',
            'working_title',
            'portfolio',
    

            ]
        for field in myfield:
            self.fields[field].required = True 

        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'placeholder':'description'   }    )    
        self.fields['portfolio'].queryset = Portfolio.objects.filter(id=1)
        self.fields['portfolio'].initial = Portfolio.objects.filter(id=1).first()
        
            
    class Meta:
        model = Program
        fields=['title',
            'fund_code',
            'description',
            'start_date', 
            'end_date',
            'donor',
            'working_title',
            'portfolio',
            ]

        exclude=  ['users_role']
       
           
    
class IndicatorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
     
        self.fields['indicator_no'].required = True 
        self.fields['indicator_title'].required = True 
        self.fields['indicator_level'].required = True 
        self.fields['indicator_unit'].required = True 
        
        self.fields['indicator_target_LoP'].required = True 
     
    class Meta:
        model = Indicator
        fields=['indicator_no',
            'indicator_title',
            'indicator_level',
            'indicator_unit',
            'indicator_baseline',
            'indicator_target_LoP'
            ]
        exclude=  ['program']

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        
       
       
     
    
    class Meta:
        model = Program
        fields=['users_role', 
           
            ]
        exclude= ['title',
            'fund_code',
            'description',
            'start_date', 
            'end_date',
            'donor',]

class UserRoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        program = kwargs.pop('program', None)
        super().__init__(*args, **kwargs)
        
        if program:
            
            self.fields['user'].queryset = User.objects.filter(is_active=True).exclude(program=program)
        else:
           
            self.fields['user'].queryset = User.objects.filter(is_active=True)
        
        self.fields['user'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})

    class Meta:
        model = UserRoles
        fields=['user','is_pcn_initiator', 'is_pcn_mel_approver','is_pcn_technical_approver', 'is_pcn_program_approver','is_pcn_finance_approver',
                'is_pacn_initiator', 'is_pacn_mel_approver','is_pacn_technical_approver', 'is_pacn_program_approver','is_pacn_finance_approver'
                ]

class UserRoleFormE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            id = user.pk
            self.fields['user'].queryset = User.objects.filter(id=id)
            self.fields['user'].initial = User.objects.filter(id=id).first()
        
       
        self.fields['user'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
        
            
    class Meta:
        model = UserRoles
        fields=['user','is_pcn_initiator', 'is_pcn_mel_approver','is_pcn_technical_approver', 'is_pcn_program_approver','is_pcn_finance_approver',
                'is_pacn_initiator', 'is_pacn_mel_approver','is_pacn_technical_approver', 'is_pacn_program_approver','is_pacn_finance_approver'
                ]
        readonly_fields = ('user',)

class UserRoleFormP(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            id = user.pk
            self.fields['user'].queryset = User.objects.filter(id=id)
            self.fields['user'].initial = User.objects.filter(id=id).first()
        
       
        self.fields['user'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
        self.fields['approval_budget_min_usd'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
        self.fields['approval_budget_max_usd'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
            
    class Meta:
        model = UserRoles
        fields=['user','is_pcn_initiator', 'is_pcn_mel_approver','is_pcn_technical_approver', 'is_pcn_program_approver','is_pcn_finance_approver',
                'is_pacn_initiator', 'is_pacn_mel_approver','is_pacn_technical_approver', 'is_pacn_program_approver','is_pacn_finance_approver'
                ,'approval_budget_min_usd', 'approval_budget_max_usd'
                ]
        readonly_fields = ('user',)


class TravelUserRoleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        program = kwargs.pop('program', None)
        super().__init__(*args, **kwargs)
        
        if program:
            
            self.fields['profile'].queryset = Profile.objects.filter(user__is_active=True).exclude(program=program)
        else:
           
            self.fields['profile'].queryset = Profile.objects.filter(user__is_active=True)
        
        self.fields['profile'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})

    class Meta:
        model = TravelUserRoles
        fields=['profile','is_initiator', 'is_budget_holder','is_finance_reviewer', 'is_security_reviewer']

class TravelUserRoleFormE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        profile = kwargs.pop('profile', None)
        super().__init__(*args, **kwargs)
        
        if profile:
            
            self.fields['profile'].queryset = Profile.objects.filter(user_id=profile.user_id)
            self.fields['profile'].initial = Profile.objects.filter(user_id=profile.user_id).first()
        
       
        self.fields['profile'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
        
    class Meta:
        model = TravelUserRoles
        fields=['profile','is_initiator', 'is_budget_holder','is_finance_reviewer', 'is_security_reviewer',]
        exclude= ['program',]


class ParnershipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
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
     
        self.fields['portfolio'].required = True 
        self.fields['partership_type'].required = True 
        self.fields['agreement_type'].required = True 
        self.fields['total_budget'].required = True 
        self.fields['subAwar_code'].required = True 
        self.fields['start_date'].required = True 
        self.fields['end_date'].required = True 
        self.fields['partership_type'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'1', 'required':'True'   }    )
        self.fields['agreement_type'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'1', 'required':'True'   }    )
        self.fields['subAwar_code'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'1', 'required':'True'   }    )
    class Meta:
        model = Partnership
        fields=['portfolio',
            'partership_type',
            'agreement_type',
            'total_budget',
            'subAwar_code',         
            'start_date',
            'end_date'
            ]
        exclude=  ['program']