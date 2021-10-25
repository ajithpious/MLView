from prepare.views import getRows
from prepare.views import cleanse
from django.urls import path
urlpatterns = [
    path("",cleanse),
    path("getRows",getRows)
]