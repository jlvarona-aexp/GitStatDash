import commons
import constant
from dash import Output, Input
import plotly.graph_objs as go


@commons.app.callback(
    Output("pie-reviewer-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def reviewer_count_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfReviewer
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Reviewer", bands, creators, repos, teams, years)
    ct = df.groupby("Reviewer").agg({"id": "count"}).sort_values(["id"], ascending=False)
    ct = commons.top_records(ct)
    data = [
        go.Pie(
            labels=ct["id"].index,
            values=ct["id"].values
        )
    ]
    return go.Figure(data=data)


@commons.app.callback(
    Output("pie-reviewer-all-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def reviewer_all_count_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfReviewerAll
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Reviewer", bands, creators, repos, teams, years)
    ct = df.groupby("Reviewer").agg({"id": "count"}).sort_values(["id"], ascending=False)
    ct = commons.top_records(ct)
    data = [
        go.Pie(
            labels=ct["id"].index,
            values=ct["id"].values
        )
    ]
    return go.Figure(data=data)


@commons.app.callback(
    Output("pie-reviewer-count-bottom", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def reviewer_count_bottom_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfReviewer
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Reviewer", bands, creators, repos, teams, years)
    ct = df.groupby("Reviewer").agg({"id": "count"}).sort_values(["id"], ascending=True).head(constant.MAX_RECORDS)
    data = [
        go.Pie(
            labels=ct["id"].index,
            values=ct["id"].values
        )
    ]
    return go.Figure(data=data)


@commons.app.callback(
    Output("pie-reviewer-duration", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def reviewer_duration_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfReviewer
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Reviewer", bands, creators, repos, teams, years)
    ct = df.groupby("Reviewer").agg({"since_start": "mean"})
    data = [
        go.Bar(
            x=ct["since_start"].index,
            y=ct["since_start"].values
        )
    ]
    return go.Figure(data=data)


@commons.app.callback(
    Output("timeline-reviewer", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def timeline_reviewer_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfReviewer
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Reviewer", bands, creators, repos, teams, years)
    return commons.create_count_timeline_table(df)


