from django import forms
from .models import Portfolio
from app_admin.models import Portfolio_Category, Portfolio_Type, Region, Zone, Woreda
from .models import FieldOffice

class PortfolioForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].widget = forms.widgets.DateInput(
          
            attrs={
               'type': 'date',
                'class': 'form-control'
              
                
                
                }
            )
  
       
        
        self.fields['type'].queryset = Portfolio_Type.objects.all()
       

        self.fields['category'].queryset = Portfolio_Category.objects.none()
       
        if 'type' in self.data:
            try:
                type = int(self.data.get('type'))
                self.fields['category'].queryset = Portfolio_Category.objects.filter(type_id=type).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
             self.fields['category'].queryset = self.instance.type.portfolio_category_set.order_by('name')

       
        self.fields['description'].widget = forms.widgets.Textarea(attrs={'type':'textarea', 'class': 'form-control', 'rows':'3', 'placeholder':'description'   }    )    
        myfield = ['title_short',
            'title','type',    
            'category',     

            ]
        for field in myfield:
            self.fields[field].required = True 
    class Meta:
            model = Portfolio
            fields = "__all__"
    

class FieldOfficeForm(forms.ModelForm):
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
            model = FieldOffice
            fields=['region',
            'zone',
            'woreda',
            'name',
            ]
            exclude=  ['portfolio']
