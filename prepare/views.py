from django.http.response import HttpResponse
from django.shortcuts import render
from matplotlib.pyplot import get
from home.views import getDataFrame,getCatCols
import pandas as pd

# Create your views here.

def cleanse(request):
    if(request.method=="POST"):
        features=request.POST.getlist('columns')
        target=request.POST.getlist('target')
        data=getDataFrame()
        cat_cols=getCatCols()
        data=data[features+target]
        na_cols=data.isna().sum(axis=0)
        print(na_cols)
        
    return HttpResponse(features+target)