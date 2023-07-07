from rest_framework import serializers
from .models import Mentor, WorkTimes, MentorReview, FavoriteMentor
from drf_writable_nested import WritableNestedModelSerializer
from django.core.exceptions import ValidationError


class WorkTimesSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkTimes
        fields = ['daystart', 'dayend', 'weekends', 'weekende']


class MentorReviewSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = MentorReview
        fields = ['text', 'user_name', 'created_at']


class MentorSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    skils = serializers.ListField(child=serializers.CharField(max_length=25))
    worktimes = WorkTimesSerializer()
    language = serializers.ListField(child=serializers.CharField(max_length=25))

    class Meta:
        model = Mentor
        fields = ['id', 'name', 'course', 'month', 'tel', 'language', 'about', 'skils', 'worktimes', 'user',
                  'like', 'dislike']

    @staticmethod
    def validate_name(name):
        if not name.isalpha():
            raise ValidationError('The name must contain only letters')
        return name

    def validate_skils(self, skils):
        if len(skils) != 0:
            raise serializers.ValidationError(f'Mentor must have at least one skill')

        for value in skils:
            if not value.isalpha():
                raise serializers.ValidationError(
                    f'The skill must contain only letters')

        return skils

        def create(self, validated_data):
            user_data = self.context['request'].user  # Извлекаем данные пользователя из запроса

            validated_data['user'] = user_data
            validated_data['course'] = user_data.course
            validated_data['month'] = user_data.month

            return super().create(validated_data)


class MentorListsSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    review = MentorReviewSerializer(many=True)

    class Meta:
        model = Mentor
        fields = ['id', 'name', 'course', 'month', 'tel', 'language', 'user', 'like', 'dislike', 'review']


class MentorDetailSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    skils = serializers.ListField(child=serializers.CharField(max_length=25))
    worktimes = WorkTimesSerializer()
    review = MentorReviewSerializer(many=True)

    class Meta:
        model = Mentor
        fields = ['id', 'name', 'about', 'course', 'month', 'tel', 'language', 'skils', 'worktimes', 'user',
                  'like', 'dislike', 'review']


class MentorProfileSerializer(serializers.ModelSerializer):
    worktimes = WorkTimesSerializer()
    review = MentorReviewSerializer(many=True)

    class Meta:
        model = Mentor
        fields = ('id', 'name', 'about', 'course', 'month', 'tel', 'language', 'skils', 'worktimes',
                  'like', 'dislike', 'review',)


class FavoriteMentorSerializer(serializers.ModelSerializer):
    mentor = MentorSerializer()

    class Meta:
        model = FavoriteMentor
        fields = ('id', 'mentor')

    # def get_mentor(self, favorite_mentor):
    #     serializer_context = {'request': self.context['request']}
    #     mentor = favorite_mentor.mentor
    #     mentor_serializer = MentorSerializer(mentor, context=serializer_context).data
    #     return mentor_serializer


class FavoriteMentorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteMentor
        fields = ('mentor',)

    def create(self, validated_data):
        user = self.context['request'].user

        try:
            mentor = validated_data['mentor']
        except KeyError:
            raise ValidationError({"mentor": ["This field is required."]})

        exist_obj = FavoriteMentor.objects.filter(user=user, mentor=mentor)
        if exist_obj.exists():
            raise ValidationError("This mentor is already added to favorites.")

        favorite_mentor = FavoriteMentor.objects.create(user=user, mentor=mentor)
        return favorite_mentor
