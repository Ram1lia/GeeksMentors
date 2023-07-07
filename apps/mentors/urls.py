from apps.mentors import views
from django.urls import path


urlpatterns = [
    path('mentor/', views.MentorListAPIView.as_view()),
    path('mentor/create/', views.MentorCreateAPIView.as_view()),
    path('mentor/<int:pk>/', views.MentorDetailAPIView.as_view()),
    path('mentor/<int:pk>/like', views.AddLike.as_view(), name='like'),
    path('mentor/<int:pk>/dislike', views.AddDislike.as_view(), name='dislike'),
    path('favorite/', views.FavoriteMentorListCreateView.as_view()),
]
