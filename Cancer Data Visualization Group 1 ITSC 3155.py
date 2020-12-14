import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# Load CSV file
df = pd.read_csv('Compiled data.csv')

app = dash.Dash()

# Layout
app.layout = html.Div(children=[
    html.H1(children='Cancer Rates',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Web dashboard for Visualizing Cancer Rate Data', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart by state', style={'color': '#df1e56'}),
    html.Div('This bar chart represents most prevalent cancer type by selected state'),
    dcc.Graph(id='graph1'),
    html.Div('Please select a state', style={'color': '#ef3e18', 'margin': '10px'}),
    dcc.Dropdown(
        id='select-state',
        options=[
            {'label': 'Nevada', 'value': 'Nevada'},
            {'label': 'Idaho', 'value': 'Idaho'},
            {'label': 'Colorado', 'value': 'Colorado'},
            {'label': 'North Carolina', 'value': 'North Carolina'},
        ],
        value='Nevada'
    ),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart by cancer type', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the states with the most prevalent cancer type selected'),
    dcc.Graph(id='graph2'),
    html.Div('Please select a cancer type', style={'color': '#ef3e18', 'margin': '10px'}),
    dcc.Dropdown(
        id='select-cancer',
        options=[
            {'label': 'Brain and Nervous System', 'value': 'Brain and Other Nervous System'},
            {'label': 'Cervix', 'value': 'Cervix'},
            {'label': 'Colon and Rectum', 'value': 'Colon and Rectum'},
            {'label': 'Esophagus', 'value': 'Esophagus'},
        ],
        value='Brain and Other Nervous System'
    ),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Interactive Bar chart for cancer type cases and deaths by state', style={'color': '#df1e56'}),
    html.Div('This bar chart represents the cancer types and deaths by state'),
    dcc.Graph(id='graph3'),
    html.Br(),
    html.Div('Please select a state', style={'color': '#ef3e18', 'margin': '10px'}),
    dcc.Dropdown(
        id='select-state-death',
        options=[
            {'label': 'Idaho', 'value': 'Idaho'},
            {'label': 'South Dakota', 'value': 'South Dakota'},
            {'label': 'Texas', 'value': 'Texas'},
            {'label': 'Utah', 'value': 'Utah'},
        ],
        value='Idaho'
    )

])


# Interactive graph1
@app.callback(Output('graph1', 'figure'),
              [Input('select-state', 'value')])
def update_figure(selected_state):
    filtered_df = df[df['Area'] == selected_state]
    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    filtered_df['CaseCount'] = pd.to_numeric(filtered_df['CaseCount'], errors='coerce')
    new_df = filtered_df.sort_values(by=['CaseCount'], ascending=[False])
    data_interactive_barchart = [go.Bar(x=new_df['CancerType'], y=new_df['CaseCount'])]
    return {'data': data_interactive_barchart, 'layout': go.Layout(title='Confirmed Cases in '
                                                                         + selected_state,
                                                                   xaxis={'title': ''},
                                                                   yaxis={'title': 'Case Count'})}


# Interactive graph2
@app.callback(Output('graph2', 'figure'),
              [Input('select-cancer', 'value')])
def update_figure(selected_type):
    filtered_df = df[df['CancerType'] == selected_type]
    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    filtered_df['CaseCount'] = pd.to_numeric(filtered_df['CaseCount'], errors='coerce')
    new_df = filtered_df.sort_values(by=['CaseCount'], ascending=[False]).head(20)
    data_interactive_barchart2 = [go.Bar(x=new_df['Area'], y=new_df['CaseCount'], marker={'color': '#CD7f32'})]
    return {'data': data_interactive_barchart2, 'layout': go.Layout(title='Cases of ' + selected_type + ' Cancer',
                                                                    xaxis={'title': 'State'},
                                                                    yaxis={'title': 'Case Count'})}


# Interactive graph3
@app.callback(Output('graph3', 'figure'),
              [Input('select-state-death', 'value')])
def update_figure(selected_state_death):
    filtered_df = df[df['Area'] == selected_state_death]
    filtered_df = filtered_df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    filtered_df['CaseCount'] = pd.to_numeric(filtered_df['CaseCount'], errors='coerce')
    filtered_df['DeathCount'] = pd.to_numeric(filtered_df['DeathCount'], errors='coerce')
    new_df = filtered_df.sort_values(by=['CaseCount'], ascending=[False])
    trace1 = go.Bar(x=new_df['CancerType'], y=new_df['CaseCount'], name='Cases', marker={'color': '#FFD700'})
    trace2 = go.Bar(x=new_df['CancerType'], y=new_df['DeathCount'], name='Deaths', marker={'color': '#CD7f32'})
    data_interactive_barchart3 = [trace1, trace2]
    return {'data': data_interactive_barchart3, 'layout': go.Layout(title='Cases and Deaths in ' + selected_state_death,
                                                                    xaxis={'title': ''},
                                                                    yaxis={'title': 'Count'})}


if __name__ == '__main__':
    app.run_server()
