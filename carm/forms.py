from django import forms
from .models import Feedback, Processing, Closing

from django.db import models
from program.models import Program
from django.contrib.auth.models import User
from portfolio.models import Portfolio
from app_admin.models import Feedback_Channel, Feedback_Category, Informant_Gender, Informant_Age, FieldOffice, Informed_Consent, Informant_Status, Region, Zone, Woreda, Feedback_Response_Type, Feedback_Status, Feedback_Resolution
# Create your models here.
Yes_No =(
    ("1", "Yes"),
    ("2", "No"),
 
    
)
shared_to =(
    ("1", "Internally"),
    ("2", "Externally"),
  
    
)
class FeedbackForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_feedback_recieved'].widget = forms.widgets.DateInput(
          
            attrs={
               'type': 'date',
                'class': 'form-control input-xs'
              
                
                
                }
            )
  
      
        self.fields['summary'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control input-xs', 'rows':'3'  }    )
        self.fields['feedback_channel_other'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'1',    }    )
        self.fields['feedback_channel'].queryset = Feedback_Channel.objects.all()
        self.fields['feedback_category'].queryset = Feedback_Category.objects.all()
        self.fields['office_location'].queryset = FieldOffice.objects.all()
        self.fields['informant_status'].queryset = Informant_Status.objects.all()
        self.fields['informant_location'].queryset = Woreda.objects.all()
        self.fields['informed_consent'].queryset = Informed_Consent.objects.all()
        self.fields['informant_name'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control  input-xs', 'rows':'1', 'required':'True'   }    )
        self.fields['informant_contact_phone_number'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control  input-xs', 'rows':'1', 'required':'True'   }    )
        self.fields['informant_contact_other'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control  input-xs', 'rows':'1',    }    )
        self.fields['supporting_document'].widget = forms.ClearableFileInput(attrs={'class': 'form-control-sm  input-xs', 'file_field_name': forms.ClearableFileInput(),} )
        pia = Woreda.objects.all().values_list('zone_id').distinct()
        all_woreda = Region.objects.filter(id__in=pia)
        self.fields['informant_location'].choices = [
             
             
             (name, [(ia.id, ia) for ia in Woreda.objects.all().filter(zone__region=name)])
                        for name in all_woreda
                
            ]
     class Meta:
         model = Feedback
         fields= '__all__'
         exclude=  ['user']

class ProcessingForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

     
        self.fields['processing_date'].widget = forms.widgets.DateInput(
          
            attrs={
               'type': 'date',
                'class': 'form-control input-xs'
              
                
                
                }
            )
        self.fields['feedback_referred'].widget = forms.widgets.Select(choices = Yes_No,attrs={'type': 'choice', 'class': 'form-control form-control-sm', 'rows':'1', 'placeholder':''   }    )
        self.fields['feedback_shared'].widget = forms.widgets.Select(choices = Yes_No,attrs={'type': 'choice', 'class': 'form-control form-control-sm', 'rows':'1', 'placeholder':''   }    )
       
        self.fields['types_of_response_required_other'].widget = forms.widgets.Textarea(attrs={'type':'textarea ', 'class': 'form-control', 'rows':'1',    }    )
        self.fields['types_of_response_required'].queryset = Feedback_Response_Type.objects.all()
        #self.fields['action_fu_required'].widget = forms.widgets.CheckboxInput(attrs={'type':'checkbox', 'class': 'form-control-sm icheckbox_flat-green1'})
        self.fields['feedback_shared_with_note'].widget = forms.widgets.Textarea(attrs={'type':'textarea ', 'class': 'form-control', 'rows':'1',    }    )
        self.fields['feedback_referred_to'].widget = forms.widgets.Textarea(attrs={'type':'textarea ', 'class': 'form-control', 'rows':'1',    }    )

     class Meta:
         model = Processing
         fields= '__all__'
         exclude=  ['user', 'feedback','updated_by']


class ClosingForm(forms.ModelForm):
     def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

     
        self.fields['closing_date'].widget = forms.widgets.DateInput(
          
            attrs={
               'type': 'date',
                'class': 'form-control input-xs'
              
                
                
                }
            )
        self.fields['response_date'].widget = forms.widgets.DateInput(
          
            attrs={
               'type': 'date',
                'class': 'form-control input-xs'
              
                
                
                }
            )
        
        self.fields['action_taken_other'].widget = forms.widgets.Textarea(attrs={'type':'textarea ', 'class': 'form-control', 'rows':'1',    }    )
        self.fields['response_summary'].widget = forms.widgets.Textarea(attrs={'type':'textarea ', 'class': 'form-control', 'rows':'2',    }    )
     class Meta:
         model = Closing
         fields= '__all__'
         exclude=  ['user', 'feedback','updated_by']