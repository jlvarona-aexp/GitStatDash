from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import html, dcc, Output, Input
from flask import Flask

import constant
import dbConnection
import pandas as pd
import plotly.graph_objs as go


def calculate_data():
    global dfCreator, dfReviewer, dfRepos, dfTeams, dfBands, dfCreatorNames, dfReviewerNames
    conn = dbConnection.getDBConnection()
    dfCreator = pd.read_sql_query(dbConnection.sqlCreatorsShort, conn)
    dfReviewer = pd.read_sql_query(dbConnection.sqlActivitiesDiffsShort, conn)
    dfRepos = pd.read_sql_query(dbConnection.sqlRepos, conn)
    dfTeams = pd.read_sql_query(dbConnection.sqlTeams, conn)
    dfBands = pd.read_sql_query(dbConnection.sqlBand, conn)
    dfCreatorNames = pd.read_sql_query(dbConnection.sqlCreatorNames, conn)
    dfReviewerNames = pd.read_sql_query(dbConnection.sqlCommenterNames, conn)
    conn.close()


calculate_data()

#server = Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
#app.title("PR Metrics Dashboard")

SIDEBAR_STYLE = {
    # "position": "fixed",
    # "top": 0,
    # "left": 0,
    # "bottom": 0,
    # "width": "16rem",
    "height": "100%",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
CONTENT_STYLE = {
    # "margin-left": "18rem",
    # "margin-right": "2rem",
    # "padding": "2rem 1rem",
    "widht": "100%",
    "height": "100%",
}
creator_dd = html.Div([
    html.P(),
    html.Label(
        "Developer", className="lead"
    ),
    dcc.Dropdown(
        id="creator-dropdown",
        options=[
            {'label': x,
             'value': x
             } for x in dfCreatorNames["Creator Name"].array
        ],
        multi=True),
]
    , className="dash-bootstrap")

reviewer_dd = html.Div([
    html.P(),
    html.Label(
        "Reviewer", className="lead"
    ),
    dcc.Dropdown(
        id="reviewer-dropdown",
        options=[
            {'label': x,
             'value': x
             } for x in dfReviewerNames["Reviewer Name"].array
        ],
        multi=True)
], className="dash-bootstrap")
band_dd = html.Div([
    html.P(),
    html.Label(
        "Band", className="lead"
    ),
    dcc.Dropdown(
        id="band-dropdown",
        options=[
            {'label': x,
             'value': x} for x in dfBands["Band"].array
        ],
        multi=True)], className="dash-bootstrap")
repo_dd = html.Div([
    html.P(),
    html.Label(
        "Repo", className="lead"
    ),
    dcc.Dropdown(
        id="repo-dropdown",
        options=[
            {'label': x,
             'value': x} for x in dfRepos["Repo"].array
        ],
        multi=True)], className="dash-bootstrap")
team_dd = html.Div([
    html.P(),
    html.Label(
        "Team", className="lead"
    ),
    dcc.Dropdown(
        id="team-dropdown",
        options=[
            {'label': x,
             'value': x} for x in dfTeams["Team"].array
        ],
        multi=True)], className="dash-bootstrap")
year_dd = html.Div([
    html.P(),
    html.Label(
        "Year", className="lead"
    ),
    dcc.Dropdown(
        id="year-dropdown",
        options=[
            {'label': x,
             'value': x} for x in ["2020", "2021", "2022", "2023", "2024"]
        ],
        multi=True)], className="dash-bootstrap")

sidebar = html.Div(
    [
        html.H2("PR Metrics", className="display-4"),
        html.Hr(),
        html.P(
            "Select the criteria to filter the charts", className="lead"
        ),
        creator_dd,
        team_dd,
        repo_dd,
        band_dd,
        year_dd,
        html.Hr(),
        dbc.Button("Refresh Data", id="refresh-button", className="me-3", href="/")
    ],
    style=SIDEBAR_STYLE
)

creator_charts = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(f"PR Count by Developer, Top {constant.MAX_RECORDS}"),
                        dcc.Graph(id="pie-creator-count")
                    ], md=6),

                dbc.Col(
                    [
                        html.Label("Average PR Duration (in Days)"),
                        dcc.Graph(id="pie-creator-duration")
                    ], md=6),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("PR Creation Count Over Time"),
                        dcc.Graph(id="timeline-creator")
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("PR Creation Average Over Time"),
                        dcc.Graph(id="timeline-creator-average")
                    ]
                )
            ]
        )
    ]
)

creator_content = html.Div(creator_charts, id="creator-page-content", style=CONTENT_STYLE)

reviewer_charts = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(f"Review Count by Developer. Top {constant.MAX_RECORDS}"),
                        dcc.Graph(id="pie-reviewer-count")
                    ], md=6),
                dbc.Col(
                    [
                        html.Label("Average Time to First Review (in Days)"),
                        dcc.Graph(id="pie-reviewer-duration")
                    ], md=6),
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Label("Review Contributions Count Over Time"),
                    dcc.Graph(id="timeline-reviewer")
                ])
        )
    ]
)

reviewer_content = html.Div(reviewer_charts, id="reviewer-page-content", style=CONTENT_STYLE)

creator_count_charts = html.Div(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.Label(f"PR Count by Developer, Top {constant.MAX_RECORDS}"),
                    dcc.Graph(id="pie-creator-count")
                ]
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Label(f"PR Count by Developer, Bottom {constant.MAX_RECORDS}"),
                    dcc.Graph(id="pie-creator-count-bottom")
                ]
            )
        )
    ]
)

creator_count_content = html.Div(creator_count_charts, id="creator-count-content", style=CONTENT_STYLE)

reviewer_count_charts = html.Div(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.Label(f"Review Count by Developer, Top {constant.MAX_RECORDS}"),
                    dcc.Graph(id="pie-reviewer-count")
                ]
            )
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Label(f"Review Count by Developer, Bottom {constant.MAX_RECORDS}"),
                    dcc.Graph(id="pie-reviewer-count-bottom")
                ]
            )
        )
    ]
)

reviewer_count_content = html.Div(reviewer_count_charts, id="creator-count-content", style=CONTENT_STYLE)

tabLayout = dbc.Container(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Creator", tab_id="creator-tab"),
                dbc.Tab(label="Creator Count", tab_id="creator-count-tab"),
                dbc.Tab(label="Reviewer", tab_id="reviewer-tab"),
                dbc.Tab(label="Reviewer Count", tab_id="reviewer-count-tab"),
            ],
            id="tabs",
            active_tab="creator-tab",
        ),
        html.Div(id="tab-content", className="w-100 h-100 p-4"),
    ],
    fluid=True
)

mainLayout = dbc.Container(
    [
        dcc.Store(id="store"),
        dbc.Row([
            dbc.Col(sidebar, width=2),
            dbc.Col(tabLayout, width=10)
        ]
        )
    ],
    fluid=True
)

app.layout = mainLayout


def format_date(x):
    if x:
        if "/" in x:
            mydate = datetime.strptime(x, "%m/%d/%y")
            return mydate.strftime("%Y-%m")
        else:
            return x[0:7]
    else:
        return ""


@app.callback(
    Output("store", "data"),
    [
        Input("refresh-button", "n_clicks"),
    ]
)
def on_button_click(n):
    calculate_data()
    return {}


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    #    if active_tab and data is not None:
    if active_tab == "creator-tab":
        return creator_content
    elif active_tab == "creator-count-tab":
        return creator_count_content
    elif active_tab == "reviewer-tab":
        return reviewer_content
    elif active_tab == "reviewer-count-tab":
        return reviewer_count_content


#    return "No tab selected"


@app.callback(
    Output("pie-creator-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
    ]
)
def creator_count_graph(creators, teams, repos, bands, years):
    df = dfCreator
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    ct = df.groupby("Creator").agg({"id": "count"}).sort_values(["id"], ascending=False)
    ct = top_records(ct)
    data = [
        go.Pie(
            labels=ct["id"].index,
            values=ct["id"].values
        )
    ]
    fig = go.Figure(data=data)
    fig.update_layout(autosize=True, margin=dict(t=0, b=0, l=0, r=0))
    return fig


@app.callback(
    Output("pie-creator-count-bottom", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
    ]
)
def creator_count_bottom_graph(creators, teams, repos, bands, years):
    df = dfCreator
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    ct = df.groupby("Creator").agg({"id": "count"}).sort_values(["id"], ascending=True).head(constant.MAX_RECORDS)
    data = [
        go.Pie(
            labels=ct["id"].index,
            values=ct["id"].values,
        )
    ]
    fig = go.Figure(data=data)
    fig.update_layout(autosize=True, margin=dict(t=0, b=0, l=0, r=0))
    return fig


@app.callback(
    Output("pie-creator-duration", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),

    ]
)
def creator_duration_graph(creators, teams, repos, bands, years):
    df = dfCreator
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    ct = df.groupby("Creator").agg({"Duration": "mean"})
    data = [
        go.Bar(
            x=ct["Duration"].index,
            y=ct["Duration"].values
        )
    ]
    return go.Figure(data=data)


@app.callback(
    Output("timeline-creator", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),

    ]
)
def timeline_creator_graph(creators, teams, repos, bands, years):
    df = dfCreator
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    return create_count_timeline_table(df)


@app.callback(
    Output("timeline-creator-average", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),

    ]
)
def timeline_creator_average_graph(creators, teams, repos, bands, years):
    df = dfCreator
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    return create_average_timeline_table(df)


@app.callback(
    Output("pie-reviewer-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),

    ]
)
def reviewer_count_graph(creators, teams, repos, bands, years):
    df = dfReviewer
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Reviewer", bands, creators, repos, teams, years)
    ct = df.groupby("Reviewer").agg({"id": "count"}).sort_values(["id"], ascending=False)
    ct = top_records(ct)
    data = [
        go.Pie(
            labels=ct["id"].index,
            values=ct["id"].values
        )
    ]
    return go.Figure(data=data)


@app.callback(
    Output("pie-reviewer-count-bottom", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),

    ]
)
def reviewer_count_bottom_graph(creators, teams, repos, bands, years):
    df = dfReviewer
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Reviewer", bands, creators, repos, teams, years)
    ct = df.groupby("Reviewer").agg({"id": "count"}).sort_values(["id"], ascending=True).head(constant.MAX_RECORDS)
    data = [
        go.Pie(
            labels=ct["id"].index,
            values=ct["id"].values
        )
    ]
    return go.Figure(data=data)


def top_records(ct):
    if ct.size > constant.MAX_RECORDS:
        sum_total = ct.sum(axis=0)
        ct = ct.head(constant.MAX_RECORDS)
        sum_head = ct.sum(axis=0)
        ct.loc['Others'] = sum_total.values - sum_head.values
    return ct


@app.callback(
    Output("pie-reviewer-duration", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),

    ]
)
def reviewer_duration_graph(creators, teams, repos, bands, years):
    df = dfReviewer
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Reviewer", bands, creators, repos, teams, years)
    ct = df.groupby("Reviewer").agg({"since_start": "mean"})
    data = [
        go.Bar(
            x=ct["since_start"].index,
            y=ct["since_start"].values
        )
    ]
    return go.Figure(data=data)


@app.callback(
    Output("timeline-reviewer", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),

    ]
)
def timeline_reviewer_graph(creators, teams, repos, bands, years):
    df = dfReviewer
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Reviewer", bands, creators, repos, teams, years)
    return create_count_timeline_table(df)


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


if __name__ == "__main__":
    app.run_server()
