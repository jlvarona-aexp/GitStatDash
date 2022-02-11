import dbConnection
import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
from datetime import datetime
import constant

is_anonymous = False

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "PR Metrics Dashboard"


def calculate_data():
    global dfCreator, dfReviewer, dfReviewerAll, dfRepos, dfTeams, dfBands, dfCreatorNames, dfReviewerNames, dfCreatorReport
    conn = dbConnection.getDBConnection()
    if is_anonymous:
        nameField = "u.nickname"
    else:
        nameField = "u.name"
    dfCreator = pd.read_sql_query(dbConnection.sqlCreatorsShort % nameField, conn)
    dfReviewer = pd.read_sql_query(dbConnection.sqlActivitiesDiffsShort % nameField, conn)
    dfReviewerAll = pd.read_sql_query(dbConnection.sqlActivitiesDiffsAll % nameField, conn)
    dfRepos = pd.read_sql_query(dbConnection.sqlRepos, conn)
    dfTeams = pd.read_sql_query(dbConnection.sqlTeams, conn)
    dfBands = pd.read_sql_query(dbConnection.sqlBand, conn)
    dfCreatorNames = pd.read_sql_query(dbConnection.sqlCreatorNames % nameField, conn)
    dfReviewerNames = pd.read_sql_query(dbConnection.sqlCommenterNames % nameField, conn)
    dfCreatorReport = pd.read_sql_query(dbConnection.sqlReportNames, conn)
    conn.close()


def format_date(x):
    if x:
        if "/" in x:
            mydate = datetime.strptime(x, "%m/%d/%y")
            return mydate.strftime("%Y-%m")
        else:
            return x[0:7]
    else:
        return ""


def format_week_date(x):
    if x:
        if "/" in x:
            mydate = datetime.strptime(x, "%m/%d/%y")
            return mydate.strftime("%Y-%U")
        else:
            mydate = datetime.strptime(x, "%Y-%m-%d")
            return mydate.strftime("%Y-%U")
    else:
        return ""


def top_records(ct):
    if ct.size > constant.MAX_RECORDS:
        sum_total = ct.sum(axis=0)
        ct = ct.head(constant.MAX_RECORDS)
        sum_head = ct.sum(axis=0)
        ct.loc['Others'] = sum_total.values - sum_head.values
    return ct


def filter_chart_data(df, user_role, bands, creators, repos, teams, years):
    if creators:
        boolean_series = df[user_role].isin(creators)
        df = df[boolean_series]
    if teams:
        boolean_series = df["Team"].isin(teams)
        df = df[boolean_series]
    if repos:
        boolean_series = df["Repo"].isin(repos)
        df = df[boolean_series]
    if bands:
        boolean_series = df["Band"].isin(bands)
        df = df[boolean_series]
    if years:
        boolean_series = df["Created_At"].str[0:4].isin(years)
        df = df[boolean_series]
    return df


def create_count_timeline_table(df):
    table = pd.pivot_table(df, values='id', index=['Created_At'],
                           columns=['Repo'], aggfunc=pd.Series.count)
    data = []
    for column in table.columns:
        data.append(
            go.Line(
                x=table[column].index,
                y=table[column].values,
                name=column
            )
        )
    figure = go.Figure(data=data)
    figure.update_yaxes(automargin=True, autorange=True)
    return figure


def create_average_timeline_table(df):
    table = pd.pivot_table(df, values='Duration', index=['Created_At'],
                           columns=['Repo'], aggfunc=np.mean)
    data = []
    for column in table.columns:
        data.append(
            go.Line(
                x=table[column].index,
                y=table[column].values,
                name=column
            )
        )
    figure = go.Figure(data=data)
    figure.update_yaxes(automargin=True, autorange=True)
    return figure


