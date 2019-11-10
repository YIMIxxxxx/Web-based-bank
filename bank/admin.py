from django.contrib import admin

# Register your models here.

from . import models

admin.site.register(models.AccntInfo)
admin.site.register(models.StaffInfo)
admin.site.register(models.TransInfo)