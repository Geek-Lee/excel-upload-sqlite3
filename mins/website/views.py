from django.shortcuts import render, Http404, HttpResponse, redirect
from django.contrib.auth import authenticate, login
from website.form import UserForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from website.models import UserProfile
from website.form import UserForm
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine
from django.contrib.auth.decorators import login_required
import sqlite3
import xlrd
import uuid


def df_to_sql_T_1(filefullpath, sheet, row_name):#路径名，sheet为sheet数，row_name为指定行为columns
    df = pd.read_excel(filefullpath, sheetname=sheet)#读取存在文件夹中的excel
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    df = df.T
    df.columns = df.loc[row_name]
    df = df.drop(row_name, axis=0, inplace=False)
    df.drop_duplicates(subset=['★机构全名'], inplace=True)

    con = sqlite3.connect(r"C:\Users\Administrator\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
    sql = "SELECT upload_company_form1.'★机构全名' FROM upload_company_form1"#!!!注意这个没有表格会出错
    data = pd.read_sql(sql, con)
    fund_name_list = data['★机构全名'].tolist()

    for name in df['★机构全名'].unique:
        df.loc['★机构全名' == name, 'UUID'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, name))
    for name in df['★机构全名'].unique():
        if name in fund_name_list:
            df.to_sql("upload_company_form1", con, if_exists="replace", index=False)
            print("if")
        else:
            df.to_sql("upload_company_form1", con, if_exists="append", index=False)
            print("else")
    print("to_sql")
def df_to_sql_T_2(filefullpath, sheet, row_name):#路径名，sheet为sheet数，row_name为指定行为columns
    df = pd.read_excel(filefullpath, sheetname=sheet)#读取存在文件夹中的excel
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    df = df.T
    df.columns = df.loc[row_name]
    df = df.drop(row_name, axis=0, inplace=False)
    df.drop_duplicates(subset=['★基金全称'], inplace=True)

    con = sqlite3.connect(r"C:\Users\Administrator\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
    sql = "SELECT upload_company_form2.'★基金全称' FROM upload_company_form2"#!!!注意这个没有表格会出错
    data = pd.read_sql(sql, con)
    fund_name_list = data['★基金全称'].tolist()

    for name in df['★基金全称'].unique:
        df.loc['★基金全称' == name, 'UUID'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, name))
    for name in df['★基金全称'].unique():
        if name in fund_name_list:
            df.to_sql("upload_company_form2", con, if_exists="replace", index=False)
            print("if")
        else:
            df.to_sql("upload_company_form2", con, if_exists="append", index=False)
            print("else")
    print("to_sql")
def df_to_sql_T_3(filefullpath, sheet, row_name):#路径名，sheet为sheet数，row_name为指定行为columns
    df = pd.read_excel(filefullpath, sheetname=sheet)#读取存在文件夹中的excel
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    df = df.T
    df.columns = df.loc[row_name]
    df = df.drop(row_name, axis=0, inplace=False)
    df.drop_duplicates(subset=['★姓名'], inplace=True)

    con = sqlite3.connect(r"C:\Users\Administrator\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
    sql = "SELECT upload_company_form3.'★姓名' FROM upload_company_form3"#!!!注意这个没有表格会出错
    data = pd.read_sql(sql, con)
    fund_name_list = data['★姓名'].tolist()

    for name in df['★姓名'].unique:
        df.loc['★姓名' == name, 'UUID'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, name))
    for name in df['★姓名'].unique():
        if name in fund_name_list:
            df.to_sql("upload_company_form3", con, if_exists="replace", index=False)
            print("if")
        else:
            df.to_sql("upload_company_form3", con, if_exists="append", index=False)
            print("else")
    print("to_sql")
def df_to_sql_4(filefullpath, sheet, row_name):#路径名，sheet为sheet数，row_name为指定行为columns
    df = pd.read_excel(filefullpath, sheetname=sheet)#读取存在文件夹中的excel
    df = df.dropna(how="all")
    df = df.dropna(axis=1, how="all")
    df = df.T
    df.drop_duplicates(subset=['基金简称'], inplace=True)

    con = sqlite3.connect(r"C:\Users\Administrator\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
    sql = "SELECT upload_company_form4.'★机构全名' FROM upload_company_form4"#!!!注意这个没有表格会出错
    data = pd.read_sql(sql, con)
    fund_name_list = data['基金简称'].tolist()

    for name in df['基金简称'].unique:
        df.loc['基金简称' == name, 'UUID'] = str(uuid.uuid3(uuid.NAMESPACE_DNS, name))
    for name in df['基金简称'].unique():
        if name in fund_name_list:
            df.to_sql("upload_company_form4", con, if_exists="replace", index=False)
            print("if")
        else:
            df.to_sql("upload_company_form4", con, if_exists="append", index=False)
            print("else")
    print("to_sql")


# def df_to_sql(filefullpath, sheet):
#     df = pd.read_excel(filefullpath, sheetname=sheet)
#     df = df.dropna(how="all")
#     df = df.dropna(axis=1, how="all")
#     print(df)
#     con = sqlite3.connect(r"C:\Users\Administrator\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
#     df.to_sql(str(sheet), con, if_exists="append")
#     print("tosql!")


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
            path = "C:\\Users\\Administrator\\Desktop\\excel-upload-sqlite3\\mins\\upload\\upload\\"
            filefullpath = path + file_name
            print(filefullpath)
            if user_upload_file:
                b = xlrd.open_workbook(filefullpath)
                #count = len(b.sheets())#不需要，sheet数都是固定的
                for sheet in range(1,5):
                    if sheet == 1:
                        row_name = "公司资料简介"
                        print(1)
                        df_to_sql_T_1(filefullpath, sheet, row_name)
                    if sheet == 2:
                        row_name = "基金简介"
                        print(2)
                        #df_to_sql_T(filefullpath, sheet)
                        df_to_sql_T_2(filefullpath, sheet, row_name)
                    if sheet == 3:
                        row_name = "人员简介"
                        print(3)
                        #df_to_sql_T(filefullpath, sheet)
                        df_to_sql_T_3(filefullpath, sheet, row_name)
                    if sheet == 4:
                        print(4)
                        df_to_sql_4(filefullpath, sheet)
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