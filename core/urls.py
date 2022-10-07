"""core URL Configuration

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
from dj_rest_auth.registration.views import VerifyEmailView
from django.contrib import admin
from django.urls import include, path

from .root_api_view import FacebookLogin, api_root

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api_root, name="api_root"),
    path("api/v1/accounts/", include("accounts.urls", namespace="v1")),
    path("api_auth/", include("rest_framework.urls")),  # login
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),  # registration dj rest auth
    path("dj-rest-auth/account-confirm-email/", VerifyEmailView.as_view(), name="account_email_verification_sent"),
    path("__debug__/", include("debug_toolbar.urls")),
]


urlpatterns += [path("dj-rest-auth/facebook/", FacebookLogin.as_view(), name="fb_login")]
