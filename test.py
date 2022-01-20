from datetime import datetime

import dash
import numpy as np
from dash.dependencies import Input, Output
from dash import dash_table
from dash import dcc
from dash import html
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objs as go


import dbConnection


conn = dbConnection.getDBConnection()
#sqlCN = '''select distinct %s as "Creator Name" from users as u, CREATORS as c where u.id = c.creator'''
#print(sqlCN % "u.name")

dfCreator = pd.read_sql_query(dbConnection.sqlCreators, conn,
                              parse_dates={"Submitted": "%Y-%m-%d",
                                           "Done": "%Y-%m-%d",
                                           "Created At": "%Y-%m-%dT%H:%M:%S.%f",
                                           "Updated At": "%Y-%m-%dT%H:%M:%S.%f"})
#dfReviewer = pd.read_sql_query(dbConnection.sqlActivitiesDiffs, conn)
#dfRepos = pd.read_sql_query(dbConnection.sqlRepos, conn)
#dfTeams = pd.read_sql_query(dbConnection.sqlTeams, conn)
#dfBands = pd.read_sql_query(dbConnection.sqlBand, conn)
#dfCreatorNames = pd.read_sql_query(sqlCN % "u.nickname", conn)
#dfReviewerNames = pd.read_sql_query(dbConnection.sqlCommenterNames, conn)
conn.close()

result = dfCreator.groupby("Creator").agg({"Submitted": "count", "Created At": lambda group: group.sort_values().diff().mean()})
print(result)

# df = dfCreator[['id','Created At','Creator','Team','Band','Repo','Duration']]
# print(df)
# df2 = df.groupby("Creator").agg({"id":"count","Duration":"mean"})
# print(df2)
creators = ["Biana Digulio", "Bryan Frane"]
teams = ["Verde", "Blinky", "Scratchy", "Itchy"]
repos = ["m1-msl"]
bands = ["30"]
def formatDate(x):
    if x:
        if "/" in x:
            mydate = datetime.strptime(x, "%m/%d/%y")
            return mydate.strftime("%Y-%m")
        else:
            return x[0:7]
    else:
        return ""

def date_columns(x):
    if "/" in x["Submitted"]:
        mydate = datetime.strptime(x["Submitted"], "%m/%d/%y")
        x["Created"] = mydate.strftime("%Y-%m")
        x["YearCreated"] = mydate.strftime("%Y")
#        return mydate.strftime("%Y-%m")
    else:
        x["Created"] = x["Submitted"][0:7]
        x["YearCreated"] = x["Submitted"][0:4]
 #       return x[0:7]
    return x

df = dfCreator[['id', 'Submitted','Creator','Team','Band','Repo','Duration']]
#df = df.apply(date_columns, axis=1)
print(df.size)
ct = df.groupby("Creator").agg({"id": "count"}).sort_values(["id"], ascending=False)

sum_total = ct.sum(axis=0)
ct = ct.head(10)
sum_head = ct.sum(axis=0)
print(sum_total)
print(sum_head)
print(ct)
ct.loc['Other'] = sum_total.values - sum_head.values
#ct = ct.append({"id": {'Other', 9}}, ignore_index=True)
#ct._set_value("Others", sum_total - sum_head)
# indx = ct.index
# ix = indx.append(pd.Index(['Others']))
# ser = ct.values
# ser2 = ser.append([sum_total - sum_head])
# print(ser2)
# ct.index = ix
# print(ix)
print(ct)
print("===========================")
#boolean_series = df["Repo"].isin(["m1-api-contracts"])
#df = df[boolean_series]
#ios = df.groupby("Created At").agg({"id": "count"})

table = pd.pivot_table(df, values='id', index=['Created'],
                       columns=['Repo'], aggfunc=pd.Series.count)
print(table)
for column in table.columns:
    print(column)
    print(table[column].index)
    print(table[column].values)
#boolean_series = df["Creator"].isin(creators)
#df = df[boolean_series]
#boolean_series = df["Team"].isin(teams)
#df = df[boolean_series]
boolean_series = df["Repo"].isin(["m1-ios"])
df = df[boolean_series]
#boolean_series = df["Band"].isin(bands)
# df = df[boolean_series]
ct = df.groupby("Creator").agg({"id": "count"}).unstack()
#print(df["id"])
print("===========================")
print(ct)
print("===========================")
print(df['Creator'].unique())
print("===========================")
print(ct['id'].values)
print("===========================")
print(ct['id'].index)
# df = dfCreator.loc[(dfCreator["Creator"].isin(creators)) &
#                    (dfCreator["Team"].isin(teams)) &
#                    (dfCreator["Repo"].isin(repos)) &
#                    (dfCreator["Band"].isin(bands)),
#                    ['id', 'Creator']].groupby['Creator'].count()
#print(df)
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
# add an id column and set it as the index
# in this case the unique ID is just the country name, so we could have just
# renamed 'country' to 'id' (but given it the display name 'country'), but
# here it's duplicated just to show the more general pattern.
#df['id'] = df['country']
#dfCreator.set_index('id', inplace=True, drop=False)

app = dash.Dash(external_stylesheets=dbc.themes.BOOTSTRAP)

# creator_selected = dcc.Dropdown(
#     id='creator-dropdown',
#     multi=True,
#     options=[{
#         'label': x,
#         'value': x
#     } for x in dfCreatorNames["Creator Name"].tolist()
#     ]
# )
# reviewer_selected = dcc.Dropdown(
#     id='reviewer-dropdown',
#     multi=True,
#     options=[{
#         'label': x,
#         'value': x
#     } for x in dfReviewerNames["Reviewer Name"].tolist()
#     ]
# )
# repo_selected = dcc.Dropdown(
#     id='repo-dropdown',
#     multi=True,
#     options=[{
#         'label': x,
#         'value': x
#     } for x in dfRepos["Repo"].tolist()
#     ]
# )
# team_selected = dcc.Dropdown(
#     id='team-dropdown',
#     multi=True,
#     options=[{
#         'label': x,
#         'value': x
#     } for x in dfTeams["Team"].tolist()
#     ]
# )
# band_selected = dcc.Dropdown(
#     id='band-dropdown',
#     multi=True,
#     options=[{
#         'label': x,
#         'value': x
#     } for x in dfBands["Band"].tolist()
#     ]
# )

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("PR Metrics"),
        html.Hr(),
        dbc.Tabs(
            [
                dbc.Tab(label="Creator", tab_id="creator-tab"),
                dbc.Tab(label="Reviewer", tab_id="reviewer-tab")
            ],
            id="tabs",
            active_tab="creator-tab"
        ),
        html.Div(id="tab-content", className="p-4")
    ]
)

#     html.Div(
#     dui.Layout(
#         grid=grid,
#         controlpanel=controlPanel
#     ),
#     style = {
#         'height': '100vh',
#         'width': '100vw'
#     }
# )


# @app.callback(Output('creator_pie', 'figure'),
#               [Input('creator-dropdown', 'value')])
# def create_creator_pie(creators):
#     creator_df = dfCreator.set_index('Creator', inplace=True, drop=False)["Duration"].groupby("Creator").mean()
#     creators_label = ["Creator", "Duration"]
#     trace = go.Pie(
#         labels=creators_label,
#         textinfo="label+percent",
#         values=[creator_df[v] for v in creators_label]
#     )
#     return go.Figure(data= [trace],
#                      layout= {
#                          'showlegend': False,
#                          'title': "By Creator"
#                      }
#                      )
#
#
# @app.callback(
#     Output('datatable-row-ids-container', 'children'),
#     Input('datatable-row-ids', 'derived_virtual_row_ids'),
#     Input('datatable-row-ids', 'selected_row_ids'),
#     Input('datatable-row-ids', 'active_cell'))
# def update_graphs(row_ids, selected_row_ids, active_cell):
#     # When the table is first rendered, `derived_virtual_data` and
#     # `derived_virtual_selected_rows` will be `None`. This is due to an
#     # idiosyncrasy in Dash (unsupplied properties are always None and Dash
#     # calls the dependent callbacks when the component is first rendered).
#     # So, if `rows` is `None`, then the component was just rendered
#     # and its value will be the same as the component's dataframe.
#     # Instead of setting `None` in here, you could also set
#     # `derived_virtual_data=df.to_rows('dict')` when you initialize
#     # the component.
#     selected_id_set = set(selected_row_ids or [])
#
#     if row_ids is None:
#         dff = dfCreator
#         # pandas Series works enough like a list for this to be OK
#         row_ids = dfCreator['id']
#     else:
#         dff = dfCreator.loc[row_ids]
#
#     active_row_id = active_cell['row_id'] if active_cell else None
#
#     colors = ['#FF69B4' if id == active_row_id
#               else '#7FDBFF' if id in selected_id_set
#     else '#0074D9'
#               for id in row_ids]
#
#     return [
#         dcc.Graph(
#             id=column + '--row-ids',
#             figure={
#                 'data': [
#                     {
#                         'x': dff['Creator'],
#                         'y': dff[column],
#                         'type': 'bar',
#                         'marker': {'color': colors},
#                     }
#                 ],
#                 'layout': {
#                     'xaxis': {'automargin': True},
#                     'yaxis': {
#                         'automargin': True,
#                         'title': {'text': column}
#                     },
#                     'height': 250,
#                     'margin': {'t': 10, 'l': 10, 'r': 10},
#                 },
#             },
#         )
#         # check if column exists - user may have deleted it
#         # If `column.deletable=False`, then you don't
#         # need to do this check.
#         for column in ['pop', 'lifeExp', 'gdpPercap'] if column in dff
#     ]


if __name__ == '__main__':
    app.run_server(debug=True)
