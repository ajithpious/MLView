from django.urls import path
from .views import analyse, home, login, selectCol,upload
urlpatterns = [
    path("upload/",upload),
    path("",home),
    path("analyze/",analyse),
    path("selectCol",selectCol)
]