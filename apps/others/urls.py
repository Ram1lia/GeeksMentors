from django.urls import path
from .views import AdminAPIView, QuestionCreateAPIView


urlpatterns = [
    path('listadmin/', AdminAPIView.as_view(), name='admin'),
    path('question/', QuestionCreateAPIView.as_view(), name='question'),
]