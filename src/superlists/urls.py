"""
URL configuration for superlists project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import include, path
from lists import views as list_views

# binds a URL to a view function
# when a request is recieved, check the matching URL and call its view function
# 'path()' has three arguments: the URL, the view function, and an optional alias to reference the URL throughout the project
urlpatterns = [
    path("", list_views.home_page, name="home"),
    path("lists/", include("lists.urls")),
]
