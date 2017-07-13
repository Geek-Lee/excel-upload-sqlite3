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
    #读取存在文件夹中的excel
    excel_df = pd.read_excel(filefullpath, sheetname=sheet)
    excel_df = excel_df.dropna(how="all")
    excel_df = excel_df.dropna(axis=1, how="all")
    excel_df = excel_df.T
    excel_df.columns = excel_df.loc[row_name]
    excel_df = excel_df.drop(row_name, axis=0, inplace=False)
    excel_df.index = range(len(excel_df))
    excel_df.drop_duplicates(subset=['★机构全名'], inplace=True)
    print("excel_df")
    print(excel_df)
    print("excel_df")

    #数据库的读取
    con = sqlite3.connect(r"C:\Users\K\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
    sql = "SELECT * FROM org_info"#!!!注意这个没有表格会出错
    sql_df = pd.read_sql(sql, con)
    fund_name_list = sql_df['org_full_name'].tolist()
    print("fund_name_list")
    print(fund_name_list)
    sql_number = len(fund_name_list)
    print("sql_df")
    print(sql_df)
    print("sql_df")

    #依次对数据库中的每一行添加一列id
    org_id = 0
    for org_full_name in sql_df['org_full_name'].unique():
        org_id = org_id+1
        with con:
            cur = con.cursor()
            cur.execute("""UPDATE org_info SET org_id=? WHERE org_full_name=?""", (org_id, org_full_name))


    #对excel进行读取
    #excel_data = pd.read_excel(filefullpath, sheetname=sheet)
    excel_name_list = excel_df['★机构全名'].tolist()
    print("excel_name_list")
    print(excel_name_list)
    for name in excel_name_list:
        if name in fund_name_list:
            #提取数据库中的org_full_name为name的id
            con = sqlite3.connect(r"C:\Users\K\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
            sql = "SELECT * FROM org_info"
            sql_df = pd.read_sql(sql, con)
            name_dataframe =sql_df[sql_df["org_full_name"] == name]
            org_id = name_dataframe.loc[name_dataframe.last_valid_index(), 'org_id']

            #把excel的一行变成dataframe，并且加上id，并上传到数据库
            index = excel_df[excel_df["★机构全名"] == name]
            commit_data = pd.DataFrame(data=excel_df, index=[index.last_valid_index()], columns=sql_df.columns)
            commit_data.loc[index.last_valid_index(), "org_id"] = id

            #把一行表格dataframe提取其中的值
            org_name = str(commit_data.loc[index.last_valid_index(), "★机构简称"])
            org_full_name = str(commit_data.loc[index.last_valid_index(), "★机构全名"])
            reg_code = str(commit_data.loc[index.last_valid_index(), "★登记编号"])
            reg_time = str(commit_data.loc[index.last_valid_index(), "★登记时间"])
            found_date = str(commit_data.loc[index.last_valid_index(), "★机构成立日期"])
            reg_capital = str(commit_data.loc[index.last_valid_index(), "★注册资本"])
            real_capital = str(commit_data.loc[index.last_valid_index(), "★实缴资本"])
            region = str(commit_data.loc[index.last_valid_index(), "★地区"])
            profile = str(commit_data.loc[index.last_valid_index(), "★公司简介"])
            address = str(commit_data.loc[index.last_valid_index(), "★联系地址"])
            team = str(commit_data.loc[index.last_valid_index(), "★投研团队"])
            fund_num = str(commit_data.loc[index.last_valid_index(), "★已发行产品数量"])
            is_qualification = str(commit_data.loc[index.last_valid_index(), "是否具备投顾资格"])
            prize = str(commit_data.loc[index.last_valid_index(), "所获荣誉"])
            team_scale = str(commit_data.loc[index.last_valid_index(), "投研人员规模"])
            investment_idea = str(commit_data.loc[index.last_valid_index(), "投资理念"])
            master_strategy = str(commit_data.loc[index.last_valid_index(), "主要策略"])
            remark = str(commit_data.loc[index.last_valid_index(), "备注"])
            asset_mgt_scale = str(commit_data.loc[index.last_valid_index(), "★截至上月末管理产品规模（亿）"])
            linkman = str(commit_data.loc[index.last_valid_index(), "★联系人"])
            linkman_duty = str(commit_data.loc[index.last_valid_index(), "联系人职位"])
            linkman_phone = str(commit_data.loc[index.last_valid_index(), "★联系人电话"])
            linkman_email = str(commit_data.loc[index.last_valid_index(), "联系人邮箱"])
            with con:
                cur = con.cursor()
                sql = """UPDATE org_info SET org_name=?, org_full_name=?, reg_code=?, reg_time=?, found_date=?, \
                reg_capital=?, real_capital=?, region=?,profile=?, address=?, team=?, fund_num=?, is_qualification=?, \
                prize=?, team_scale=?, investment_idea=?, master_strategy=?, remark=?, asset_mgt_scale=?, linkman=?, \
                linkman_duty=?, linkman_phone=?, linkman_email=? WHERE org_id=?"""
                l = (org_name, org_full_name, reg_code, reg_time, found_date, reg_capital, real_capital, region, profile,\
                     address, team, fund_num, is_qualification, prize, team_scale, investment_idea, master_strategy, remark,\
                     asset_mgt_scale, linkman, linkman_duty, linkman_phone, linkman_email, org_id)
                cur.execute(sql, l)
            print("if")
        else:
            sql_number = sql_number + 1
            print(sql_number)
            index = excel_df[excel_df["★机构全名"] == name]
            commit_data = pd.DataFrame(data=excel_df, index=[index.last_valid_index()], columns=sql_df.columns)
            commit_data.loc[index.last_valid_index(), "org_id"] = str(sql_number)
            commit_data.to_sql("org_info", con, if_exists="append", index=False)
            print("else")


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
            path = "C:\\Users\\K\\Desktop\\excel-upload-sqlite3\\mins\\upload\\upload\\"
            #C:\Users\K\Desktop\excel - upload - sqlite3\excel - upload - sqlite3\mins\upload\upload\华泰大赛参赛私募基金数据填报模板.xlsx
            filefullpath = path + file_name
            #print(filefullpath)
            if user_upload_file:
                b = xlrd.open_workbook(filefullpath)
                #count = len(b.sheets())#不需要，sheet数都是固定的
                for sheet in range(1, 5):
                    if sheet == 1:
                        row_name = "公司资料简介"
                        print(1)
                        df_to_sql_T_1(filefullpath, sheet, row_name)
                    if sheet == 2:
                        pass
                    if sheet == 3:
                        pass
                    if sheet == 4:
                        pass
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