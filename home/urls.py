from django.urls import path
from .views import analyse, home, login,upload
urlpatterns = [
    path("upload/",upload),
    path("",home),
    path("analyze/",analyse)
]