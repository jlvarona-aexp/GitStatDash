import pandas as pd
import commons
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
import plotly.figure_factory as ff
from sklearn.preprocessing import MaxAbsScaler
import styles

distribution_charts = html.Div(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.Label(f"PR Created Distribution", className="lead"),
                    dcc.Graph(id="dist-creator")
                ], style=styles.CHART_TABLE_STYLE
            )
        ]),
        dbc.Row([
            dbc.Col(
                [
                    html.Label(f"PR Duration Distribution", className="lead"),
                    dcc.Graph(id="dist-duration-creator")
                ], style=styles.CHART_TABLE_STYLE
            )
        ]),
        dbc.Row([
            dbc.Col(
                [
                    html.Label(f"PR Reviewed Distribution", className="lead"),
                    dcc.Graph(id="dist-reviewer")
                ], style=styles.CHART_TABLE_STYLE
            )
        ]
        )
    ]
)


@commons.app.callback(
    Output("dist-creator", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def dist_creator_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    return calc_count_graph(df)


@commons.app.callback(
    Output("dist-duration-creator", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def dist_duration_creator_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    return calc_avg_graph(df)


@commons.app.callback(
    Output("dist-reviewer", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def dist_reviewer_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfReviewer
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Reviewer", bands, creators, repos, teams, years)
    return calc_count_graph(df)


@commons.app.callback(
    Output("dist-duration-reviewer", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def dist_duration_reviewer_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfReviewer
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Reviewer", bands, creators, repos, teams, years)
    return calc_avg_graph(df)


def calc_count_graph(df):
    table = pd.pivot_table(df, values='id', index=['Created_At'],
                           columns='Repo', aggfunc=pd.Series.count, fill_value=0)
    return create_dist_graph(table)


def calc_avg_graph(df):
    table = pd.pivot_table(df, values='Duration', index=['Created_At'],
                           columns='Repo', aggfunc=pd.Series.mean, fill_value=0)
    return create_dist_graph(table)


def create_dist_graph(table):
    scaler = MaxAbsScaler()
    scaler.fit(table)
    scaled = scaler.fit_transform(table)
    scaled_df = pd.DataFrame(scaled, columns=table.columns)
    group_labels = scaled_df.columns.values.tolist()
    res = []
    for key, value in scaled_df.to_dict().items():
        res.append(list(value.values()))
    figure = ff.create_distplot(hist_data=res, group_labels=group_labels, curve_type="normal", show_hist=False)
    return figure
