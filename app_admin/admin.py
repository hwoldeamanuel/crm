from django.contrib import admin
from .models import Portfolio_Category, Portfolio_Type, Region, Zone, Woreda, Feedback_Resolution, Country, FieldOffice, Approvalt_Status, Approvalf_Status, Submission_Status, Travel_Cost,Fund, Lin_Code, Feedback_Category, Feedback_Channel, Informant_Age, Informant_Gender, Informed_Consent, Informant_Status,Feedback_Status,Feedback_Response_Type
# Register your models here.
#kflkdsjf
admin.site.register(Portfolio_Type)
admin.site.register(Portfolio_Category)
admin.site.register(Region)
admin.site.register(Zone)
admin.site.register(Country)
admin.site.register(Woreda)
admin.site.register(FieldOffice)
admin.site.register(Approvalt_Status)
admin.site.register(Approvalf_Status)
admin.site.register(Submission_Status)
admin.site.register(Travel_Cost)
admin.site.register(Fund)
admin.site.register(Lin_Code)
admin.site.register(Feedback_Category)
admin.site.register(Feedback_Channel)
admin.site.register(Informant_Age)
admin.site.register(Informant_Gender)
admin.site.register(Informed_Consent)   
admin.site.register(Informant_Status)
admin.site.register(Feedback_Status)
admin.site.register(Feedback_Response_Type)
admin.site.register(Feedback_Resolution)


