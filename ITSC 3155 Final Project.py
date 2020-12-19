import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd

df = pd.read_csv('Compiled data.csv')

app = dash.Dash()

# Group bar of deaths vs cases
filtered_df = df
filtered_df['CaseCount'] = pd.to_numeric(filtered_df['CaseCount'], errors='coerce')
filtered_df['DeathCount'] = pd.to_numeric(filtered_df['DeathCount'], errors='coerce')
case_df = filtered_df.groupby(['CancerType'])['CaseCount'].sum().reset_index()
death_df = filtered_df.groupby(['CancerType'])['DeathCount'].sum().reset_index()
trace1 = go.Bar(x=case_df['CancerType'], y=case_df['CaseCount'], name='Cases', marker={'color': '#FFD700'})
trace2 = go.Bar(x=death_df['CancerType'], y=death_df['DeathCount'], name='Deaths', marker={'color': '#CD7F32'})
data_barchart = [trace1, trace2]

app.layout = html.Div(children=[
    html.H1(children='Cancer Rates of 2017',
            style={
                'textAlign': 'center',
                'color': '#1b00b3'
            }),
    html.H2(children='This page provides data information on cancer case rates and death rates '
                     'across the United States broken down by states.',
            style={
                'textAlign': 'center'
            }),
    html.P("Please select a Cancer type: ",
           style={'margin-left': '210px'}),
    dcc.Dropdown(
        id='select-cancer',
        options=[
            {'label': 'Brain and Nervous System', 'value': 'Brain and Other Nervous System'},
            {'label': 'Cervix', 'value': 'Cervix'},
            {'label': 'Colon and Rectum', 'value': 'Colon and Rectum'},
            {'label': 'Corpus and Uterus', 'value': 'Corpus and Uterus NOS'},
            {'label': 'Esophagus', 'value': 'Esophagus'},
            {'label': 'Female Breast', 'value': 'Female Breast'},
            {'label': 'Hodgkin Lymphoma', 'value': 'Hodgkin Lymphoma'},
            {'label': 'Kaposi Sarcoma', 'value': 'Kaposi Sarcoma'},
            {'label': 'Kidney and Renal Pelvis', 'value': 'Kidney and Renal Pelvis'},
            {'label': 'Larynx', 'value': 'Larynx'},
            {'label': 'Leukemias', 'value': 'Leukemias'},
            {'label': 'Liver and Intrahepatic Bile Duct', 'value': 'Liver and Intrahepatic Bile Duct'},
            {'label': 'Lung and Bronchus', 'value': 'Lung and Bronchus'},
            {'label': 'Melanomas of the Skin', 'value': 'Melanomas of the Skin'},
            {'label': 'Mesothelioma', 'value': 'Mesothelioma'},
            {'label': 'Myeloma', 'value': 'Myeloma'},
            {'label': 'Non-Hodgkin Lymphoma', 'value': 'Non-Hodgkin Lymphoma'},
            {'label': 'Oral Cavity and Pharynx', 'value': 'Oral Cavity and Pharynx'},
            {'label': 'Ovary', 'value': 'Ovary'},
            {'label': 'Pancreas', 'value': 'Pancreas'},
            {'label': 'Prostate', 'value': 'Prostate'},
            {'label': 'Stomach', 'value': 'Stomach'},
            {'label': 'Testis', 'value': 'Testis'},
            {'label': 'Thyroid', 'value': 'Thyroid'},
            {'label': 'Urinary Bladder', 'value': 'Urinary Bladder'}
        ],
        value='Brain and Other Nervous System',
        style={'width': '250px',
               'margin-left': '100px'}
    ),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(label='Cases', children=[
            dcc.Graph(id='choropleth')
        ]),
        dcc.Tab(label='Deaths', children=[
            dcc.Graph(id='choropleth1')
        ]),
        dcc.Tab(label='Cases vs Deaths across the US', children=[
            dcc.Graph(id='graph',
                      figure={
                          'data': data_barchart,
                          'layout': go.Layout(xaxis={'title': 'Cancer Type',
                                                     'automargin': True},
                                              yaxis={'title': 'Cases vs Deaths'})
                      },
                      style={'height': '700px',
                             'margin-bottom': '100px'},

                      )
            ]),
        dcc.Tab(label='More Information', children=[
            html.Br(),
            html.P("Below is a list of links to Cancer.net where you can find much more information on each cancer "
                   "type."),
            html.Br(),
            html.Br(),
            html.A("Click here to visit Cancer.net's homepage", href='https://www.cancer.net/',
                   target='_blank', style={'margin-left': '100px'}),
            html.Br(),
            html.Br(),
            html.A("Brain and Nervous System Cancer",
                   href='https://www.cancer.net/cancer-types/brain-tumor/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Breast Cancer", href='https://www.cancer.net/cancer-types/breast-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Cervical Cancer", href='https://www.cancer.net/cancer-types/cervical-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Colon and Rectal Cancer", href='https://www.cancer.net/cancer-types/colorectal-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Uterine Cancer", href='https://www.cancer.net/cancer-types/uterine-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Esophageal Cancer", href='https://www.cancer.net/cancer-types/esophageal-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Hodgkin Lymphoma", href='https://www.cancer.net/cancer-types/lymphoma-hodgkin/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Kaposi Sarcoma", href='https://www.cancer.net/cancer-types/sarcoma-kaposi/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Kidney", href='https://www.cancer.net/cancer-types/kidney-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Larynx - Laryngeal and Hypopharyngeal",
                   href='https://www.cancer.net/cancer-types/laryngeal-and-hypopharyngeal-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Leukemia", href='https://www.cancer.net/navigating-cancer-care/videos/cancer-research-news/leukemia-adults-%E2%80%93-introduction-with-dr-bruno-medeiros',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Liver", href='https://www.cancer.net/cancer-types/liver-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Lung, Non-Small Cell",
                   href='https://www.cancer.net/cancer-types/lung-cancer-non-small-cell/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Lung, Small Cell", href='https://www.cancer.net/cancer-types/lung-cancer-small-cell/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Melanoma", href='https://www.cancer.net/cancer-types/melanoma/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Mesothelioma", href='https://www.cancer.net/cancer-types/mesothelioma/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Multiple Myeloma", href='https://www.cancer.net/cancer-types/multiple-myeloma/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Oral and Oropharyngeal",
                   href='https://www.cancer.net/cancer-types/oral-and-oropharyngeal-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Ovary, Fallopian Tube, and Peritoneal",
                   href='https://www.cancer.net/cancer-types/ovarian-fallopian-tube-and-peritoneal-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Pancreas", href='https://www.cancer.net/cancer-types/pancreatic-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Prostate", href='https://www.cancer.net/cancer-types/prostate-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Stomach", href='https://www.cancer.net/cancer-types/stomach-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Testicular", href='https://www.cancer.net/cancer-types/testicular-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Thyroid", href='https://www.cancer.net/cancer-types/thyroid-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br(),
            html.A("Bladder", href='https://www.cancer.net/cancer-types/bladder-cancer/introduction',
                   target='_blank', style={'margin-left': '150px'}),
            html.Br(),
            html.Br()
        ])
    ])
])


# Choropleth US map of cases of selected cancer type
@app.callback(
    Output('choropleth', 'figure'),
    [Input('select-cancer', 'value')])
def display_choropleth(cancer):
    new_df = df[df['CancerType'] == cancer]
    new_df['CaseCount'] = pd.to_numeric(new_df['CaseCount'], errors='coerce')
    new_df = new_df.sort_values(by=['CaseCount'], ascending=[False])
    fig = px.choropleth(new_df, locations='Code', locationmode='USA-states',
                        color='CaseCount', range_color=[100, 5000], hover_name='Area')

    fig.update_layout(
        geo_scope='usa',
        height=700
    )
    return fig


# Choropleth US map of deaths of selected cancer type
@app.callback(
    Output('choropleth1', 'figure'),
    [Input('select-cancer', 'value')])
def display_choropleth(cancer):
    new_df = df[df['CancerType'] == cancer]
    new_df['DeathCount'] = pd.to_numeric(new_df['DeathCount'], errors='coerce')
    new_df = new_df.sort_values(by=['DeathCount'], ascending=[False])
    fig = px.choropleth(new_df, locations=new_df['Code'], locationmode='USA-states',
                        color='DeathCount', range_color=[100, 5000], hover_name='Area')

    fig.update_layout(
        geo_scope='usa',
        height=700
    )
    return fig


if __name__ == '__main__':
    app.run_server()
