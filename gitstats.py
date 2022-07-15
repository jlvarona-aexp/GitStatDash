import dash_bootstrap_components as dbc
import pandas as pd
from dash import html, dcc, Output, Input, dash_table
from flask import Flask
from pandas import Index

import constant
import commons
import styles
import dropdowns
import distributions
import creator_graphs
import reviewer_graphs
import personal_reports
import comparison

commons.calculate_data()

#server = Flask(__name__)

creator_charts = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(f"PR Count by Developer, Top {constant.MAX_RECORDS}", className="lead"),
                        dcc.Graph(id="pie-creator-count")
                    ], md=6, style=styles.CHART_TABLE_STYLE),

                dbc.Col(
                    [
                        html.Label("Average PR Duration (in Days)", className="lead"),
                        dcc.Graph(id="pie-creator-duration")
                    ], md=6, style=styles.CHART_TABLE_STYLE),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("PR Creation Count Over Time", className="lead"),
                        dcc.Graph(id="timeline-creator")
                    ], style=styles.CHART_TABLE_STYLE
                ),
                dbc.Col(
                    [
                        html.Label("PR Duration Average Over Time", className="lead"),
                        dcc.Graph(id="timeline-creator-average")
                    ], style=styles.CHART_TABLE_STYLE
                )
            ]
        )
    ]
)

creator_content = html.Div(creator_charts, id="creator-page-content", style=styles.CONTENT_STYLE)

reviewer_charts = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label(f"Review Count by Developer. Top {constant.MAX_RECORDS}", className="lead"),
                        dcc.Graph(id="pie-reviewer-count")
                    ], md=6, style=styles.CHART_TABLE_STYLE),
                dbc.Col(
                    [
                        html.Label("Average Time to First Review (in Days)", className="lead"),
                        dcc.Graph(id="pie-reviewer-duration")
                    ], md=6, style=styles.CHART_TABLE_STYLE),
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Label("Review Contributions Count Over Time", className="lead"),
                    dcc.Graph(id="timeline-reviewer")
                ], style=styles.CHART_TABLE_STYLE)
        )
    ]
)

reviewer_content = html.Div(reviewer_charts, id="reviewer-page-content", style=styles.CONTENT_STYLE)

creator_count_charts = html.Div(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.Label(f"PR Count by Developer, Top {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-creator-count")
                ], md=6, style=styles.CHART_TABLE_STYLE
            ),
            dbc.Col(
                [
                    html.Label(f"PR Addition Count by Developer, Top {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-creator-addition-count")
                ], md=6, style=styles.CHART_TABLE_STYLE
            )
            ]
        ),
        dbc.Row([
            dbc.Col(
                [
                    html.Label(f"PR Deletion Count by Developer, Top {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-creator-deletions-count")
                ], md=6, style=styles.CHART_TABLE_STYLE
            ),
            dbc.Col(
                [
                    html.Label(f"PR Changed Files Count by Developer, Top {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-creator-changed-files-count")
                ], md=6, style=styles.CHART_TABLE_STYLE
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

creator_count_content = html.Div(creator_count_charts, id="creator-count-content", style=styles.CONTENT_STYLE)

creator_pr_size_content = html.Div(pr_size_count, id="creator-pr-size-content", style=styles.CONTENT_STYLE)

personal_report_content = html.Div(personal_reports.creator_personal_count, id="creator-personal-count", style=styles.CONTENT_STYLE)

reviewer_count_charts = html.Div(
    [
        dbc.Row([
            dbc.Col(
                [
                    html.Label(f"Review Count by Developer, Top {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-reviewer-count")
                ], md=6, style=styles.CHART_TABLE_STYLE
            ),
            dbc.Col(
                [
                    html.Label(f"Review Count by Developer All States, Top {constant.MAX_RECORDS}", className="lead"),
                    dcc.Graph(id="pie-reviewer-all-count")
                ], md=6, style=styles.CHART_TABLE_STYLE
            )
            ]
        )
        # ,
        # dbc.Row(
        #     dbc.Col(
        #         [
        #             html.Label(f"Review Count by Developer, Bottom {constant.MAX_RECORDS}", className="lead"),
        #             dcc.Graph(id="pie-reviewer-count-bottom")
        #         ], md=6, style=styles.CHART_TABLE_STYLE
        #     )
        # )
    ]
)

comparison_charts = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("PR Creation Comparison Count Over Time", className="lead"),
                        dcc.Graph(id="timeline-creator-comp")
                    ], style=styles.CHART_TABLE_STYLE
                ),
                dbc.Col(
                    [
                        html.Label("PR Duration Comparison Average Over Time", className="lead"),
                        dcc.Graph(id="timeline-creator-average-comp")
                    ], style=styles.CHART_TABLE_STYLE
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("Review Contributions Count Comparison Over Time", className="lead"),
                        dcc.Graph(id="timeline-reviewer-comp")
                    ], style=styles.CHART_TABLE_STYLE
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("PR Creation Comparison Per Developer", className="lead"),
                        dcc.Graph(id="timeline-creator-to-creator-comp")
                    ], style=styles.CHART_TABLE_STYLE
                ),
            ]
        )
    ]
)


reviewer_count_content = html.Div(reviewer_count_charts, id="reviewer-count-content", style=styles.CONTENT_STYLE)

distribution_content = html.Div(distributions.distribution_charts, id="distribution-content", style=styles.CONTENT_STYLE)

comparison_content = html.Div(comparison_charts, id="comparison-page-content", style=styles.CONTENT_STYLE)

tabLayout = dbc.Container(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Creator", tab_id="creator-tab"),
                dbc.Tab(label="Creator Count", tab_id="creator-count-tab"),
                dbc.Tab(label="Creator Sizes", tab_id="creator-pr-size-tab"),
                dbc.Tab(label="Reviewer", tab_id="reviewer-tab"),
                dbc.Tab(label="Reviewer Count", tab_id="reviewer-count-tab"),
                dbc.Tab(label="Personal Report", tab_id="personal-report-tab"),
                dbc.Tab(label="Distributions", tab_id="distribution-tab"),
                dbc.Tab(label="Comparison", tab_id="comparison-tab")
            ],
            id="tabs",
            active_tab="creator-tab",
        ),
        html.Div(id="tab-content", className="w-100 h-100 p-4"),
    ],
    fluid=True
)

sidebar = html.Div(
    [
        html.H2("PR Metrics", className="display-4"),
        html.Hr(),
        html.P(
            "Select the criteria to filter the charts", className="lead"
        ),
        dbc.Switch(id="anonymous-data", label="Anonymous", value=commons.is_anonymous),
        dropdowns.creator_dd,
        dropdowns.team_dd,
        dropdowns.repo_dd,
        dropdowns.band_dd,
        dropdowns.year_dd,
        html.Hr(),
        dbc.Button("Refresh Data", id="refresh-button", className="me-3", href="/"),
        html.Hr(),
        dbc.Button("Export Data to Excel", id="export-button", className="me-3")
    ],
    style=styles.SIDEBAR_STYLE
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

commons.app.layout = mainLayout


@commons.app.callback(
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
    elif active_tab == "personal-report-tab":
        return personal_report_content
    elif active_tab == "reviewer-tab":
        return reviewer_content
    elif active_tab == "reviewer-count-tab":
        return reviewer_count_content
    elif active_tab == "distribution-tab":
        return distribution_content
    elif active_tab == "comparison-tab":
        return comparison_content


#    return "No tab selected"


if __name__ == "__main__":
    commons.app.run_server()
