from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from matplotlib.pyplot import get
from home.views import getCatCols
import pandas as pd
import json
from sklearn.impute import SimpleImputer
from utilities.dataStorage import saveDb

from utilities.dataStorage import readData

# Create your views here.
fillna_cat_methods=['most_frequent']
fillna_num_methods=['mean','median']
def cleanse(request):
    if(request.method=="POST"):
        features=request.POST.getlist('columns')
        target=request.POST.getlist('target')
        username=request.COOKIES['username']
        data=readData(username+"_data")
        data=data[features+target]
        saveDb(data,username+"_data")
        na_cols=data.isna().sum(axis=0)
        num_cols=get_num_cols(data)
        return render(request,"cleaning\clean.html",{'na_cols':list(zip(na_cols.values,na_cols.index)),'col_names':list(na_cols.index),
        'rows':data.shape[0],'num_cols':num_cols,'fillna_cat_methods':fillna_cat_methods,'fillna_num_methods':fillna_num_methods})
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
        col=[]
        dataframe=readData(username+"_data")
        for i in range(len(nalist)):
            if(i%2==0):
                column=nalist[i][0]
                col.append(column)
                if(nalist[i][1]=="1"):
                    dataframe=dataframe.dropna(subset=[column])
                elif(nalist[i][1]=="2"):
                    method=nalist[i+1][1]
                    imputer=SimpleImputer(strategy=method)
                    col_values=imputer.fit_transform(dataframe[column].values.reshape(-1,1))
                    dataframe[column]=col_values

                    


        data=dataframe[col]
        num_cols=get_num_cols(data)
        saveDb(data,username+"_data")
        na_cols=data.isna().sum(axis=0)
        return render(request,"cleaning\clean.html",{'na_cols':list(zip(na_cols.values,na_cols.index)),'col_names':list(na_cols.index),
        "rows":data.shape[0],'num_cols':num_cols,'fillna_cat_methods':fillna_cat_methods,
        'fillna_num_methods':fillna_num_methods})
def reset(request):
    if(request.method=="POST"):
        username=request.COOKIES['username']
        cols=request.POST.getlist('col_names')
        cols=cols[0].strip('[]').replace("'","").split(",")
        cols=list(map(str.strip,cols))
        print(cols)
        data=readData(username+"_copy")
        data=data[cols]
        saveDb(data,username+"_data")
        na_cols=data.isna().sum(axis=0)
        num_cols=get_num_cols(data)
        return render(request,"cleaning\clean.html",{'na_cols':list(zip(na_cols.values,na_cols.index)),'col_names':list(na_cols.index),"rows":data.shape[0],
        'num_cols':num_cols,'fillna_cat_methods':fillna_cat_methods,'fillna_num_methods':fillna_num_methods})
def get_num_cols(data):
    num_cols=list(data._get_numeric_data().columns.values)
    return num_cols

def modify(request):
    if(request.method=="GET"):
        pass
    return render(request,"cleaning\modify.html")

