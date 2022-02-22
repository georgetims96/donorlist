"""donorly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from donorlist import views

urlpatterns = [
    # Path for admin
    path('admin/', admin.site.urls),
    # Path for homepage
    path('', views.home, name = 'home'),
    # Path for logging out a signed in user
    path('logout/', views.logoutuser, name = 'logoutuser'),
    # Path for registering new users
    path('registeruser/', views.registeruser, name = 'registeruser'),
    # Path for logging in existing users
    path('login/', views.loginuser, name = 'loginuser'),
    # Path for user to enter key details after sign up or login
    path('updateprofile/', views.updateprofile, name = 'updateprofile'),
    # Path to see list of top donors
    path('viewdonors/', views.viewdonors, name = 'viewdonors'),
    # Path to send emails
    path('email/', views.email_donors, name='emaildonors')
]
