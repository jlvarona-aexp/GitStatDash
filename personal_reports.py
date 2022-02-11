import numpy as np

import commons
import constant
from dash import html, dcc, Output, Input, dash_table
import pandas as pd


creator_pr = html.Div([
    html.P(),
    html.Label(
        "Developer", className="lead"
    ),
    dcc.Dropdown(
        id="creator-pr-dropdown"),
], className="dash-bootstrap")

year_pr = html.Div([
    html.P(),
    html.Label(
        "Year", className="lead"
    ),
    dcc.Dropdown(
        id="year-pr-dropdown",
        options=[
            {'label': x,
             'value': x} for x in ["2020", "2021", "2022", "2023", "2024"]
        ], multi=True)], className="dash-bootstrap")


creator_personal_count = html.Div([
    creator_pr,
    year_pr,
    dash_table.DataTable(
        id="pr-personal-table",
        columns=[
            {"name": "PR's created by Week", "id": "Week"},
            {"name": "Your Count", "id": "You"},
            {"name": "My Peers", "id": "Peers"},
            {"name": "My Platform", "id": "Platform"},
            {"name": "My Organization", "id": "Everybody"}],   #[{"name": i, "id": i} for i in prSizeColumns],
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
def populate_creators_pr(anonymous):
    options = [
        {'label': x,
         'value': x
         } for x in commons.dfCreatorReport["name"].array
    ]
    return options


@commons.app.callback(
    Output("pr-personal-table", "data"),
    [
        Input("creator-pr-dropdown", "value"),
        Input("year-pr-dropdown", "value"),
        Input("pr-personal-table", "page_current"),
        Input("pr-personal-table", "page_size"),
        Input("pr-personal-table", "sort_by"),
        Input("anonymous-data", "value")
    ]
)
def creator_personal_report(creator, years, page_current, page_size, sort_by, anonymous):
    if creator:
        df = commons.dfCreator.copy()
        df['Created_At'] = df['Submitted'].apply(commons.format_week_date)
        if years:
            boolean_series = df["Created_At"].str[0:4].isin(years)
            df = df[boolean_series]

        main_rec = commons.dfCreatorReport.loc[commons.dfCreatorReport['name'] == creator]
        in_band_repo = commons.dfCreatorReport.loc[(commons.dfCreatorReport['platform'] == main_rec['platform'].values[0]) & (commons.dfCreatorReport['band'] == main_rec['band'].values[0])]['name'].values
        in_repo = commons.dfCreatorReport.loc[commons.dfCreatorReport['platform'] == main_rec['platform'].values[0]]['name'].values

        table = pd.pivot_table(df, values='id', index=['Created_At'],
                                columns=['Creator'], fill_value=0, aggfunc='count')

        data_res = {"You": table[creator].array}
        df_res = pd.DataFrame(data_res, index=table[creator].index.values)
        add_quantiles("All", table, df_res)

        create_quantiles("Platform", in_repo, df, df_res)

        create_quantiles("Peers", in_band_repo, df, df_res)

        df_res["Peers"] = df_res.apply(lambda row: categorise(row, "Peers"), axis=1)
        df_res["Platform"] = df_res.apply(lambda row: categorise(row, "Platform"), axis=1)
        df_res["Everybody"] = df_res.apply(lambda row: categorise(row, "All"), axis=1)
        df_res.index.name = "Week"
        df_res.reset_index(inplace=True)

        if len(sort_by):
            dff = df_res.sort_values(
                sort_by[0]['column_id'],
                ascending=sort_by[0]['direction'] == 'asc',
                inplace=False
            )
        else:
            # No sort is applied
            dff = df_res
        return dff.iloc[page_current*page_size:(page_current + 1) * page_size].to_dict('records')
    else:
        return []


def create_quantiles(level, filter, df, df_res):
    boolean_series = df["Creator"].isin(filter)
    df = df[boolean_series]
    table = pd.pivot_table(df, values='id', index=['Created_At'],
                       columns=['Creator'], fill_value=0, aggfunc='count')
    add_quantiles(level, table, df_res)


def add_quantiles(level, table, df_res):
    df_res[level+"30"] = table.quantile(0.3, axis=1)
    df_res[level+"50"] = table.quantile(0.5, axis=1)
    df_res[level+"90"] = table.quantile(0.9, axis=1)
    df_res[level+"95"] = table.quantile(0.95, axis=1)


def categorise(row, level):
    if row["You"] > row[level+"95"]:
        return "Top 5% 🔥"
    elif row["You"] > row[level+"90"]:
        return "Top 10%"
    elif row["You"] > row[level+"50"]:
        return "Top 50%"
    elif row["You"] > row[level+"30"]:
        return "Bottom 50%"
    else:
        return "Bottom 30% ❄️"
