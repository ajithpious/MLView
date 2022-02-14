from prepare.views import modify
from prepare.views import reset
from prepare.views import cleanna
from prepare.views import getRows
from prepare.views import cleanse
from django.urls import path
urlpatterns = [
    path("",cleanse),
    path("getRows",getRows),
    path('cleanna',cleanna),
    path('reset',reset),
    path('modify',modify)
]