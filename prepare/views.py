from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from matplotlib.pyplot import get
from home.views import getCatCols
import pandas as pd
import json

from utilities.dataStorage import readData

# Create your views here.

def cleanse(request):
    if(request.method=="POST"):
        features=request.POST.getlist('columns')
        target=request.POST.getlist('target')
        username=request.COOKIES['username']
        data=readData(username+"_data")
        cat_cols=data.select_dtypes(exclude="number").columns
        data=data[features+target]
        na_cols=data.isna().sum(axis=0)
        print(na_cols)
        return render(request,"clean.html")
def getRows(request):
    username=request.COOKIES['username']
    df=readData(username+"_data")
    # print(df)
    rows=request.GET.get('rows',None)
    new_df=df.head(int(rows)).values.tolist()
    new_df=[list(map(str,a)) for a in new_df]
    resp={'data':json.dumps(new_df),'columns':json.dumps(list(df.columns.values))}
    # new_df=df.head(int(rows)).to_json(orient="records")
    # resp={"data":new_df,"columns":json.dumps(list(df.columns.values))}
    return JsonResponse(resp)

        
     
