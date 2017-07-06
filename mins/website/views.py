from django.shortcuts import render, Http404, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from website.form import UserForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from website.models import UserProfile
from website.form import UserForm
import pandas as pd
from django.contrib.auth.decorators import login_required
import sqlite3
import xlrd

def df_to_sql_T(filefullpath, sheet):
    df = pd.read_excel(filefullpath, sheetname=sheet)
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    print(df)
    df = df.T
    print(df)
    con = sqlite3.connect(r"C:\Users\Administrator\Desktop\upload\mins\db.sqlite3")
    df.to_sql(str(sheet), con, if_exists="append")
    print("tosql!")

def df_to_sql(filefullpath, sheet):
    df = pd.read_excel(filefullpath, sheetname=sheet)
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    print(df)
    con = sqlite3.connect(r"C:\Users\Administrator\Desktop\upload\mins\db.sqlite3")
    df.to_sql(str(sheet), con, if_exists="append")
    print("tosql!")


def listing(request):
    context = {}
    if request.method == "POST":
        uf = UserForm(request.POST, request.FILES)
        if request.user.username and uf.is_valid():
            #username = uf.cleaned_data['username']
            user_upload_file = uf.cleaned_data['user_upload_file']
            #写入数据库
            profile = UserProfile()
            profile.username = request.user.username
            profile.user_upload_file = user_upload_file
            profile.save()
            file_name = request.FILES.get('user_upload_file').name
            print(request.FILES.get('user_upload_file').name)
            print(type(request.FILES.get('user_upload_file').name))
            print(type(request.FILES))
            path = "C:\\Users\\Administrator\\Desktop\\upload\\mins\\upload\\upload\\"
            filefullpath = path + file_name
            print(filefullpath)
            if user_upload_file:
                b = xlrd.open_workbook(filefullpath)
                #count = len(b.sheets())#不需要，sheet数都是固定的
                for sheet in range(1,5):
                    if sheet == 1:
                        print(1)
                        df_to_sql_T(filefullpath, sheet)
                    if sheet == 2:
                        print(2)
                        df_to_sql_T(filefullpath, sheet)
                    if sheet == 3:
                        print(3)
                        df_to_sql_T(filefullpath, sheet)
                    if sheet == 4:
                        print(4)
                        df_to_sql(filefullpath, sheet)
            return HttpResponse('upload ok!')
        else:
            return redirect(to='login')
    else:
        uf = UserForm()
    context['uf'] = uf
    return render(request, 'website/templates/listing.html', context)

def index_login(request):
    context = {}
    if request.method == "GET":
        form = AuthenticationForm
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(to='list')
    context['form'] = form
    return render(request, 'register_login.html', context)

def index_register(request):
    context = {}
    if request.method == 'GET':
        form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='login')
    context['form'] = form
    return render(request, 'register_login.html', context)