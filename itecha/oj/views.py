from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.views import APIView, Response

from .models import Problem, Submission
from .serializers import (
    BasicProblemSerializer,
    ProblemSerializer,
    SubmissionSerializer,
    UserSerializer,
)


class Login(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"token": str(user.id)})
        else:
            raise ValueError()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user, creator_ip=self.request.META.get("REMOTE_ADDR")
        )
