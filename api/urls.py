from django.urls import path
from api.views import LoginAPIView, RegisterView, Home
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('home/', Home.as_view(), name='home'),

]