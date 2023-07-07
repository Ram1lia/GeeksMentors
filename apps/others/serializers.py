from rest_framework import serializers
from .models import Admin, Question


class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['id', 'image', 'first_name', 'last_name', 'position']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text']
