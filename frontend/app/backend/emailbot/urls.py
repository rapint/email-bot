"""
URL configuration for emailbot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth import logout
from django.shortcuts import redirect
from mailer import views


# Custom logout view to allow GET
def custom_logout_view(request):
    logout(request)
    return redirect('login')  # redirect to login page after logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('mailer/', include('mailer.urls')),
    path('', include('mailer.urls')),

    # Login
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='mailer/login.html'),
        name='login'
    ),
    
    path('get-logs/', views.get_logs, name='get_logs'),

    # Logout (custom view)
    path(
        'logout/',
        custom_logout_view,
        name='logout'
    ),
]
