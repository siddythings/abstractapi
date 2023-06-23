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
from api.utils import *
import datetime
class LoginAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginTokenSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        requested_data = request.data
        ip = self.get_client_ip(self.request)
        geolocation_data = get_geolocation_data("203.122.40.242")
        
        if not geolocation_data:
            return Response(data={"status":"Invalid IP Address"}, status=status.HTTP_400_BAD_REQUEST)
        
        country_code = geolocation_data.get("country_code")
        day = datetime.datetime.now().date().day
        month = datetime.datetime.now().date().month
        year = datetime.datetime.now().date().year

        holidays = check_holiday(country_code, day, month, year)

        requested_data.update({
            "gio_location": geolocation_data,
            "has_holiday": holidays
        })
        print(requested_data)
        serializer = RegisterSerializer(data=requested_data)
        if serializer.is_valid():
            user = serializer.save()
            # Additional logic for enriching user data and checking holidays can be added here
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


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