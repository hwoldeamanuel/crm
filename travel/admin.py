from django.contrib import admin

# Register your models here.
from .models import Travel_Request,   Estimated_Cost, Finance_Code, RequestSubmit, SubmitApproval_B, SubmitApproval_F, SubmitApproval_S

# Register your models here.
admin.site.register(Travel_Request)
admin.site.register(Estimated_Cost)
admin.site.register(Finance_Code)
admin.site.register(RequestSubmit)
admin.site.register(SubmitApproval_B)
admin.site.register(SubmitApproval_F)
admin.site.register(SubmitApproval_S)
