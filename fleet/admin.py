from django.contrib import admin

# Register your models here.
from .models import Fleet, Fleet_Log, Fleet_Expense
#Fleet_Logg, Fleet_Expense,Generator,Generator_Report


admin.site.register(Fleet)
admin.site.register(Fleet_Expense)
admin.site.register(Fleet_Log)