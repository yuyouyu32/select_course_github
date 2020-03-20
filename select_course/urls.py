"""select_course URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from select_c import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'index/',views.index),
    path(r'login/',views.login),
    path(r'gochange/',views.gochange),
    path(r'changepass/',views.changepass),
    path(r'submit/',views.submit),
    path(r'managec/',views.managec),
    path(r'changegrade/',views.changegrade),
    path(r'opencrouse/',views.opencrouse),
    path(r'quit/',views.quit),
    path(r'back/',views.back),
    path(r'',views.index),

]
