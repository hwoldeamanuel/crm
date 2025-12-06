from django.contrib import admin

# Register your models here.
from .models import Feedback, Processing, Closing

admin.site.register(Feedback)
admin.site.register(Processing)
admin.site.register(Closing)