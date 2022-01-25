import commons
from dash import html, dcc, Output, Input

creator_dd = html.Div([
    html.P(),
    html.Label(
        "Developer", className="lead"
    ),
    dcc.Dropdown(
        id="creator-dropdown",
        multi=True),
]
    , className="dash-bootstrap")

band_dd = html.Div([
    html.P(),
    html.Label(
        "Band", className="lead"
    ),
    dcc.Dropdown(
        id="band-dropdown",
        multi=True)], className="dash-bootstrap")

repo_dd = html.Div([
    html.P(),
    html.Label(
        "Repo", className="lead"
    ),
    dcc.Dropdown(
        id="repo-dropdown",
        multi=True)], className="dash-bootstrap")

team_dd = html.Div([
    html.P(),
    html.Label(
        "Team", className="lead"
    ),
    dcc.Dropdown(
        id="team-dropdown",
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


@commons.app.callback(
    Output("creator-dropdown", "options"),
    [
        Input("a", "value")
    ]
)
def populateCreators(anonymous):
    options = [
        {'label': x,
         'value': x
         } for x in commons.dfCreatorNames["Creator Name"].array
    ]
    return options


@commons.app.callback(
    Output("band-dropdown", "options"),
    [
        Input("anonymous-data", "value")
    ]
)
def populateBands(anonymous):
    options = [
        {'label': x,
         'value': x
         } for x in commons.dfBands["Band"].array
    ]
    return options


@commons.app.callback(
    Output("repo-dropdown", "options"),
    [
        Input("anonymous-data", "value")
    ]
)
def populateRepos(anonymous):
    options = [
                {'label': x,
                 'value': x} for x in commons.dfRepos["Repo"].array
            ]
    return options


@commons.app.callback(
    Output("team-dropdown", "options"),
    [
        Input("anonymous-data", "value")
    ]
)
def populateTeams(anonymous):
    options = [
                {'label': x,
                 'value': x} for x in commons.dfTeams["Team"].array
            ]
    return options


@commons.app.callback(
    Output("anonymous-data", "value"),
    [
        Input("anonymous-data", "value")
    ]
)
def anonymize(anonymous_value):
    commons.is_anonymous = anonymous_value
    commons.calculate_data()
    return anonymous_value


@commons.app.callback(
    Output("store", "data"),
    [
        Input("refresh-button", "n_clicks"),
    ]
)
def on_button_click(n):
    commons.calculate_data()
    return {}

