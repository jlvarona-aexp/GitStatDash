import pandas as pd

import commons
import constant
from dash import Output, Input
import plotly.graph_objs as go
import numpy as np


@commons.app.callback(
    Output("pie-creator-comp-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def creator_count_graph_comp(creators, teams, repos, bands, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df['Created_At_Year'] = df['Submitted'].apply(commons.format_year)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams)
    dff = df
    dff['createdat'] = pd.to_datetime(dff['createdat'], utc=True)
    #print(dff['createdat'].diff())
    ct = df.groupby("Creator").agg({"id": "count"}).sort_values(["id"], ascending=False)
    ct = commons.top_records(ct)
    data = [
        go.Pie(
            labels=ct["id"].index,
            values=ct["id"].values
        )
    ]
    fig = go.Figure(data=data)
    fig.update_layout(autosize=True, margin=dict(t=0, b=0, l=0, r=0))
    return fig


@commons.app.callback(
    Output("pie-creator-comp-count-bottom", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def creator_count_bottom_graph_comp(creators, teams, repos, bands, years, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
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


@commons.app.callback(
    Output("pie-creator-comp-duration", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def creator_duration_graph_comp(creators, teams, repos, bands, years, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    ct = df.groupby("Creator").agg({"Duration": "mean"})
    data = [
        go.Bar(
            x=ct["Duration"].index,
            y=ct["Duration"].values
        )
    ]
    return go.Figure(data=data)


@commons.app.callback(
    Output("pr-comp-size-table", "data"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("pr-size-table", "page_current"),
        Input("pr-size-table", "page_size"),
        Input("pr-size-table", "sort_by"),
        Input("anonymous-data", "value")
    ]
)
def creator_table_size_graph_comp(creators, teams, repos, bands, years, page_current, page_size, sort_by, anonymous):
    df = commons.dfCreator.copy()
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    df = df[["Created_At", "Creator", "Additions", "Deletions", "Changed Files", "Duration"]].copy()
    df = df.groupby("Creator").agg({"Additions": "mean", "Deletions": "mean", "Changed Files": "mean", "Duration": "mean"})
    df.reset_index(inplace=True)
    df["Additions"] = df["Additions"].round(2)
    df["Deletions"] = df["Deletions"].round(2)
    df["Changed Files"] = df["Changed Files"].round(2)
    df["Duration"] = df["Duration"].round(2)
    df['index'] = range(1, len(df) + 1)
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


@commons.app.callback(
    Output('pr-comp_size-table', 'page_count'),
    Input('datatable-use-page-count', 'value'),
    Input('datatable-page-count', 'value'))
def update_table_comp(use_page_count, page_count_value):
    if len(use_page_count) == 0 or page_count_value is None:
        return None
    return page_count_value


@commons.app.callback(
    Output("timeline-creator-comp", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def timeline_creator_graph_comp(creators, teams, repos, bands, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df['Created_At_Year'] = df['Submitted'].apply(commons.format_year)
    df['Created_At_Month'] = df['Submitted'].apply(commons.format_month)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, False)
    return create_count_timeline_table_comp(df)


@commons.app.callback(
    Output("timeline-creator-average-comp", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def timeline_creator_average_graph_comp(creators, teams, repos, bands, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df['Created_At_Year'] = df['Submitted'].apply(commons.format_year)
    df['Created_At_Month'] = df['Submitted'].apply(commons.format_month)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, False)
    return create_average_timeline_table_comp(df)


@commons.app.callback(
    Output("timeline-reviewer-comp", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def timeline_reviewer_graph_comp(creators, teams, repos, bands, anonymous):
    df = commons.dfReviewer
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df['Created_At_Year'] = df['Submitted'].apply(commons.format_year)
    df['Created_At_Month'] = df['Submitted'].apply(commons.format_month)
    df = commons.filter_chart_data(df, "Reviewer", bands, creators, repos, teams, False)
    return create_count_timeline_table_comp(df)


@commons.app.callback(
    Output("timeline-creator-to-creator-comp", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def timeline_creator_to_creator_graph_comp(creators, teams, repos, bands, years, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df['Created_At_Month'] = df['Submitted'].apply(commons.format_month)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    return create_developer_table_comp(df)


def create_count_timeline_table_comp(df):
    table = pd.pivot_table(df, values='id', index=['Created_At_Month'],
                           columns=['Created_At_Year'], aggfunc=pd.Series.count)
    data = []
    for column in table.columns:
        data.append(
            go.Scatter(
                x=table[column].index,
                y=table[column].values,
                name=column,
                #category_orders={"Created_At_Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]}
            )
        )
    figure = go.Figure(data=data)
    figure.update_yaxes(automargin=True, autorange=True)
    return figure


def create_average_timeline_table_comp(df):
    table = pd.pivot_table(df, values='Duration', index=['Created_At_Month'],
                           columns=['Created_At_Year'], aggfunc=np.mean)
    data = []
    for column in table.columns:
        data.append(
            go.Scatter(
                x=table[column].index,
                y=table[column].values,
                name=column
            )
        )
    figure = go.Figure(data=data)
    figure.update_yaxes(automargin=True, autorange=True)
    return figure


def create_developer_table_comp(df):
    table = pd.pivot_table(df, values='id', index=['Created_At'],
                           columns=['Creator'], aggfunc=pd.Series.count)
    data = []
    for column in table.columns:
        data.append(
            go.Scatter(
                x=table[column].index,
                y=table[column].values,
                name=column
            )
        )
    figure = go.Figure(data=data)
    figure.update_yaxes(automargin=True, autorange=True)
    return figure
