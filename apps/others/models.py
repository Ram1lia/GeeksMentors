from django.db import models
from apps.users.models import User


class Admin(models.Model):
    image = models.ImageField('Фото', upload_to='admin_photo/')
    first_name = models.CharField('Имя', max_length=20)
    last_name = models.CharField('Фамилия', max_length=20)
    position = models.CharField('Должность', max_length=50)

    def __str__(self):
        return self.first_name


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_add = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:15]