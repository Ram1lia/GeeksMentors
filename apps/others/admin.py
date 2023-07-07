from django.contrib import admin
from apps.others import models


admin.site.register(models.Admin)
admin.site.register(models.Question)

