import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file
df = pd.read_csv('Compiled data.csv')

app = dash.Dash()

# Bar chart
barchart_df = df[df['Area'] == 'Nevada']
barchart_df = barchart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
barchart_df = barchart_df.sort_values(by=['CaseCount'], ascending=[False]).head(20)
data_barchart = [go.Bar(x=barchart_df['CancerType'], y=barchart_df['CaseCount'])]
layout = go.Layout(title='Cancer Cases in Nevada', xaxis_title="Cancer Type", yaxis_title="Number of cases")

# Line chart
linechart_df = df[df['CancerType'] == 'Esophagus']
linechart_df = linechart_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
linechart_df = linechart_df.sort_values(by=['Population'], ascending=[False])
data_linechart = [go.Scatter(x=linechart_df['Population'], y=linechart_df['CaseCount'], mode='lines+markers',
                             name='Cases correlating to Population')]


# Layout
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Data Visualization using Python', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represents cancer type by state'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a type of cancer', style={'color': '#ef3e18', 'margin': '10px'}),
    dcc.Dropdown(
        id='select-state',
        options=[
            {'label': 'Nevada', 'value': 'Nevada'},
            {'label': 'Idaho', 'value': 'Idaho'},
            {'label': 'Colorado', 'value': 'Colorado'},
            {'label': 'Georgia', 'value': 'Georgia'},
        ],
        value='Nevada'
    ),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Bar chart', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the cases of the top 20 cancers found in Nevada'),
    dcc.Graph(id='graph2',
              figure={
                  'data': data_barchart,
                  'layout': go.Layout(title='Cases of the 20 most populous Cancers in Nevada',
                                      xaxis={'title': ''}, yaxis={'title': 'Number of cases'})
              }
              ),
    html.Br(),
    html.Hr(style={'color': '7FDBFF'}),
    html.H3('Line and marker chart', style={'color': 'df1e56'}),
    html.Div('This line and marker chart represents the cases of Esophagus cancer per population'),
    dcc.Graph(id='graph3',
              figure={
                  'data': data_linechart,
                  'layout': go.Layout(title='Cases of Esophagus cancer compared to population',
                                      xaxis={'title': 'Population'}, yaxis={'title': 'Number of cases'})
              })
])


# Interactive graph
@app.callback(Output('graph1', 'figure'),
              [Input('select-state', 'value')])
def update_figure(selected_state):
    filtered_df = df[df['Area'] == selected_state]

    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    new_df = filtered_df.groupby(['CancerType'])['CaseCount'].sum().reset_index()
    new_df = new_df.sort_values(by=['CaseCount'], ascending=[False]).head(20)
    data_interactive_barchart = [go.Bar(x=new_df['CancerType'], y=new_df['CaseCount'])]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title='Confirmed Cases in '
                                                                         + selected_state,
                                                                   xaxis={'title': 'State'},
                                                                   yaxis={'title': 'Case Count'})}


if __name__ == '__main__':
    app.run_server()
