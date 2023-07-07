from rest_framework.generics import CreateAPIView, ListAPIView
from .models import Question, Admin
from .serializers import QuestionSerializer, AdminSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


class QuestionCreateAPIView(APIView):
    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save(user=request.user)
            return Response(QuestionSerializer(question).data, status=201)
        return Response(serializer.errors, status=400)


class AdminAPIView(ListAPIView):
    queryset = Admin
    serializer_class = AdminSerializer
