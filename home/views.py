from .models import user
from typing import Sequence
from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.conf import include
import pandas as pd
import matplotlib.pyplot as plt
from .dataUploadForm import DataForm
from django.contrib import messages
import math
import numpy as np
import plotly.express as px

# Create your views here.

data=None
mltype=None
cat_cols=None
def home(request):
    if(request.method=='POST'):
        userName=request.POST['username']
        passWord=request.POST['password']
        # cUser=user.objects.get(pk=userName)
        cUser = user.objects.filter(pk=userName).first()
        if(cUser==None):
            messages.error(request, 'Username or Password Incorrect')
            return redirect(request.META['HTTP_REFERER'])
        elif(passWord==str(cUser.password)):
            return render(request,"home.html")
        else:
            messages.error(request, 'Username or Password Incorrect')
            return redirect(request.META['HTTP_REFERER'])
            
   
# def upload(request):
#     global data
#     if(request.method=="POST"):
#         if(request.FILES.get('myfile',None)==None):
#             return redirect(request.META['HTTP_REFERER'])
#         noHeader=request.POST.get('noHeader',None)
#         if(noHeader):
#             data=pd.read_csv(request.FILES['myfile'],header=None)
#             describe=data.describe();
#             describe.insert(0,"Parameter",describe.index)
#             checkbox=request.POST.getlist('plot')
#             plot(data,checkbox)
#             return render(request,"analyzeResult.html",{"des":describe,"plots":checkbox,"values":list(describe.values)})
#         head=request.POST.get('header',None)
#         print("head=",head)
#         if(head=="" or int(head)<1):
#             data=pd.read_csv(request.FILES['myfile'],header=0)
#             describe=data.describe();
#             describe.insert(0,"Parameter",describe.index)
#             checkbox=request.POST.getlist('plot')
#             plot(data,checkbox)
#             return render(request,"analyzeResult.html",{"des":describe,"plots":checkbox,"values":list(describe.values)})
#         elif(int(head)>0):
#             head=int(head)
#             data=pd.read_csv(request.FILES['myfile'],header=head-1)
#             describe=data.describe();
#             describe.insert(0,"Parameter",describe.index)
#             checkbox=request.POST.getlist('plot')
#             plot(data,checkbox)

#             fig=px.scatter(x=[1,2,3,4,5,6],y=[1,2,3,4,5,6])
#             graph=fig.to_html(full_html=False,default_height=500, default_width=700)

#             # return render(request,"analyzeResult.html",{"des":describe,"plots":checkbox,"values":list(describe.values)})

#             return render(request,"analyzeResult.html",{"des":describe,"plots":checkbox,"values":list(describe.values),"graph":graph})
def selectCol(request):
    global data,cat_cols
    data=None
    if(request.method=="POST"):
        noHeader=request.POST.get('noHeader',None)
        # data=None
        describe=None
        head=request.POST.get('header',None)
        if(noHeader):
            data=pd.read_csv(request.FILES['myfile'],header=None)
            describe=data.describe();
        elif(head=="" or int(head)<1):
            data=pd.read_csv(request.FILES['myfile'],header=0)
            describe=data.describe();
        elif(int(head)>0):
            head=int(head)
            data=pd.read_csv(request.FILES['myfile'],header=head-1)
            describe=data.describe();
        else:
            data=pd.read_csv(request.FILES['myfile'],header=0)
            describe=data.describe();
        describe=describe.transpose()
        rows=data.shape[0]
        describe.insert(0,"Column Name",describe.index)
        cat_cols=data.select_dtypes(exclude="number")
        ls=[]
        cat=False
        columns=[]
        index=[]
        cat_df=pd.DataFrame(np.arange(10))
        if(not cat_cols.empty):
            cat=True
            for col in cat_cols:
                column=[]
                valueCount=data[col].value_counts()
                if(valueCount.shape[0]>20):
                    column.append("NA")
                else:
                    values=""
                    for i in range(valueCount.shape[0]):
                        values=values+str(valueCount.index[i])+":"+str(valueCount[i])+","
                    values=values[:-1]
                    column.append(values)
                ls.append(column)
                index.append(valueCount.name)
            columns.append("Value Count")
            cat_df=pd.DataFrame(ls,columns=columns,index=index)
            cat_df.insert(0,"Column Name",cat_cols.columns)
            
        return render(request,"analysis.html",{"numData":describe,"numValues":list(describe.values),"selectCol":True,"cat":cat,"cat_df":cat_df,"catValues":list(cat_df.values),"rows":rows})   
    return render(request,"analysis.html",{"selectCol":True})
def login(request):
    return render(request,"login.html")
def analyse(request):
    return render(request,"analysis.html")


def plot(data,checkbox):
    for plot in checkbox:
            if(plot=="density"):
                columns=data.columns.shape[0]

                fig,axis=plt.subplots(math.ceil(columns/3),3,figsize=(10,(5/9)*columns))
                plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)
                axis=axis.flatten(order="F")
                axis=axis[:columns]                
                data.plot(kind="density",subplots=True,sharex=False,ax=axis)
                plt.savefig("static/img/plot.png")

def cleanse(request):
    if(request.method=="POST"):
        features=request.POST.getlist('columns')
        target=request.POST.getlist('target')
    return HttpResponse(features+target)

def getDataFrame():
    return data
def getCatCols():
    return cat_cols.columns

def getData(request,data):
    describe=data.describe();
    describe.insert(0,"Parameter",describe.index)
    checkbox=request.POST.getlist('plot')
    plot(data,checkbox)
    return 
