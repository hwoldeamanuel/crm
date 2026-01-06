from django.contrib import admin

# Register your models here.
from .models import IcnReport, IcnReportImplementationArea, IcnReportSubmit, IcnReportSubmitApproval_F,IcnReportSubmitApproval_P,  IcnReportImpact, IcnReportDocument, ActivityReport,ActivityReportImplementationArea, ActivityReportImpact, ActivityReportDocument,ActivityReportSubmit,ActivityReportSubmitApproval_F,ActivityReportSubmitApproval_P, IcnReportDisaggregate

admin.site.register(IcnReport)
admin.site.register(IcnReportImplementationArea)
admin.site.register(IcnReportSubmit)
admin.site.register(IcnReportSubmitApproval_F)
admin.site.register(IcnReportSubmitApproval_P)

admin.site.register(IcnReportImpact)
admin.site.register(IcnReportDocument)
admin.site.register(ActivityReport)
admin.site.register(ActivityReportImplementationArea)
admin.site.register(ActivityReportImpact)
admin.site.register(ActivityReportDocument)
admin.site.register(ActivityReportSubmit)
admin.site.register(ActivityReportSubmitApproval_F)
admin.site.register(ActivityReportSubmitApproval_P)

admin.site.register(IcnReportDisaggregate)
