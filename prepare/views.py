from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from matplotlib.pyplot import get
from home.views import getCatCols
import pandas as pd
import json
from utilities.dataStorage import saveDb

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
        fillna_methods=['Mean','Median','Most Frequent','Constant']
        return render(request,"clean.html",{'na_cols':list(zip(na_cols.values,na_cols.index)),'col_names':list(na_cols.index),'fillna_methods':fillna_methods})
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
def cleanna(request):
    if(request.method=="POST"):
        nalist=list(request.POST.items())[1:]
        username=request.COOKIES['username']
        print(nalist)
        col=[]
        dataframe=readData(username+"_data")
        for i in range(len(nalist)):
            if(i%2==0):
                column=nalist[i][0]
                col.append(column)
                if(nalist[i][1]=="1"):
                    dataframe=dataframe.dropna(subset=[column])
                elif(nalist[i][1]=="2"):
                    pass
        data=dataframe[col]
        saveDb(data,username+"_data")
        na_cols=data.isna().sum(axis=0)
        fillna_methods=['Mean','Median','Most Frequent','Constant']
        return render(request,"clean.html",{'na_cols':list(zip(na_cols.values,na_cols.index)),'col_names':list(na_cols.index),'fillna_methods':fillna_methods})

                    

