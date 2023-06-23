from api.models import User
from .serializers import RegisterSerializer, UsersSerializer
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from .serializers import LoginTokenSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Post
from .serializers import PostSerializer

class LoginAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginTokenSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class UserDetails(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersSerializer
    def get(self, request, pk):
        serializer = UsersSerializer(User.objects.get(id=pk))
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class Home(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(data={} ,status=status.HTTP_200_OK)

class CreatePostView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, likes=[])
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



class RetrieveUpdateDeletePostView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'


class LikePostView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        post.likes.add(request.user)
        return Response(status=status.HTTP_200_OK)


class UnlikePostView(generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        post.likes.remove(request.user)
        return Response(status=status.HTTP_200_OK)