from django.contrib import admin
from . import models


admin.site.register(models.Mentor)
admin.site.register(models.WorkTimes)
admin.site.register(models.FavoriteMentor)
admin.site.register(models.MentorReview)
