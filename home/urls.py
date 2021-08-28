from django.urls import path
from .views import analyse, cleanse, home, login, selectCol,upload
urlpatterns = [
    path("upload/",upload),
    path("",home),
    path("analyze/",analyse),
    path("selectCol",selectCol),
    path("cleanse",cleanse)
]