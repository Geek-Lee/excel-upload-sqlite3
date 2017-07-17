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

    #数据库的读取
    con = sqlite3.connect(r"C:\Users\K\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
    sql = "SELECT * FROM org_info"#!!!注意sql中没有表格会出错
    sql_df = pd.read_sql(sql, con)
    fund_name_list = sql_df['org_full_name'].tolist()
    sql_number = len(fund_name_list)


    #依次对数据库中的每一行添加一列id
    org_id_number = 0
    for org_full_name in sql_df['org_full_name'].unique():
        org_id_number = org_id_number+1
        org_id = 'O'+'0'*(5-len(str(org_id_number)))+str(org_id_number)
        with con:
            cur = con.cursor()
            cur.execute("""UPDATE org_info SET org_id=? WHERE org_full_name=?""", (org_id, org_full_name))


    #对excel进行读取
    #excel_data = pd.read_excel(filefullpath, sheetname=sheet)
    excel_name_list = excel_df['★机构全名'].tolist()
    for name in excel_name_list:
        if name in fund_name_list:
            #提取数据库中的org_full_name为name的id
            con = sqlite3.connect(r"C:\Users\K\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
            sql = "SELECT * FROM org_info"
            sql_df = pd.read_sql(sql, con)
            name_dataframe =sql_df[sql_df["org_full_name"] == name]
            org_id = name_dataframe.loc[name_dataframe.last_valid_index(), 'org_id']

            #把excel的一行变成dataframe，并且加上id，并上传到数据库
            commit_data = excel_df[excel_df["★机构全名"] == name]
            commit_data.columns = ["org_name", "org_full_name", "reg_code", "reg_time", "found_date", "reg_capital",
                                   "real_capital", "region", "profile", "address", "team", "fund_num",
                                   "is_qualification", "prize", "team_scale", "investment_idea", "master_strategy",
                                   "remark", "asset_mgt_scale", "linkman", "linkman_duty", "linkman_phone",
                                   "linkman_email"]
            commit_data["org_id"] = str(org_id)

            #把一行表格dataframe提取其中的值
            org_name = str(commit_data.loc[commit_data.org_full_name == name, 'org_name'].values[0])
            org_full_name = str(name)
            reg_code = str(commit_data.loc[commit_data.org_full_name == name, 'reg_code'].values[0])
            reg_time = str(commit_data.loc[commit_data.org_full_name == name, 'reg_time'].values[0])
            found_date = str(commit_data.loc[commit_data.org_full_name == name, 'found_date'].values[0])
            reg_capital = str(commit_data.loc[commit_data.org_full_name == name, 'reg_capital'].values[0])
            real_capital = str(commit_data.loc[commit_data.org_full_name == name, 'real_capital'].values[0])
            region = str(commit_data.loc[commit_data.org_full_name == name, 'region'].values[0])
            profile = str(commit_data.loc[commit_data.org_full_name == name, 'profile'].values[0])
            address = str(commit_data.loc[commit_data.org_full_name == name, 'address'].values[0])
            team = str(commit_data.loc[commit_data.org_full_name == name, 'org_name'].values[0])
            fund_num = str(commit_data.loc[commit_data.org_full_name == name, 'team'].values[0])
            is_qualification = str(commit_data.loc[commit_data.org_full_name == name, 'is_qualification'].values[0])
            prize = str(commit_data.loc[commit_data.org_full_name == name, 'prize'].values[0])
            team_scale = str(commit_data.loc[commit_data.org_full_name == name, 'team_scale'])
            investment_idea = str(commit_data.loc[commit_data.org_full_name == name, 'investment_idea'].values[0])
            master_strategy = str(commit_data.loc[commit_data.org_full_name == name, 'master_strategy'].values[0])
            remark = str(commit_data.loc[commit_data.org_full_name == name, 'remark'].values[0])
            asset_mgt_scale = str(commit_data.loc[commit_data.org_full_name == name, 'asset_mgt_scale'].values[0])
            linkman = str(commit_data.loc[commit_data.org_full_name == name, 'linkman'].values[0])
            linkman_duty = str(commit_data.loc[commit_data.org_full_name == name, 'linkman_duty'].values[0])
            linkman_phone = str(commit_data.loc[commit_data.org_full_name == name, 'linkman_phone'].values[0])
            linkman_email = str(commit_data.loc[commit_data.org_full_name == name, 'linkman_email'].values[0])
            # org_name = str(commit_data.loc[index.last_valid_index(), "org_name"])

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
            commit_data = excel_df[excel_df["★机构全名"] == name]
            commit_data.columns = ["org_name", "org_full_name", "reg_code", "reg_time", "found_date", "reg_capital",
                                   "real_capital", "region", "profile", "address", "team", "fund_num",
                                   "is_qualification", "prize", "team_scale", "investment_idea", "master_strategy",
                                   "remark", "asset_mgt_scale", "linkman", "linkman_duty", "linkman_phone",
                                   "linkman_email"]
            commit_data.loc[:, "org_id"] = 'O'+'0'*(5-len(str(sql_number)))+str(sql_number)
            commit_data.to_sql("org_info", con, if_exists="append", index=False)
            print("else")

def df_to_sql_T_2(filefullpath, sheet, row_name):#路径名，sheet为sheet数，row_name为指定行为columns
    #读取存在文件夹中的excel
    excel_df = pd.read_excel(filefullpath, sheetname=sheet)
    excel_df = excel_df.dropna(how="all")
    excel_df = excel_df.dropna(axis=1, how="all")
    excel_df = excel_df.T
    excel_df.columns = excel_df.loc[row_name]
    excel_df = excel_df.drop(row_name, axis=0, inplace=False)
    excel_df.index = range(len(excel_df))
    excel_df.drop_duplicates(subset=['★基金全称'], inplace=True)

    #数据库的读取
    con = sqlite3.connect(r"C:\Users\K\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
    sql = "SELECT * FROM fund_info"#!!!注意sql中没有表格会出错
    sql_df = pd.read_sql(sql, con)
    fund_name_list = sql_df['fund_full_name'].tolist()#list
    sql_number = len(fund_name_list)


    #依次对数据库中的每一行添加一列id
    fund_id_number = 0
    for fund_full_name in sql_df['fund_full_name'].unique():
        fund_id_number = fund_id_number+1
        fund_id = 'F'+'0'*(6-len(str(fund_id_number)))+str(fund_id_number)
        with con:
            cur = con.cursor()
            cur.execute("""UPDATE fund_info SET fund_id=? WHERE fund_full_name=?""", (fund_id, fund_full_name))


    #对excel进行读取
    #excel_data = pd.read_excel(filefullpath, sheetname=sheet)
    excel_name_list = excel_df['★基金全称'].tolist()#list
    for name in excel_name_list:
        if name in fund_name_list:
            #提取数据库中的org_full_name为name的id
            con = sqlite3.connect(r"C:\Users\K\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
            sql = "SELECT * FROM fund_info"
            sql_df = pd.read_sql(sql, con)
            name_dataframe =sql_df[sql_df["fund_full_name"] == name]
            fund_id = name_dataframe.loc[name_dataframe.last_valid_index(), 'fund_id']

            #把excel的一行变成dataframe，并且加上id，并上传到数据库
            commit_data = excel_df[excel_df["★基金全称"] == name]
            commit_data.columns = ["group", "fund_type_strategy", "reg_code", "foundation_date", "fund_name",
                                   "fund_full_name", "fund_manager", "fund_manager_nominal", "fund_stockbroker",
                                   "fund_custodian", "fund_member", "fund_type_issuance", "fund_type_structure",
                                   "fund_structure", "issue_scale", "asset_scale", "is_main_fund", "fee_pay",
                                   "open_date", "locked_time_limit", "duration", "fee_manage", "fee_pay_remark",
                                   "fee_redeem", "fee_subscription", "fee_trust", "investment_range",
                                   "min_purchase_amount", "min_append_amount", "stop_line", "alert_line",
                                   "manager_participation_scale", "investment_idea", "structure_hierarchy", "remark"]
            commit_data["fund_id"] = str(fund_id)

            #把一行表格dataframe提取其中的值
            group = str(commit_data.loc[commit_data.fund_full_name == name, 'group'].values[0])
            fund_type_strategy = str(commit_data.loc[commit_data.fund_full_name == name, 'fund_type_strategy'].values[0])
            reg_code = str(commit_data.loc[commit_data.fund_full_name == name, 'reg_code'].values[0])
            foundation_date = str(commit_data.loc[commit_data.fund_full_name == name, 'foundation_date'].values[0])
            fund_name = str(commit_data.loc[commit_data.fund_full_name == name, 'fund_name'].values[0])
            fund_full_name = str(name)
            fund_manager = str(commit_data.loc[commit_data.fund_full_name == name, 'fund_manager'].values[0])
            fund_manager_nominal = str(commit_data.loc[commit_data.fund_full_name == name, 'fund_manager_nominal'].values[0])
            fund_stockbroker = str(commit_data.loc[commit_data.fund_full_name == name, 'fund_stockbroker'].values[0])
            fund_custodian = str(commit_data.loc[commit_data.fund_full_name == name, 'fund_custodian'].values[0])
            fund_member = str(commit_data.loc[commit_data.fund_full_name == name, 'fund_member'].values[0])
            fund_type_issuance = str(commit_data.loc[commit_data.fund_full_name == name, 'fund_type_issuance'].values[0])
            fund_type_structure = str(commit_data.loc[commit_data.fund_full_name == name, 'fund_type_structure'].values[0])
            fund_structure = str(commit_data.loc[commit_data.fund_full_name == name, 'fund_structure'].values[0])
            issue_scale = str(commit_data.loc[commit_data.fund_full_name == name, 'issue_scale'].values[0])
            asset_scale = str(commit_data.loc[commit_data.fund_full_name == name, 'asset_scale'].values[0])
            is_main_fund = str(commit_data.loc[commit_data.fund_full_name == name, 'is_main_fund'].values[0])
            fee_pay = str(commit_data.loc[commit_data.fund_full_name == name, 'fee_pay'].values[0])
            open_date = str(commit_data.loc[commit_data.fund_full_name == name, 'open_date'])
            locked_time_limit = str(commit_data.loc[commit_data.fund_full_name == name, 'locked_time_limit'].values[0])
            duration = str(commit_data.loc[commit_data.fund_full_name == name, 'duration'].values[0])
            fee_manage = str(commit_data.loc[commit_data.fund_full_name == name, 'fee_manage'].values[0])
            fee_pay_remark = str(commit_data.loc[commit_data.fund_full_name == name, 'fee_pay_remark'].values[0])
            fee_redeem = str(commit_data.loc[commit_data.fund_full_name == name, 'fee_redeem'].values[0])
            fee_subscription = str(commit_data.loc[commit_data.fund_full_name == name, 'fee_subscription'].values[0])
            fee_trust = str(commit_data.loc[commit_data.fund_full_name == name, 'fee_trust'].values[0])
            investment_range = str(commit_data.loc[commit_data.fund_full_name == name, 'investment_range'].values[0])
            min_purchase_amount = str(commit_data.loc[commit_data.fund_full_name == name, 'min_purchase_amount'].values[0])
            min_append_amount = str(commit_data.loc[commit_data.fund_full_name == name, 'min_append_amount'].values[0])
            stop_line = str(commit_data.loc[commit_data.fund_full_name == name, 'stop_line'].values[0])
            alert_line = str(commit_data.loc[commit_data.fund_full_name == name, 'alert_line'].values[0])
            manager_participation_scale = str(commit_data.loc[commit_data.fund_full_name == name, 'manager_participation_scale'].values[0])
            investment_idea = str(commit_data.loc[commit_data.fund_full_name == name, 'investment_idea'].values[0])
            structure_hierarchy = str(commit_data.loc[commit_data.fund_full_name == name, 'structure_hierarchy'].values[0])
            remark = str(commit_data.loc[commit_data.fund_full_name == name, 'remark'].values[0])

            with con:
                cur = con.cursor()
                sql = """UPDATE fund_info SET 'group'=?, fund_type_strategy=?, reg_code=?, foundation_date=?, fund_name=?,\
                fund_full_name=?, fund_manager=?, fund_manager_nominal=?, fund_stockbroker=?, fund_custodian=?, fund_member=?,\
                fund_type_issuance=?, fund_type_structure=?, fund_structure=?, issue_scale=?, asset_scale=?, is_main_fund=?, fee_pay=?,\
                open_date=?, locked_time_limit=?, duration=?, fee_manage=?, fee_pay_remark=?, fee_redeem=?, fee_subscription=?, fee_trust=?,\
                investment_range=?, min_purchase_amount=?, min_append_amount=?, stop_line=?, alert_line=?, manager_participation_scale=?, \
                investment_idea=?, structure_hierarchy=?, remark=? WHERE fund_id=?"""
                l = (group, fund_type_strategy, reg_code, foundation_date, fund_name, fund_full_name, fund_manager, \
                     fund_manager_nominal, fund_stockbroker, fund_custodian, fund_member, fund_type_issuance, \
                     fund_type_structure, fund_structure, issue_scale, asset_scale, is_main_fund, fee_pay, open_date, \
                     locked_time_limit, duration, fee_manage, fee_pay_remark, fee_redeem, fee_subscription, fee_trust, \
                     investment_range, min_purchase_amount, min_append_amount, stop_line, alert_line, manager_participation_scale, \
                     investment_idea, structure_hierarchy, remark, fund_id)
                cur.execute(sql, l)
            print("if")
        else:
            sql_number = sql_number + 1
            commit_data = excel_df[excel_df["★基金全称"] == name]
            commit_data.columns = ["group", "fund_type_strategy", "reg_code", "foundation_date", "fund_name", "fund_full_name", \
                                   "fund_manager", "fund_manager_nominal", "fund_stockbroker", "fund_custodian", "fund_member", \
                                   "fund_type_issuance", "fund_type_structure", "fund_structure", "issue_scale", "asset_scale", \
                                   "is_main_fund", "fee_pay", "open_date", "locked_time_limit", "duration", "fee_manage", \
                                   "fee_pay_remark", "fee_redeem", "fee_subscription", "fee_trust", "investment_range", \
                                   "min_purchase_amount", "min_append_amount", "stop_line", "alert_line", "manager_participation_scale", \
                                   "investment_idea", "structure_hierarchy", "remark"]
            commit_data.loc[:, "fund_id"] = 'F'+'0'*(6-len(str(sql_number)))+str(sql_number)
            commit_data.to_sql("fund_info", con, if_exists="append", index=False)
            print("else")

def df_to_sql_T_3(filefullpath, sheet, row_name):#路径名，sheet为sheet数，row_name为指定行为columns
    #读取存在文件夹中的excel
    excel_df = pd.read_excel(filefullpath, sheetname=sheet)
    excel_df = excel_df.dropna(how="all")
    excel_df = excel_df.dropna(axis=1, how="all")
    excel_df = excel_df.T
    excel_df.columns = excel_df.loc[row_name]#把【人员简介】的这一行变成columns这一列
    excel_df = excel_df.drop(row_name, axis=0, inplace=False)#去除【人员简介】这一行
    excel_df.index = range(len(excel_df))
    excel_df.drop_duplicates(subset=['★姓名'], inplace=True)

    #数据库的读取
    con = sqlite3.connect(r"C:\Users\K\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
    sql = "SELECT * FROM manager_info"#!!!注意sql中没有表格会出错
    sql_df = pd.read_sql(sql, con)
    user_list = sql_df['user_name'].tolist()#list
    sql_number = len(user_list)


    #依次对数据库中的每一行添加一列id
    user_id_number = 0
    for user_name in sql_df['user_name'].unique():
        user_id_number = user_id_number+1
        user_id = 'M'+'0'*(5-len(str(user_id_number)))+str(user_id_number)
        with con:
            cur = con.cursor()
            cur.execute("""UPDATE manager_info SET user_id=? WHERE user_name=?""", (user_id, user_name))


    #对excel进行读取
    #excel_data = pd.read_excel(filefullpath, sheetname=sheet)
    excel_name_list = excel_df['★姓名'].tolist()#list
    for name in excel_name_list:
        if name in user_list:
            #提取数据库中的user_name为name的id
            con = sqlite3.connect(r"C:\Users\K\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
            sql = "SELECT * FROM manager_info"
            sql_df = pd.read_sql(sql, con)
            name_dataframe =sql_df[sql_df["user_name"] == name]
            user_id = name_dataframe.loc[name_dataframe.last_valid_index(), 'user_id']#loc到最后一个有效的index和fund_id，取出值

            #把excel的一行变成dataframe，并且加上id，并上传到数据库
            commit_data = excel_df[excel_df["★姓名"] == name]
            commit_data.columns = ["user_name", "sex", "org_name", "introduction", "photo", "entry_date",
                                   "investment_years", "education", "duty", "qualification", "background", "is_fund_qualification",
                                   "is_core_member", "resume", "max_asset_mgt_scale", "prize", "remark"]
            commit_data["user_id"] = str(user_id)#不需要

            #把一行表格dataframe提取其中的值
            user_name = str(name)
            sex = str(commit_data.loc[commit_data.user_name == name, 'sex'].values[0])
            org_name = str(commit_data.loc[commit_data.user_name == name, 'org_name'].values[0])
            introduction = str(commit_data.loc[commit_data.user_name == name, 'introduction'].values[0])
            photo = str(commit_data.loc[commit_data.user_name == name, 'photo'].values[0])
            entry_date = str(commit_data.loc[commit_data.user_name == name, 'entry_date'].values[0])
            investment_years = str(commit_data.loc[commit_data.user_name == name, 'investment_years'].values[0])
            education = str(commit_data.loc[commit_data.user_name == name, 'education'].values[0])
            duty = str(commit_data.loc[commit_data.user_name == name, 'duty'].values[0])
            qualification = str(commit_data.loc[commit_data.user_name == name, 'qualification'].values[0])
            background = str(commit_data.loc[commit_data.user_name == name, 'background'].values[0])
            is_fund_qualification = str(commit_data.loc[commit_data.user_name == name, 'is_fund_qualification'].values[0])
            is_core_member = str(commit_data.loc[commit_data.user_name == name, 'is_core_member'].values[0])
            resume = str(commit_data.loc[commit_data.user_name == name, 'resume'].values[0])
            max_asset_mgt_scale = str(commit_data.loc[commit_data.user_name == name, 'max_asset_mgt_scale'].values[0])
            prize = str(commit_data.loc[commit_data.user_name == name, 'prize'].values[0])
            remark = str(commit_data.loc[commit_data.user_name == name, 'remark'].values[0])

            with con:
                cur = con.cursor()
                sql = """UPDATE manager_info SET user_name=?, sex=?, org_name=?, introduction=?, photo=?, \
                entry_date=?, investment_years=?, education=?, duty=?, qualification=?, background=?, is_fund_qualification=?, \
                is_core_member=?, resume=?, max_asset_mgt_scale=?, prize=?, remark=? WHERE user_id=?"""
                l = (user_name, sex, org_name, introduction, photo, entry_date, investment_years, education, \
                     duty, qualification, background, is_fund_qualification, is_core_member, resume, max_asset_mgt_scale, \
                     prize, remark, user_id)
                cur.execute(sql, l)
            print("if")
        else:
            sql_number = sql_number + 1
            commit_data = excel_df[excel_df["★姓名"] == name]
            commit_data.columns = ["user_name", "sex", "org_name", "introduction", "photo", "entry_date", \
                                   "investment_years", "education", "duty", "qualification", "background", \
                                   "is_fund_qualification", "is_core_member", "resume", "max_asset_mgt_scale", "prize", \
                                   "remark"]
            commit_data.loc[:, "user_id"] = 'M'+'0'*(5-len(str(sql_number)))+str(sql_number)
            commit_data.to_sql("manager_info", con, if_exists="append", index=False)
            print("else")

def df_to_sql_4(filefullpath, sheet, row_name):#路径名，sheet为sheet数，row_name为指定行为columns
    #读取存在文件夹中的excel
    excel_df = pd.read_excel(filefullpath, sheetname=sheet)
    excel_df = excel_df.dropna(how="all")
    excel_df = excel_df.dropna(axis=1, how="all")
    #excel_df.columns = excel_df.loc[row_name]#把【基金简称】的这一行变成columns这一列
    #excel_df = excel_df.drop(row_name, axis=0, inplace=False)#去除【基金简称】这一行
    excel_df.index = range(len(excel_df))
    excel_df.drop_duplicates(subset=['基金简称'], inplace=True)

    #数据库的读取
    con = sqlite3.connect(r"C:\Users\K\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
    sql = "SELECT * FROM fund_nav_data"#!!!注意sql中没有表格会出错
    sql_df = pd.read_sql(sql, con)
    user_list = sql_df['fund_name'].tolist()#list
    sql_number = len(user_list)


    #依次对数据库中的每一行添加一列id
    fund_id_number = 0
    for fund_name in sql_df['fund_name'].unique():
        fund_id_number = fund_id_number+1
        fund_id = 'F'+'0'*(6-len(str(fund_id_number)))+str(fund_id_number)
        with con:
            cur = con.cursor()
            cur.execute("""UPDATE fund_nav_data SET fund_id=? WHERE fund_name=?""", (fund_id, fund_name))


    #对excel进行读取
    #excel_data = pd.read_excel(filefullpath, sheetname=sheet)
    excel_name_list = excel_df['基金简称'].tolist()#list
    for name in excel_name_list:
        if name in user_list:
            #提取数据库中的user_name为name的id
            con = sqlite3.connect(r"C:\Users\K\Desktop\excel-upload-sqlite3\mins\db.sqlite3")
            sql = "SELECT * FROM fund_nav_data"
            sql_df = pd.read_sql(sql, con)
            name_dataframe =sql_df[sql_df["fund_name"] == name]
            user_id = name_dataframe.loc[name_dataframe.last_valid_index(), 'fund_id']#loc到最后一个有效的index和fund_id，取出值

            #把excel的一行变成dataframe，并且加上id，并上传到数据库
            commit_data = excel_df[excel_df["基金简称"] == name]
            commit_data.columns = ["fund_name", "statistic_date", "nav", "added_nav", "total_share", "total_asset",
                                   "total_nav", "is_split", "is_open_date", "split_ratio", "after_tax_bonus"]
            commit_data["fund_id"] = str(fund_id)#不需要

            #把一行表格dataframe提取其中的值
            fund_name = str(name)
            statistic_date = str(commit_data.loc[commit_data.fund_name == name, 'statistic_date'].values[0])
            nav = str(commit_data.loc[commit_data.fund_name == name, 'nav'].values[0])
            added_nav = str(commit_data.loc[commit_data.fund_name == name, 'added_nav'].values[0])
            total_share = str(commit_data.loc[commit_data.fund_name == name, 'total_share'].values[0])
            total_asset = str(commit_data.loc[commit_data.fund_name == name, 'total_asset'].values[0])
            total_nav = str(commit_data.loc[commit_data.fund_name == name, 'total_nav'].values[0])
            is_split = str(commit_data.loc[commit_data.fund_name == name, 'is_split'].values[0])
            is_open_date = str(commit_data.loc[commit_data.fund_name == name, 'is_open_date'].values[0])
            split_ratio = str(commit_data.loc[commit_data.fund_name == name, 'split_ratio'].values[0])
            after_tax_bonus = str(commit_data.loc[commit_data.fund_name == name, 'after_tax_bonus'].values[0])

            with con:
                cur = con.cursor()
                sql = """UPDATE fund_nav_data SET fund_name=?, statistic_date=?, nav=?, added_nav=?, total_share=?, total_asset=?, total_nav=?, is_split=?, is_open_date=?, split_ratio=?, after_tax_bonus=? WHERE fund_id=?"""
                l = (fund_name, statistic_date, nav, added_nav, total_share, total_asset, total_nav, is_split, is_open_date, split_ratio, after_tax_bonus, fund_id)
                cur.execute(sql, l)
            print("if")
        else:
            sql_number = sql_number + 1
            commit_data = excel_df[excel_df["基金简称"] == name]
            commit_data.columns = ["fund_name", "statistic_date", "nav", "added_nav", "total_share", "total_asset",
                                   "total_nav", "is_split", "is_open_date", "split_ratio", "after_tax_bonus"]
            commit_data.loc[:, "fund_id"] = 'F'+'0'*(6-len(str(sql_number)))+str(sql_number)
            commit_data.to_sql("fund_nav_data", con, if_exists="append", index=False)
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
                        pass
                        #row_name = "公司资料简介"
                        #df_to_sql_T_1(filefullpath, sheet, row_name)
                    if sheet == 2:
                        pass
                        #row_name = "基金简介"
                        #df_to_sql_T_2(filefullpath, sheet, row_name)
                    if sheet == 3:
                        pass
                        #row_name = "人员简介"
                        #df_to_sql_T_3(filefullpath, sheet, row_name)
                    if sheet == 4:
                        row_name = "基金简称"
                        df_to_sql_4(filefullpath, sheet, row_name)
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