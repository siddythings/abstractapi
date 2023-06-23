from django.urls import path
from api.views import *
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('home/', Home.as_view(), name='home'),
    path('user/<int:pk>/', UserDetails.as_view(), name='users'),
    path('posts/', CreatePostView.as_view(), name='create-post'),
    path('posts/<int:post_id>/', RetrieveUpdateDeletePostView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:post_id>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
]