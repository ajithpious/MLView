from typing import Sequence
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
import pandas as pd
import matplotlib.pyplot as plt
from .dataUploadForm import DataForm
from django.contrib import messages
import math
import plotly.express as px

# Create your views here.

def home(request):
    if(request.method=='POST'):
        userName=request.POST['username']
        passWord=request.POST['password']
        if(userName=="admin" and passWord=="admin"):
            return render(request,"home.html")
        else:
            messages.error(request, 'Username or Password Incorrect')
            return redirect(request.META['HTTP_REFERER'])
   
def upload(request):
    if(request.method=="POST"):
        if(request.FILES.get('myfile',None)==None):
            return redirect(request.META['HTTP_REFERER'])
        noHeader=request.POST.get('noHeader',None)
        if(noHeader):
            data=pd.read_csv(request.FILES['myfile'],header=None)
            describe=data.describe();
            describe.insert(0,"Parameter",describe.index)
            checkbox=request.POST.getlist('plot')
            plot(data,checkbox)
            return render(request,"analyzeResult.html",{"des":describe,"plots":checkbox,"values":list(describe.values)})
        head=request.POST.get('header',None)
        print("head=",head)
        if(head=="" or int(head)<1):
            data=pd.read_csv(request.FILES['myfile'],header=0)
            describe=data.describe();
            describe.insert(0,"Parameter",describe.index)
            checkbox=request.POST.getlist('plot')
            plot(data,checkbox)
            return render(request,"analyzeResult.html",{"des":describe,"plots":checkbox,"values":list(describe.values)})
        elif(int(head)>0):
            head=int(head)
            data=pd.read_csv(request.FILES['myfile'],header=head-1)
            describe=data.describe();
            describe.insert(0,"Parameter",describe.index)
            checkbox=request.POST.getlist('plot')
            plot(data,checkbox)

            fig=px.scatter(x=[1,2,3,4,5,6],y=[1,2,3,4,5,6])
            graph=fig.to_html(full_html=False,default_height=500, default_width=700)

            # return render(request,"analyzeResult.html",{"des":describe,"plots":checkbox,"values":list(describe.values)})

            return render(request,"analyzeResult.html",{"des":describe,"plots":checkbox,"values":list(describe.values),"graph":graph})
        
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


def getData(request,data):
    describe=data.describe();
    describe.insert(0,"Parameter",describe.index)
    checkbox=request.POST.getlist('plot')
    plot(data,checkbox)
    return 
