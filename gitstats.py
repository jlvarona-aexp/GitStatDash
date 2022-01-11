from datetime import datetime

import dash
import dash_bootstrap_components as dbc
import numpy as np
from dash import html, dcc, Output, Input, dash_table
from flask import Flask
from pandas import Index

import constant
import dbConnection
import pandas as pd
import plotly.graph_objs as go


def calculate_data():
    global dfCreator, dfReviewer, dfReviewerAll, dfRepos, dfTeams, dfBands, dfCreatorNames, dfReviewerNames, dfCreatorSize
    conn = dbConnection.getDBConnection()
    dfCreator = pd.read_sql_query(dbConnection.sqlCreatorsShort, conn)
    dfReviewer = pd.read_sql_query(dbConnection.sqlActivitiesDiffsShort, conn)
    dfReviewerAll = pd.read_sql_query(dbConnection.sqlActivitiesDiffsAll, conn)
    dfRepos = pd.read_sql_query(dbConnection.sqlRepos, conn)
    dfTeams = pd.read_sql_query(dbConnection.sqlTeams, conn)
    dfBands = pd.read_sql_query(dbConnection.sqlBand, conn)
    dfCreatorNames = pd.read_sql_query(dbConnection.sqlCreatorNames, conn)
    dfReviewerNames = pd.read_sql_query(dbConnection.sqlCommenterNames, conn)
    conn.close()
#    dfCreatorSize = dfCreator[["Created_At", "Creator", "Additions", "Deletions", "Changed Files"]].copy()


calculate_data()

#server = Flask(__name__)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "PR Metrics Dashboard"

PAGE_SIZE = 20

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

CHART_TABLE_STYLE = {
    "border-style": "solid",
    "border-color": "#f8f9fa",
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
                        html.Label(f"PR Count by Developer, Top {constant.MAX_RECORDS}", className="lead"),
                        dcc.Graph(id="pie-creator-count")
                    ], md=6, style=CHART_TABLE_STYLE),

                dbc.Col(
                    [
                        html.Label("Average PR Duration (in Days)", className="lead"),
                        dcc.Graph(id="pie-creator-duration")
                    ], md=6, style=CHART_TABLE_STYLE),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("PR Creation Count Over Time", className="lead"),
                        dcc.Graph(id="timeline-creator")
                    ], style=CHART_TABLE_STYLE
                ),
                dbc.Col(
                    [
                        html.Label("PR Creation Average Over Time", className="lead"),
                        dcc.Graph(id="timeline-creator-average")
                    ], style=CHART_TABLE_STYLE
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
                        html.Label(f"Review Count by Developer. Top {constant.MAX_RECORDS}", className="lead"),
                        dcc.Graph(id="pie-reviewer-count")
                    ], md=6, style=CHART_TABLE_STYLE),
                dbc.Col(
                    [
                        html.Label("Average Time to First Review (in Days)", className="lead"),
                        dcc.Graph(id="pie-reviewer-duration")
                    ], md=6, style=CHART_TABLE_STYLE),
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Label("Review Contributions Count Over Time", className="lead"),
                    dcc.Graph(id="timeline-reviewer")
                ], style=CHART_TABLE_STYLE)
        )
    ]
)

reviewer_content = html.Div(reviewer_charts, id="reviewer-page-content", style=CONTENT_STYLE)

creator_count_charts = html.Div(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.Label(f"PR Count by Developer, Top {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-creator-count")
                ], md=6, style=CHART_TABLE_STYLE
            ),
            dbc.Col(
                [
                    html.Label(f"PR Addition Count by Developer, Top {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-creator-addition-count")
                ], md=6, style=CHART_TABLE_STYLE
            )
            ]
        ),
        dbc.Row([
            dbc.Col(
                [
                    html.Label(f"PR Deletion Count by Developer, Top {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-creator-deletions-count")
                ], md=6, style=CHART_TABLE_STYLE
            ),
            dbc.Col(
                [
                    html.Label(f"PR Changed Files Count by Developer, Top {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-creator-changed-files-count")
                ], md=6, style=CHART_TABLE_STYLE
            )
            ]
        )
    ]
)

pr_size_count = html.Div([
    dash_table.DataTable(
        id="pr-size-table",
        columns=[
            {"name": "Creator", "id": "Creator"},
            {"name": "Additions (lines)", "id": "Additions"},
            {"name": "Deletions (lines)", "id": "Deletions"},
            {"name": "Changed Files", "id": "Changed Files"},
            {"name": "Duration (days)", "id": "Duration"}],   #[{"name": i, "id": i} for i in prSizeColumns],
        page_current=0,
        page_size=PAGE_SIZE,
        page_action='custom',
        sort_action='custom',
        sort_mode='single',
        sort_by=[],
        style_header={'backgroundColor': 'black',
                      'color': 'white'},
        style_cell={'textAlign': 'center'},
        style_cell_conditional=[
            {
                'if': {'column_id': 'Creator'},
                'textAlign': 'left'
            }
        ]
    ),
    html.Br(),
    dcc.Checklist(
        id='datatable-use-page-count',
        options=[
            {'label': 'Use page_count', 'value': 'True'}
        ],
        value=['True']
    ),
    'Page count: ',
    dcc.Input(
        id='datatable-page-count',
        type='number',
        min=1,
        max=29,
        value=20
    )
    ]
)

creator_count_content = html.Div(creator_count_charts, id="creator-count-content", style=CONTENT_STYLE)

creator_pr_size_content = html.Div(pr_size_count, id="creator-pr-size-content", style=CONTENT_STYLE)

reviewer_count_charts = html.Div(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.Label(f"Review Count by Developer, Top {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-reviewer-count")
                ], md=6, style=CHART_TABLE_STYLE
            ),
            dbc.Col(
                [
                    html.Label(f"Review Count by Developer All States, Top {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-reviewer-all-count")
                ], md=6, style=CHART_TABLE_STYLE
            )
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Label(f"Review Count by Developer, Bottom {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-reviewer-count-bottom")
                ], md=6, style=CHART_TABLE_STYLE
            )
        )
    ]
)

reviewer_count_content = html.Div(reviewer_count_charts, id="reviewer-count-content", style=CONTENT_STYLE)

tabLayout = dbc.Container(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Creator", tab_id="creator-tab"),
                dbc.Tab(label="Creator Count", tab_id="creator-count-tab"),
                dbc.Tab(label="Creator Sizes", tab_id="creator-pr-size-tab"),
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
    elif active_tab == "creator-pr-size-tab":
        return creator_pr_size_content
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
    Output("pie-creator-addition-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
    ]
)
def creator_addition_count_graph(creators, teams, repos, bands, years):
    df = dfCreator
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    ct = df.groupby("Creator").agg({"Additions": "sum"}).sort_values(["Additions"], ascending=False)
    ct = top_records(ct)
    data = [
        go.Pie(
            labels=ct["Additions"].index,
            values=ct["Additions"].values
        )
    ]
    fig = go.Figure(data=data)
    fig.update_layout(autosize=True, margin=dict(t=0, b=0, l=0, r=0))
    return fig


@app.callback(
    Output("pie-creator-deletions-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
    ]
)
def creator_deletions_count_graph(creators, teams, repos, bands, years):
    df = dfCreator
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    ct = df.groupby("Creator").agg({"Deletions": "sum"}).sort_values(["Deletions"], ascending=False)
    ct = top_records(ct)
    data = [
        go.Pie(
            labels=ct["Deletions"].index,
            values=ct["Deletions"].values
        )
    ]
    fig = go.Figure(data=data)
    fig.update_layout(autosize=True, margin=dict(t=0, b=0, l=0, r=0))
    return fig


@app.callback(
    Output("pie-creator-changed-files-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
    ]
)
def creator_changed_files_count_graph(creators, teams, repos, bands, years):
    df = dfCreator
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    ct = df.groupby("Creator").agg({"Changed Files": "count"}).sort_values(["Changed Files"], ascending=False)
    ct = top_records(ct)
    data = [
        go.Pie(
            labels=ct["Changed Files"].index,
            values=ct["Changed Files"].values
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
        Output("pr-size-table", "data"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("pr-size-table", "page_current"),
        Input("pr-size-table", "page_size"),
        Input("pr-size-table", "sort_by")
    ]
)
def creator_table_size_graph(creators, teams, repos, bands, years, page_current, page_size, sort_by):
    df = dfCreator.copy()
    df['Created_At'] = df['Submitted'].apply(format_date)
    df = filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    df = df[["Created_At", "Creator", "Additions", "Deletions", "Changed Files", "Duration"]].copy()
    df = df.groupby("Creator").agg({"Additions": "mean", "Deletions": "mean", "Changed Files": "mean", "Duration": "mean"})
    df.reset_index(inplace=True)
    df["Additions"] = df["Additions"].round(2)
    df["Deletions"] = df["Deletions"].round(2)
    df["Changed Files"] = df["Changed Files"].round(2)
    df["Duration"] = df["Duration"].round(2)
    df[' index'] = range(1, len(df) + 1)
    if len(sort_by):
        dff = df.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = df
    return dff.iloc[page_current*page_size:(page_current + 1) * page_size].to_dict('records')


@app.callback(
    Output('pr-size-table', 'page_count'),
    Input('datatable-use-page-count', 'value'),
    Input('datatable-page-count', 'value'))
def update_table(use_page_count, page_count_value):
    if len(use_page_count) == 0 or page_count_value is None:
        return None
    return page_count_value


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
    Output("pie-reviewer-all-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),

    ]
)
def reviewer_all_count_graph(creators, teams, repos, bands, years):
    df = dfReviewerAll
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
