import commons
import constant
from dash import html, dcc, Output, Input, dash_table
import pandas as pd
import numpy as np
import plotly.graph_objs as go


creator_pr = html.Div([
    html.P(),
    html.Label(
        "Developer", className="lead"
    ),
    dcc.Dropdown(
        id="creator-pr-dropdown",
        multi=True),
]
    , className="dash-bootstrap")


creator_personal_count = html.Div([
    creator_pr,
    dash_table.DataTable(
        id="pr-personal-table",
        columns=[
            {"name": "PR's created by Month", "id": "Created"},
            {"name": "You", "id": "Creator"},
            {"name": "My Peers", "id": "Additions"},
            {"name": "My Platform", "id": "Deletions"},
            {"name": "My Organization", "id": "Changed Files"}],   #[{"name": i, "id": i} for i in prSizeColumns],
        page_current=0,
        page_size=constant.PAGE_SIZE,
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


@commons.app.callback(
    Output("creator-pr-dropdown", "options"),
    [
        Input("anonymous-data", "value")
    ]
)
def populateCreatorsPR(anonymous):
    if anonymous:
        options = [
            {'label': x,
             'value': x
             } for x in commons.dfCreatorReport["name"].array
        ]
    else:
        options = []
    return options


@commons.app.callback(
    Output("pr-personal-table", "data"),
    [
        Input("creator-pr-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("pr-personal-table", "page_current"),
        Input("pr-personal-table", "page_size"),
        Input("pr-personal-table", "sort_by"),
        Input("anonymous-data", "value")
    ]
)
def creator_personal_report(creators, years, page_current, page_size, sort_by, anonymous):
    df = commons.dfCreator.copy()
    creator = "Amelia A Boli"
    df['Created_At'] = df['Submitted'].apply(commons.format_date)
    main_rec = commons.dfCreatorReport.loc[commons.dfCreatorReport['name'] == creator]
    in_band_repo = commons.dfCreatorReport.loc[(commons.dfCreatorReport['platform'] == main_rec['platform'].values[0]) & (commons.dfCreatorReport['band'] == main_rec['band'].values[0])]['name'].values
    in_repo = commons.dfCreatorReport.loc[commons.dfCreatorReport['platform'] == main_rec['platform'].values[0]]['name'].values

    table = pd.pivot_table(df, values='id', index=['Created_At'],
                            fill_value=0, aggfunc='count')
    print(table)
    print(table[creator])
    df = commons.filter_chart_data(df, "Creator", False, creators, False, False, years)
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
