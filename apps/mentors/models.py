from django.db import models
from apps.users.models import User
from django.contrib.postgres.fields import ArrayField
from django.conf import settings


class WorkTimes(models.Model):
    daystart = models.CharField(max_length=20)
    dayend = models.CharField(max_length=20)
    weekends = models.CharField(max_length=20)
    weekende = models.CharField(max_length=20)

    def __str__(self):
        return f'daystart: {self.daystart}' \
               f'dayend: {self.dayend}' \
               f'weekends: {self.weekends}' \
               f'weekende: {self.weekende}'


class Mentor(models.Model):
    LANGUAGE_CHOICES = (
        ('Русский', 'Русский'),
        ('Кыргызский', 'Кыргызский')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False, blank=True)
    image = models.ImageField(blank=True, upload_to='mentors/', default='mentors/default.jpg')
    name = models.CharField(max_length=15)
    about = models.TextField()
    tel = models.URLField()
    course = models.CharField(max_length=255)
    month = models.CharField(max_length=255)
    language = ArrayField(models.CharField(max_length=20, choices=LANGUAGE_CHOICES))
    skils = ArrayField(models.CharField(max_length=25))
    worktimes = models.ForeignKey(WorkTimes, on_delete=models.CASCADE)
    time_create = models.DateTimeField(auto_now_add=True, null=True)
    time_update = models.DateTimeField(auto_now=True, null=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')

    @property
    def like(self):
        return self.likes.count()

    @property
    def dislike(self):
        return self.dislikes.count()

    class Meta:
        verbose_name = 'Mentor'
        verbose_name_plural = 'Mentors'

    def __str__(self):
        return f'{self.name}'


class FavoriteMentor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)


class MentorReview(models.Model):
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE, related_name='review')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def user_name(self):
        return self.user.name
