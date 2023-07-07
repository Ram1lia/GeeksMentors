from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from .models import Mentor, FavoriteMentor
from .serializers import MentorSerializer, MentorDetailSerializer, MentorListsSerializer, MentorProfileSerializer, \
    FavoriteMentorSerializer, MentorReviewSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from django.http import HttpResponseRedirect
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MentorFilter
from django.db.models import Count
from rest_framework.views import APIView
from apps.users.models import User
from apps.users.serializers import PersonalProfileSerializer
from rest_framework import status


class MentorListAPIView(ListAPIView):
    queryset = Mentor.objects.filter(is_active=True).annotate(like_count=Count('likes')).order_by('-like_count')
    serializer_class = MentorListsSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MentorFilter


class MentorCreateAPIView(CreateAPIView):
    queryset = Mentor.objects.filter(is_active=True)
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user

        list_data = [request.data['name']]
        for data in list_data:
            if not data.exists():
                raise ValueError('This is must form')

        mentor_data = {
            'user': user.id,
            'course': user.course,
            'month': user.month,
            'name': request.data['name'],
            'tel': request.data['tel'],
            'about': request.data['about'],
            'skils': request.data['skils'],
            'worktimes': request.data['worktimes'],
            'language': request.data['language']
        }

        serializer = MentorSerializer(data=mentor_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class MentorDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Mentor.objects.filter(is_active=True)
    serializer_class = MentorDetailSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class MentorProfileView(APIView):
    def get(self, request):
        user = request.user
        if user.is_mentor:
            snippets = Mentor.objects.filter(user=user)
            serializer = MentorProfileSerializer(snippets, many=True)
            return Response(serializer.data)
        else:
            snippets = User.objects.filter(email=user.email)
            serializer = PersonalProfileSerializer(snippets, many=True)
            return Response(serializer.data)


class AddLike(ListCreateAPIView):
    def post(self, request, pk, *args, **kwargs):
        mentor = Mentor.objects.get(pk=pk)
        is_dislike = False

        for dislike in mentor.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break
        if is_dislike:
            mentor.dislikes.remove(request.user)

        is_like = False

        for like in mentor.likes.all():
            if like == request.user:
                is_like = True
                break
        if not is_like:
            mentor.likes.add(request.user)

        if is_like:
            mentor.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class AddDislike(ListCreateAPIView):
    def post(self, request, pk, *args, **kwargs):
        mentor = Mentor.objects.get(pk=pk)
        is_like = False

        for like in mentor.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            mentor.likes.remove(request.user)

        is_dislike = False

        for dislike in mentor.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            mentor.dislikes.add(request.user)

        if is_dislike:
            mentor.dislikes.remove(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class FavoriteMentorListCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        favorite_mentors = FavoriteMentor.objects.filter(user=request.user)
        serializer = FavoriteMentorSerializer(favorite_mentors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = FavoriteMentorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(data={"msg": "created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavoriteMentorDeleteView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request, mentor_id):
        favorite_mentor = FavoriteMentor.objects.filter(user=request.user, mentor_id=mentor_id)
        if favorite_mentor.exists():
            favorite_mentor.delete()
            return Response(data={"msg": "deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={"error": "Favorite mentor not found"}, status=status.HTTP_404_NOT_FOUND)


class MentorReviewCreateView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = MentorReviewSerializer(data=request.data)
        if serializer.is_valid():

            review_text = serializer.validated_data.get('review', '')
            if len(review_text) < 10:
                return Response({'error': 'The review must be at least 10 characters long.'}, status=400)

            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
