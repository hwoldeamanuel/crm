from django.contrib import admin
from .models import Program,   ImplementationArea, Indicator, UserRoles, TravelUserRoles, CarmUserRoles

# Register your models here.
admin.site.register(Program)
admin.site.register(ImplementationArea)


admin.site.register(Indicator)
admin.site.register(UserRoles)
admin.site.register(TravelUserRoles)
admin.site.register(CarmUserRoles)
