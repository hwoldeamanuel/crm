from django.contrib import admin
from .models import Program,   ImplementationArea, Indicator, UserRoles, TravelUserRoles

# Register your models here.
admin.site.register(Program)
admin.site.register(ImplementationArea)


admin.site.register(Indicator)
admin.site.register(UserRoles)
