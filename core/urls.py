from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from knowledge.token import MyTokenObtainPairView  # Import your custom view

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include('knowledge.urls')),
    
    # JWT Authentication (kept in core)
    path('api/auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Optional: Add token verify endpoint
    # path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]