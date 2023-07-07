from django_filters import rest_framework as filters
from .models import Mentor


class MentorFilter(filters.FilterSet):
    course = filters.CharFilter()
    month = filters.CharFilter()
    skils = filters.CharFilter()

    class Meta:
        model = Mentor
        fields = ['course', 'month', 'skils']
