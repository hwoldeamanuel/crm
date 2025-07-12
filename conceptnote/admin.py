from django.contrib import admin

# Register your models here.
from .models import Icn, IcnImplementationArea, IcnSubmit, IcnSubmitApproval_F, IcnSubmitApproval_P, IcnSubmitApproval_T, Impact, Document, Activity,ActivityImplementationArea, ActivityImpact, ActivityDocument,ActivitySubmit,ActivitySubmitApproval_F,ActivitySubmitApproval_P,ActivitySubmitApproval_T

admin.site.register(Icn)
admin.site.register(IcnImplementationArea)
admin.site.register(IcnSubmit)
admin.site.register(IcnSubmitApproval_F)
admin.site.register(IcnSubmitApproval_P)
admin.site.register(IcnSubmitApproval_T)
admin.site.register(Impact)
admin.site.register(Document)
admin.site.register(Activity)
admin.site.register(ActivityImplementationArea)
admin.site.register(ActivityImpact)
admin.site.register(ActivitySubmitApproval_T)
admin.site.register(ActivitySubmitApproval_P)
admin.site.register(ActivitySubmitApproval_F)
admin.site.register(ActivitySubmit)
admin.site.register(ActivityDocument)