import commons
import constant
from dash import Output, Input
import plotly.graph_objs as go


@commons.app.callback(
    Output("pie-creator-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def creator_count_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
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
    Output("pie-creator-addition-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def creator_addition_count_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    ct = df.groupby("Creator").agg({"Additions": "sum"}).sort_values(["Additions"], ascending=False)
    ct = commons.top_records(ct)
    data = [
        go.Pie(
            labels=ct["Additions"].index,
            values=ct["Additions"].values
        )
    ]
    fig = go.Figure(data=data)
    fig.update_layout(autosize=True, margin=dict(t=0, b=0, l=0, r=0))
    return fig


@commons.app.callback(
    Output("pie-creator-deletions-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def creator_deletions_count_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    ct = df.groupby("Creator").agg({"Deletions": "sum"}).sort_values(["Deletions"], ascending=False)
    ct = commons.top_records(ct)
    data = [
        go.Pie(
            labels=ct["Deletions"].index,
            values=ct["Deletions"].values
        )
    ]
    fig = go.Figure(data=data)
    fig.update_layout(autosize=True, margin=dict(t=0, b=0, l=0, r=0))
    return fig


@commons.app.callback(
    Output("pie-creator-changed-files-count", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def creator_changed_files_count_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    ct = df.groupby("Creator").agg({"Changed Files": "count"}).sort_values(["Changed Files"], ascending=False)
    ct = settings.top_records(ct)
    data = [
        go.Pie(
            labels=ct["Changed Files"].index,
            values=ct["Changed Files"].values
        )
    ]
    fig = go.Figure(data=data)
    fig.update_layout(autosize=True, margin=dict(t=0, b=0, l=0, r=0))
    return fig


@commons.app.callback(
    Output("pie-creator-count-bottom", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def creator_count_bottom_graph(creators, teams, repos, bands, years, anonymous):
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
    Output("pie-creator-duration", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def creator_duration_graph(creators, teams, repos, bands, years, anonymous):
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
    Output("pr-size-table", "data"),
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
def creator_table_size_graph(creators, teams, repos, bands, years, page_current, page_size, sort_by, anonymous):
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
    Output('pr-size-table', 'page_count'),
    Input('datatable-use-page-count', 'value'),
    Input('datatable-page-count', 'value'))
def update_table(use_page_count, page_count_value):
    if len(use_page_count) == 0 or page_count_value is None:
        return None
    return page_count_value


@commons.app.callback(
    Output("timeline-creator", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def timeline_creator_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    return commons.create_count_timeline_table(df)


@commons.app.callback(
    Output("timeline-creator-average", "figure"),
    [
        Input("creator-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("repo-dropdown", "value"),
        Input("band-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("anonymous-data", "value")
    ]
)
def timeline_creator_average_graph(creators, teams, repos, bands, years, anonymous):
    df = commons.dfCreator
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    df = commons.filter_chart_data(df, "Creator", bands, creators, repos, teams, years)
    return commons.create_average_timeline_table(df)


