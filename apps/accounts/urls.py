from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from .views import (
    RegisterView,
    CustomTokenObtainPairView,
    ProfileView,
    UpdateAddressView,
    ChangePasswordView,
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('address/', UpdateAddressView.as_view(), name='update_address'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
]
