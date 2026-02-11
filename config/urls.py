from django.contrib import admin
from django.urls import path, include, redirect
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
        path('', redirect, {'url': '/api/schema/'}, name='root'),

    
    # API Schema
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
    # Apps
    path('api/users/', include('users.urls')),
]
