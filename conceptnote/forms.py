from django import forms
from django.core.exceptions import ValidationError
from .models import Icn, Activity,Impact,ActivityImpact, IcnImplementationArea,  ActivityImplementationArea,IcnSubmit, Document, IcnSubmitApproval_F, IcnSubmitApproval_T, IcnSubmitApproval_P, IcnSubmitApproval_M, ActivityDocument, ActivitySubmit,ActivitySubmitApproval_F,ActivitySubmitApproval_P,ActivitySubmitApproval_T, ActivitySubmitApproval_M
from django import forms

from program.models import  Program, ImplementationArea, Indicator, UserRoles
from portfolio.models import Portfolio
from datetime import datetime
from django.forms.models import modelformset_factory
from django_select2 import forms as s2forms
from app_admin.models import Country , Region , Zone , Woreda , Approvalt_Status, Approvalf_Status, Submission_Status
from django.contrib.auth.models import User
from portfolio.models import Portfolio
from django.forms import inlineformset_factory
from django.db.models import Max
from django.shortcuts import get_object_or_404
from django.db.models import Q






CHOICE1 =(
    ("1", "Low"),
    ("2", "Medium"),
    ("3", "High"),
    
)
CHOICE2 =(
    ("0", "No"),
    ("1", "Yes"),
  
    
)
class IcnForm(forms.ModelForm):
           
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(IcnForm, self).__init__(*args, **kwargs)
               
        
       
      
        if user:
            self.fields['program'].queryset = Program.objects.filter(users_role=user, userroles__is_pcn_initiator=True)
            self.fields['program'].initial=Program.objects.filter(users_role=user, userroles__is_pcn_initiator=True).first()
            program = Program.objects.filter(users_role=user, userroles__is_pcn_initiator=True)
            self.fields['mel_lead'].queryset =  UserRoles.objects.filter(program__in=program, is_pcn_mel_approver=True).exclude(user=user)
            self.fields['mel_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_mel_approver=True).exclude(user=user).first()
            self.fields['technical_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pcn_technical_approver=True).exclude(user=user)
            self.fields['technical_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_technical_approver=True).exclude(user=user).first()
            self.fields['finance_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pcn_finance_approver=True).exclude(user=user)
            self.fields['finance_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_finance_approver=True).exclude(user=user).first()
            self.fields['program_lead'].queryset =  UserRoles.objects.filter(program__in=program, is_pcn_program_approver=True, approval_budget_min_usd__isnull=False, approval_budget_max_usd__isnull=False).exclude(user=user)
            self.fields['program_lead'].initial=UserRoles.objects.filter(program__in=program, is_pcn_program_approver=True, approval_budget_min_usd__isnull=False, approval_budget_max_usd__isnull=False).exclude(user=user).first()
            self.fields['ilead_agency'].queryset = Portfolio.objects.filter(id=user.profile.portfolio_id).order_by('id')
            self.fields['ilead_agency'].initial = Portfolio.objects.filter(id=user.profile.portfolio_id).first()
            self.fields['ilead_co_agency'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
            self.fields['ilead_co_agency'].queryset = Portfolio.objects.exclude(Q(id=user.profile.portfolio_id)).order_by('id')

        myfield = ['title',
            'program',
            'description',
            'proposed_start_date', 
            'proposed_end_date',
            'ilead_agency',
            'final_report_due_date',
            'program_lead',
            'technical_lead',
            'finance_lead',
            'mel_lead',
            'iworeda',
            'mc_budget',
           
            'cost_sharing_budget',
            
            'eniromental_impact',
            
            
           
          


           
            

            ]
        for field in myfield:
            self.fields[field].required = True 

        
        self.fields['iworeda'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
        pia = ImplementationArea.objects.filter(program__in=program).values_list('region').distinct()
        all_woreda = Region.objects.filter(id__in=pia)
        self.fields['iworeda'].choices = [
             
             
             (name, [(ia.id, ia) for ia in ImplementationArea.objects.filter(region=name, program__in=program)])
                        for name in all_woreda
                
            ]
       
       
        self.fields['proposed_start_date'].widget = forms.widgets.DateInput(
          
            attrs={
               'type': 'date', 'placeholder': 'yyyy-mm-dd',
                'class': 'form-control',
                'required': 'true'
                
                
                }
            )
    
  
        self.fields['proposed_end_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['final_report_due_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-contro-sm', 'rows':'3', 'required':'required'  }    )
        self.fields['eniromental_impact'].widget = forms.widgets.Select(choices = CHOICE1,attrs={'type': 'choice', 'class': 'form-control form-control-sm', 'rows':'1', 'placeholder':''   }    )
        
        

       
       
       
        
    class Meta:
        model = Icn
        fields=['title',
            'program',
            'description',
            'proposed_start_date', 
            'proposed_end_date',
            'mc_currency',
            'cs_currency',
            'final_report_due_date',
            'program_lead',
            'mel_lead',
            'technical_lead',
            'finance_lead',
            'iworeda',
            'mc_budget',
            
            'cost_sharing_budget',
            
            'eniromental_impact',
            'environmental_assessment_att',
            'ilead_agency',
            'ilead_co_agency',
            
           
           
          


           
            

            ]

        exclude=  ['status', 'approval_status',  'user',]
        
    def clean(self):
         cleaned_data = super().clean()
         program = self.cleaned_data.get('program')
         program_lead = self.cleaned_data.get('program_lead')
         finance_lead = self.cleaned_data.get('finance_lead')
         technical_lead = self.cleaned_data.get('technical_lead')
         mel_lead = self.cleaned_data.get('mel_lead')
         eniromental_impact = self.cleaned_data.get('eniromental_impact')
         environmental_assessment_att = self.cleaned_data.get('environmental_assessment_att')
         proposed_start_date = self.cleaned_data.get('proposed_start_date')
         proposed_end_date = self.cleaned_data.get('proposed_end_date')
         final_report_due_date = self.cleaned_data.get('final_report_due_date')
         ilead_agency = self.cleaned_data.get('ilead_agency')
         cs_budget = self.cleaned_data.get('cost_sharing_budget')
         mc_budget = self.cleaned_data.get('mc_budget')
         mc_currency = self.cleaned_data.get('mc_currency')
         cs_currency = self.cleaned_data.get('cs_currency')
         ilead_co_agency = self.cleaned_data.get('ilead_co_agency')
         cost_sharing_budget = self.cleaned_data.get('cost_sharing_budget')
       
         if mc_currency == 2:
            mc_budget = mc_budget/120
    
         if cs_currency == 2:
            cs_budget = cs_budget/120
            
         total_budget_usd = mc_budget + cs_budget
         
         budget_limit_min = UserRoles.objects.get(program=program, user=program_lead.user)
         budget_limit_max = UserRoles.objects.get(program=program, user=program_lead.user)
         budget_limit_min = budget_limit_min.approval_budget_min_usd
         budget_limit_max = budget_limit_max.approval_budget_max_usd

         
        
         if program_lead not in UserRoles.objects.filter(program=program) or technical_lead not in UserRoles.objects.filter(program=program) or finance_lead not in UserRoles.objects.filter(program=program):
               self._errors['program'] = self.error_class(['At least 1 of the Leads not belong this program'])

         elif (technical_lead==program_lead or technical_lead==finance_lead or technical_lead==mel_lead):
              self._errors['technical_lead'] = self.error_class(['Lead should take up only one role'])
         elif (program_lead==technical_lead or program_lead==finance_lead or program_lead==mel_lead):
              self._errors['program_lead'] = self.error_class(['Lead should take up only one role'])
         
         elif (finance_lead==technical_lead or finance_lead==program_lead or finance_lead==mel_lead):
              self._errors['finance_lead'] = self.error_class(['Lead should take up only one role'])
         elif (mel_lead==technical_lead or mel_lead==program_lead or mel_lead==finance_lead):
              self._errors['mel_lead'] = self.error_class(['Lead should take up only one role'])
         elif (eniromental_impact == '3' and environmental_assessment_att==None):
              self._errors['eniromental_impact'] = self.error_class(['Attachment required for High Impact'])
         elif ( proposed_end_date != None and proposed_start_date != None and proposed_end_date < proposed_start_date):
               self._errors['proposed_end_date'] = self.error_class(['End date should always be after start date'])
         elif (final_report_due_date != None and proposed_end_date != None and final_report_due_date < proposed_end_date):
             self._errors['final_report_due_date'] = self.error_class(['Reporting Date should always be after end date'])
         elif (ilead_agency != None and ilead_co_agency != None and ilead_co_agency.contains(ilead_agency)):
             self._errors['ilead_agency'] = self.error_class(['Lead Agency & Co-Lead Agency should be different'])
                 
         elif (mc_currency != None and cs_currency != None and mc_currency != cs_currency):
             self._errors['mc_currency'] = self.error_class(['Different Currency for MC & Cost Sharing'])
         elif (total_budget_usd > budget_limit_max or total_budget_usd < budget_limit_min):
             self._errors['program_lead'] = self.error_class(['Check Program Lead budget limit'])
        
         return cleaned_data








class IcnAreaFormEdit(forms.ModelForm):
    
    class Meta:
        model = IcnImplementationArea
        fields=['region',
            'zone',
            'woreda',
            ]
        exclude=  ['icn']

class IcnAreaFormE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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

        myfield = ['region',
            'zone','woreda'          

            ]
        for field in myfield:
            self.fields[field].required = True 
    
    class Meta:
            model = IcnImplementationArea
            fields=['region',
            'zone',
            'woreda',
            ]
            exclude=  ['icn']

class IcnSubmitForm(forms.ModelForm):
     
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        icn = kwargs.pop('icn', None)
        sid = kwargs.pop('sid', None)
        super(IcnSubmitForm, self).__init__(*args, **kwargs)

        if sid==1 and IcnSubmit.objects.filter(icn_id=icn).exists():
            icnsubmit = IcnSubmit.objects.filter(icn_id=icn).latest('id')
            self.fields['document'].choices = [
                (document.pk, document) for document in Document.objects.filter(id=icnsubmit.document.id)
            ]
        elif sid==2 and IcnSubmit.objects.filter(icn_id=icn).exists():
            icnsubmit = IcnSubmit.objects.filter(icn_id=icn).latest('id')
            self.fields['document'].choices = [
                (document.pk, document) for document in Document.objects.filter(user = user, icn=icn, id__gt=icnsubmit.document.id)
            ]  
        else:
            self.fields['document'].choices = [
                (document.pk, document) for document in Document.objects.filter(user = user, icn=icn)
            ]  
             
               
        self.fields['submission_status'].choices = [
            (submission_status.id, submission_status.name) for submission_status in Submission_Status.objects.filter(id=sid)
        ]

            
       
        self.fields['document'].widget.attrs['readonly'] = True
              
      # invalid input from the client; ignore and fallback to empty City queryset
        

    

        self.fields['submission_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'True'   }    )
        self.fields['submission_note'].required = True 
        self.fields['submission_status'].widget.attrs['readonly'] = True
        self.fields['document'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})

   
         
          
           
    class Meta:
        model = IcnSubmit
        fields=['submission_status',
            'submission_note',
            'document',
           
           
            ]
        exclude=  ['icn',]
            
          


class IcnDocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
              
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'required'  }    )
        self.fields['description'].required = True 
        self.fields['document'].required = True 
        self.fields['document'].widget= forms.widgets.FileInput(attrs={'accept':'application/doc'})
    
    
        
    class Meta:
        model = Document
        fields = ('description', 'document',)

        exclude=  ['icn','user', 'ver']
    
    


class IcnApprovalTForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
          did = kwargs.pop('did', None)
          user = kwargs.pop('user', None)
          icn = kwargs.pop('icn', None)
          super(IcnApprovalTForm, self).__init__(*args, **kwargs)    
          
          document_id = self.instance.document.id

          self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'required'  }    )
          self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalt_Status.objects.filter(id=did)
                 ]
          self.fields['approval_status'].widget.attrs['readonly'] = True
          if did == 2:
               self.fields['document'].choices = [
             (document.pk, document) for document in Document.objects.filter(user= user,icn= icn, id__gt=document_id)
         ]
       
          if did == 3 or did==4:
               self.fields['document'].choices = [
             (document.pk, document) for document in Document.objects.filter(id=document_id)
                 ]
               self.fields['document'].widget.attrs['readonly'] = True
        
          self.fields['document'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
        
     class Meta:
            model = IcnSubmitApproval_T
            fields = ('approval_note','approval_status','document')
            readonly_fields = ('approval_status',)

            exclude=  ['icn','user',]
            
class IcnApprovalMForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
          did = kwargs.pop('did', None)
          icn = kwargs.pop('icn', None)
          user = kwargs.pop('user', None)
          super(IcnApprovalMForm, self).__init__(*args, **kwargs)
       
     
          document_id = self.instance.document.id
          self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'required'  }    )
          self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalt_Status.objects.filter(id=did)
                 ]
          self.fields['approval_status'].widget.attrs['readonly'] = True
          if did == 2:
               self.fields['document'].choices = [
             (document.pk, document) for document in Document.objects.filter(user= user,icn= icn, id__gt=document_id)
         ]
       
          if did == 3 or did==4:
               self.fields['document'].choices = [
             (document.pk, document) for document in Document.objects.filter(id=document_id)
                 ]
               self.fields['document'].widget.attrs['readonly'] = True
        
          self.fields['document'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
        
     class Meta:
            model = IcnSubmitApproval_M
            fields = ('approval_note','approval_status','document')
            readonly_fields = ('approval_status',)

            exclude=  ['icn','user',]

class IcnApprovalFForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
          did = kwargs.pop('did', None)
          icn = kwargs.pop('icn', None)
          user = kwargs.pop('user', None)
          super(IcnApprovalFForm, self).__init__(*args, **kwargs)
          
          document_id = self.instance.document.id
          self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'required'  }    )
          self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalt_Status.objects.filter(id=did)
                 ]
          self.fields['approval_status'].widget.attrs['readonly'] = True
          if did == 2:
               self.fields['document'].choices = [
             (document.pk, document) for document in Document.objects.filter(user= user,icn= icn, id__gt=document_id)
         ]
       
          if did == 3 or did==4:
               self.fields['document'].choices = [
             (document.pk, document) for document in Document.objects.filter(id=document_id)
                 ]
               self.fields['document'].widget.attrs['readonly'] = True
        
          self.fields['document'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
        
     class Meta:
            model = IcnSubmitApproval_F
            fields =  ('approval_note','approval_status','document')

            exclude=  ['icn','user']

class IcnApprovalPForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
           did = kwargs.pop('did', None)
           icn = kwargs.pop('icn', None)
           user = kwargs.pop('user', None)
           super(IcnApprovalPForm, self).__init__(*args, **kwargs)

           document_id = self.instance.document.id
           self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'required'  }    )
           self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalf_Status.objects.filter(id=did)
                 ]
           self.fields['approval_status'].widget.attrs['readonly'] = True
           if did == 2:
                self.fields['document'].choices = [
             (document.pk, document) for document in Document.objects.filter(user= user,icn= icn, id__gt=document_id)
            ]
       
           if did == 3 or did==4:
                self.fields['document'].choices = [
                (document.pk, document) for document in Document.objects.filter(id=document_id)
                 ]
                self.fields['document'].widget.attrs['readonly'] = True
        
           self.fields['document'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
                
              
    
               
     class Meta:
            model = IcnSubmitApproval_P
            fields =  ('approval_note','approval_status','document')

            exclude=  ['icn','user']
    
    



class ImpactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        program = kwargs.pop('program', None)
        super().__init__(*args, **kwargs)
    
       
        self.fields['indicators'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'select2', 'class':'form-control form-control-sm', 'data-width': '100%'})
        if program:
             self.fields['indicators'].queryset = Indicator.objects.filter(program_id=program.id)
        else:
            self.fields['indicators'].queryset = Indicator.objects.all()
        self.fields['indicators'].required = True 
        self.fields['title'].required = True 
       
        self.fields['impact_pilot'].required = True 
        self.fields['impact_scaleup'].required = True 
        self.fields['unit'].required = True 
    class Meta:
        model = Impact
        fields = ['title', 'description','unit','impact_pilot' ,'impact_scaleup',
                    'indicators']
        exclude=  ['icn']

    def clean(self):
         cleaned_data = super().clean()
         unit = self.cleaned_data.get('unit')
         impact_pilot = self.cleaned_data.get('impact_pilot')
         impact_scaleup = self.cleaned_data.get('impact_scaleup')
         diff1 = (impact_pilot - int(impact_pilot) )
         diff2 = (impact_scaleup - int(impact_scaleup) )
         
         if (unit == 2 and ( impact_pilot > 100 or impact_scaleup > 100 )):
              self._errors['unit'] = self.error_class(['Target with percentage unit exceeds 100%'])
         elif (unit == 1 and diff1 != 0.0):
              self._errors['impact_pilot'] = self.error_class(['value should match int or ends with .0'])
         elif (unit == 1 and diff2 != 0.0):
              self._errors['impact_scaleup'] = self.error_class(['value should match int or ends with .0'])
         return cleaned_data

class ActivityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
      
        if user:
            
            program = Program.objects.filter(users_role=user, userroles__is_pacn_initiator=True)
            self.fields['program_lead'].queryset =  UserRoles.objects.filter(program__in=program, is_pacn_program_approver=True, approval_budget_min_usd__isnull=False, approval_budget_max_usd__isnull=False).exclude(user=user)
            self.fields['program_lead'].initial=UserRoles.objects.filter(program__in=program, is_pacn_program_approver=True, approval_budget_min_usd__isnull=False, approval_budget_max_usd__isnull=False).exclude(user=user).first()
            self.fields['technical_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pacn_technical_approver=True).exclude(user=user)
            self.fields['technical_lead'].initial=UserRoles.objects.filter(program__in=program, is_pacn_technical_approver=True).exclude(user=user).first()
            self.fields['mel_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pacn_mel_approver=True).exclude(user=user)
            self.fields['mel_lead'].initial=UserRoles.objects.filter(program__in=program, is_pacn_mel_approver=True).exclude(user=user).first()
            self.fields['finance_lead'].queryset = UserRoles.objects.filter(program__in=program, is_pacn_finance_approver=True).exclude(user=user)
            self.fields['finance_lead'].initial=UserRoles.objects.filter(program__in=program, is_pacn_finance_approver=True).exclude(user=user).first()
            self.fields['icn'].queryset = Icn.objects.filter(program__in=program, approval_status="100% Approved")
            self.fields['alead_agency'].queryset = Portfolio.objects.filter(id=user.profile.portfolio_id).order_by('id')
            self.fields['alead_agency'].initial = Portfolio.objects.filter(id=user.profile.portfolio_id).first()
            self.fields['alead_co_agency'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
            self.fields['alead_co_agency'].queryset = Portfolio.objects.exclude(Q(id=user.profile.portfolio_id)).order_by('id')
        myfield = ['title',
            'icn',
            'description',
            'proposed_start_date', 
            'proposed_end_date',
            'alead_agency',
            'final_report_due_date',
            'program_lead',
            'technical_lead',
            'finance_lead',
            'mel_lead',
            'mc_currency',
            'cs_currency',
            'mc_budget',
           
            'cost_sharing_budget',
            'aworeda',
            
            
            
           
          


           
            

            ]
        for field in myfield:
            self.fields[field].required = True 
 
        
    

        self.fields['aworeda'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
        pia = ImplementationArea.objects.filter(program__in=program).values_list('region').distinct()
        all_woreda = Region.objects.filter(id__in=pia)
        self.fields['aworeda'].choices = [
             
             
             (name, [(ia.id, ia) for ia in ImplementationArea.objects.filter(region=name, program__in=program)])
                        for name in all_woreda
                
            ]
       
        self.fields['proposed_start_date'].widget = forms.widgets.DateInput(
          
            attrs={
               'type': 'date', 'placeholder': 'yyyy-mm-dd',
                'class': 'form-control',
                'required': 'true'
                
                
                }
            )
  
        self.fields['proposed_end_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['final_report_due_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-contro-sm', 'rows':'3', 'required':'required'  }    )
        
        
       
       
        self.fields['aworeda'].required = True 
        self.fields['mc_budget'].required = True 
        self.fields['cost_sharing_budget'].required = True 
        self.fields['aworeda'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select',  'data-width': '100%'})
         
        pia = ImplementationArea.objects.filter(program__in=program).values_list('region').distinct()
        all_woreda = Region.objects.filter(id__in=pia)
        self.fields['aworeda'].choices = [
             
             
             (name, [(ia.id, ia) for ia in ImplementationArea.objects.filter(region=name, program__in=program)])
                        for name in all_woreda
                
            ]
        
         
    class Meta:
        model = Activity
        fields=['title',
            'icn',
            'description',
            'proposed_start_date', 
            'proposed_end_date',
            
            'final_report_due_date',
            'program_lead',
            'technical_lead',
            'finance_lead',
            'mel_lead',
            'aworeda',
            'mc_budget',
           
            'cost_sharing_budget',
            'mc_currency',
            'cs_currency',
            
          
            'alead_agency',
            'alead_co_agency',
           
          


           
            

            ]

        exclude=  ['status', 'approval_status',  'user',]
        
    def clean(self):
        cleaned_data = super().clean()
        if self.cleaned_data.get('icn'):
            icn = self.cleaned_data.get('icn')
            icn = Icn.objects.get(id=icn.id)
            
        
        alead_agency = self.cleaned_data.get('alead_agency')
        mc_currency = self.cleaned_data.get('mc_currency')
        cs_currency = self.cleaned_data.get('cs_currency')
        if self.cleaned_data.get('mc_budget') != None:
            mc_budget = self.cleaned_data.get('mc_budget')
        else:
            mc_budget = 0

        if self.cleaned_data.get('cost_sharing_budget') != None:
            cs_budget = self.cleaned_data.get('cost_sharing_budget')
        else:
            cs_budget = 0
            
        if mc_currency == 2:
            mc_budget = mc_budget/120
    
        if cs_currency == 2:
            cs_budget = cs_budget/120
            
        tactbud = mc_budget + cs_budget
        rembud = icn.get_remaining_budget()
        
        
        if self.instance is not None and self.instance.pk is not None:
             rembud = rembud + self.instance.activity_total_budget()
        
        alead_co_agency = self.cleaned_data.get('alead_co_agency')
        cost_sharing_budget= self.cleaned_data.get('cost_sharing_budget')
        program_lead = self.cleaned_data.get('program_lead')
        finance_lead = self.cleaned_data.get('finance_lead')
        technical_lead = self.cleaned_data.get('technical_lead')
        mel_lead = self.cleaned_data.get('mel_lead')
        
         
        proposed_start_date = self.cleaned_data.get('proposed_start_date')
        proposed_end_date = self.cleaned_data.get('proposed_end_date')
        final_report_due_date = self.cleaned_data.get('final_report_due_date')

        budget_limit_min = UserRoles.objects.get(program=icn.program, user=program_lead.user)
        budget_limit_max = UserRoles.objects.get(program=icn.program, user=program_lead.user)
        budget_limit_min = budget_limit_min.approval_budget_min_usd
        budget_limit_max = budget_limit_max.approval_budget_max_usd

        if (technical_lead==program_lead or technical_lead==finance_lead or technical_lead==mel_lead):
              self._errors['technical_lead'] = self.error_class(['Lead should take up only one role'])
        elif (program_lead==technical_lead or program_lead==finance_lead or program_lead==mel_lead):
              self._errors['program_lead'] = self.error_class(['Lead should take up only one role'])
         
        elif (finance_lead==technical_lead or finance_lead==program_lead or finance_lead==mel_lead):
              self._errors['finance_lead'] = self.error_class(['Lead should take up only one role'])
        elif (mel_lead==technical_lead or mel_lead==program_lead or mel_lead == finance_lead):
              self._errors['mel_lead'] = self.error_class(['Lead should take up only one role'])
        
        elif ( proposed_end_date != None and proposed_start_date != None and proposed_end_date < proposed_start_date):
               self._errors['proposed_end_date'] = self.error_class(['End date should always be after start date'])
        elif (final_report_due_date != None and proposed_end_date != None and final_report_due_date < proposed_end_date):
             self._errors['final_report_due_date'] = self.error_class(['Reporting Date should always be after end date'])
        elif ((proposed_start_date != None and proposed_start_date > icn.proposed_end_date) or (proposed_start_date != None and proposed_start_date < icn.proposed_start_date)):
             self._errors['proposed_start_date'] = self.error_class(['Activity Date should align with its parent intervention period'])
        elif ((proposed_end_date != None and proposed_end_date > icn.proposed_end_date) or (proposed_end_date != None and proposed_end_date < icn.proposed_start_date)):
             self._errors['proposed_end_date'] = self.error_class(['Activity Date should align with its parent intervention period'])
        elif ((final_report_due_date != None and final_report_due_date > icn.final_report_due_date) or (final_report_due_date != None and final_report_due_date < icn.proposed_start_date)):
             self._errors['final_report_due_date'] = self.error_class(['Activity Date should align with its parent intervention period'])
        elif (alead_agency != None and alead_co_agency != None and alead_co_agency.contains(alead_agency)):
             self._errors['alead_agency'] = self.error_class(['Lead Agency & Co-Lead Agency should be different'])
        elif ((mc_currency != None and cs_currency != None) and mc_currency != cs_currency  ):
              self._errors['mc_currency'] = self.error_class(['Different currency for MC & cost sharing budget'])
        elif ((mc_budget != None and cs_budget != None) and tactbud > rembud  ):
              self._errors['mc_budget'] = self.error_class(['Please check Intervention & Activity Budget '])
        elif (tactbud < budget_limit_min or tactbud > budget_limit_max  ):
              self._errors['program_lead'] = self.error_class(['Program Lead not aligh with total budget'])            
        return cleaned_data

class ActivityAreaFormE(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
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

        myfield = ['region',
            'zone','woreda'          

            ]
        for field in myfield:
            self.fields[field].required = True 
    
    class Meta:
            model = ActivityImplementationArea
            fields=['region',
            'zone',
            'woreda',
            ]
            exclude=  ['activity']

class ActivityImpactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        icn = kwargs.pop('icn', None)
        super().__init__(*args, **kwargs)
    

        self.fields['impact'].widget =  s2forms.Select2MultipleWidget(attrs={ 'type': 'checkbox', 'class':'form-control form-control-sm select', 'data-width': '100%'})
        if icn:
             self.fields['impact'].queryset = Impact.objects.filter(icn_id=icn.id)
        else:
            self.fields['impact'].queryset = Impact.objects.all()
        self.fields['impact'].required = True 
        self.fields['title'].required = True 
        self.fields['description'].required = True 
        self.fields['impact_pilot'].required = True 
        self.fields['impact_scaleup'].required = True 
    class Meta:
        model = ActivityImpact
        fields = ['title','description','unit', 'impact_pilot' ,'impact_scaleup',
                    'impact']
        exclude=  ['activity']
    
    def clean(self):
         cleaned_data = super().clean()
         unit = self.cleaned_data.get('unit')
         impact_pilot = self.cleaned_data.get('impact_pilot')
         impact_scaleup = self.cleaned_data.get('impact_scaleup')
         diff1 = (impact_pilot - int(impact_pilot) )
         diff2 = (impact_scaleup - int(impact_scaleup) )
         if (unit == 2 and ( impact_pilot > 100 or impact_scaleup > 100 )):
              self._errors['unit'] = self.error_class(['Target with percentage unit exceeds 100%'])
         elif (unit == 1 and diff1 != 0.0):
              self._errors['impact_pilot'] = self.error_class(['value should match int or ends with .0'])
         elif (unit == 1 and diff2 != 0.0):
              self._errors['impact_scaleup'] = self.error_class(['value should match int or ends with .0'])
         return cleaned_data

class ActivitySubmitForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
          user = kwargs.pop('user', None)
          activity = kwargs.pop('activity', None)
          sid = kwargs.pop('sid', None)
          super(ActivitySubmitForm, self).__init__(*args, **kwargs)
                
         
          if sid:
               self.fields['submission_status'].choices = [
                        (submission_status.id, submission_status.name) for submission_status in Submission_Status.objects.filter(id=sid)
                    ]
                 

            
          if sid == 2 and ActivitySubmit.objects.filter(activity_id=activity).exists():
               activitysubmit = ActivitySubmit.objects.filter(activity_id=activity).latest('id')
              
               self.fields['document'].choices =  [
                    (document.pk, document) for document in ActivityDocument.objects.filter(user=user, activity=activity, id__gt=activitysubmit.document.id)
                        ] 
          elif sid == 1  and ActivitySubmit.objects.filter(activity_id=activity).exists():
               activitysubmit = ActivitySubmit.objects.filter(activity_id=activity).latest('id')
               self.fields['document'].choices = [
                (document.pk, document) for document in ActivityDocument.objects.filter(id=activitysubmit.document.id)
                        ] 
          else:
               self.fields['document'].choices = [
                (document.pk, document) for document in ActivityDocument.objects.filter(user=user, activity=activity)
                        ] 
              
            
      # invalid input from the client; ignore and fallback to empty City queryset
        
  
    

          self.fields['submission_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'True'   }    )
          self.fields['submission_note'].required = True 
          self.fields['document'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
          self.fields['submission_status'].widget.attrs['readonly'] = True
          self.fields['document'].widget.attrs['readonly'] = True


     class Meta:
          model = ActivitySubmit
          fields=['submission_status',
            'submission_note',
            'document',
           
           
            ]
          exclude=  ['activity',]
            
          


class ActivityDocumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
              
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'required'  }    )
        self.fields['description'].required = True 
        self.fields['document'].required = True 
    
    
        
    class Meta:
        model = ActivityDocument
        fields = ('description', 'document',)

        exclude=  ['activity','user', 'ver']

class ActivityApprovalTForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        did = kwargs.pop('did', None)
        activity = kwargs.pop('activity', None)
        super(ActivityApprovalTForm, self).__init__(*args, **kwargs)

        self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'True'  }    )
        self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalt_Status.objects.filter(id=did)
         ]
          
        if did == 2:       
             self.fields['document'].choices = [
             (document.pk, document) for document in ActivityDocument.objects.filter(user= self.instance.user.user,activity=activity, id__gt=self.instance.document.id)
            
         ]

       
        if did == 3 or did == 4:
             self.fields['document'].widget.attrs['readonly'] = True
             self.fields['document'].choices = [
             (document.pk, document) for document in ActivityDocument.objects.filter(id=self.instance.document.id)
             ]
             

        self.fields['document'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
       
        self.fields['approval_status'].widget.attrs['readonly'] = True

        
        
    class Meta:
            model = ActivitySubmitApproval_T
            fields = ('approval_note','approval_status','document')

            exclude=  ['activity','user',]

class ActivityApprovalMForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        did = kwargs.pop('did', None)
        activity = kwargs.pop('activity', None)
        super(ActivityApprovalMForm, self).__init__(*args, **kwargs)

        self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'True'  }    )
        self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalt_Status.objects.filter(id=did)
         ]
          
        if did == 2:       
             self.fields['document'].choices = [
             (document.pk, document) for document in ActivityDocument.objects.filter(user= self.instance.user.user,activity=activity, id__gt=self.instance.document.id)
            
         ]

       
        if did == 3 or did == 4:
             self.fields['document'].widget.attrs['readonly'] = True
             self.fields['document'].choices = [
             (document.pk, document) for document in ActivityDocument.objects.filter(id=self.instance.document.id)
             ]
        
        self.fields['document'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
       
        self.fields['approval_status'].widget.attrs['readonly'] = True
        
    class Meta:
            model = ActivitySubmitApproval_M
            fields = ('approval_note','approval_status','document')

            exclude=  ['activity','user',]

class ActivityApprovalPForm(forms.ModelForm):
    #document = forms.ChoiceField()
    #document.widget.attrs.update({'required':'True'})
    def __init__(self, *args, **kwargs):
        did = kwargs.pop('did', None)
        activity = kwargs.pop('activity', None)
        super(ActivityApprovalPForm, self).__init__(*args, **kwargs)
       
        self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'True'  }    )
        self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalf_Status.objects.filter(id=did)
          ]
          
        if did == 2:       
             self.fields['document'].choices = [
             (document.pk, document) for document in ActivityDocument.objects.filter(user= self.instance.user.user,activity=activity, id__gt=self.instance.document.id)
            
         ]

       
        if did == 3 or did == 4:
             self.fields['document'].widget.attrs['readonly'] = True
             self.fields['document'].choices = [
             (document.pk, document) for document in ActivityDocument.objects.filter(id=self.instance.document.id)
             ]
        
        self.fields['document'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
       
        self.fields['approval_status'].widget.attrs['readonly'] = True
        
    class Meta:
            model = ActivitySubmitApproval_P
            fields = ('approval_note','approval_status','document')

            exclude=  ['activity','user',]

class ActivityApprovalFForm(forms.ModelForm):
    #document = forms.ChoiceField()
    #document.widget.attrs.update({'required':'True'})
    def __init__(self, *args, **kwargs):
         did = kwargs.pop('did', None)
         activity = kwargs.pop('activity', None)
         super(ActivityApprovalFForm, self).__init__(*args, **kwargs)   
        
         self.fields['approval_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'required':'True'  }    )
         self.fields['approval_status'].choices = [
             (approvalt_status.id, approvalt_status.name) for approvalt_status in Approvalt_Status.objects.filter(id=did)
          ]
          
         if did == 2:       
             self.fields['document'].choices = [
             (document.pk, document) for document in ActivityDocument.objects.filter(user= self.instance.user.user,activity=activity, id__gt=self.instance.document.id)
            
         ]

       
         if did == 3 or did == 4:
             self.fields['document'].widget.attrs['readonly'] = True
             self.fields['document'].choices = [
             (document.pk, document) for document in ActivityDocument.objects.filter(id=self.instance.document.id)
             ]
        
         self.fields['document'].widget.attrs.update({'class': 'form-control m-input form-control-sm','required':'True'})
       
         self.fields['approval_status'].widget.attrs['readonly'] = True
        
        
    class Meta:
            model = ActivitySubmitApproval_F
            fields = ('approval_note','approval_status','document')

            exclude=  ['activity','user',]

