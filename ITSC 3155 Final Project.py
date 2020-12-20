import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import sqlite3
from sqlite3 import Error
from datetime import date


def create_connection(file):
    conn = None
    try:
        conn = sqlite3.connect(file)
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_email(conn, email):
    """
    Create a new email into the emails table
    :param conn:
    :param email:
    :return: email id
    """
    sql = ''' INSERT INTO emails(email,date)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, email)
    conn.commit()
    return cur.lastrowid


if __name__ == '__main__':
    database = r"SQLDatabase.db"
    conn = create_connection(database)

    sql_create_emails_table = """ CREATE TABLE IF NOT EXISTS emails (
                                            id integer PRIMARY KEY,
                                            email text NOT NULL,
                                            date text
                                        ); """
    if conn is not None:
        # create email table
        create_table(conn, sql_create_emails_table)
    else:
        print("Error! cannot create the database connection.")


df = pd.read_csv('Compiled data.csv')

app = dash.Dash()


@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-on-submit', 'value')])
def update_output(n_clicks, value):
    conn = create_connection(database)
    with conn:
        if value is not None:
            email = (value, date.today())
            email_id = create_email(conn, email)


# Group bar of deaths vs cases
filtered_df = df
filtered_df['CaseCount'] = pd.to_numeric(filtered_df['CaseCount'], errors='coerce')
filtered_df['DeathCount'] = pd.to_numeric(filtered_df['DeathCount'], errors='coerce')
case_df = filtered_df.groupby(['CancerType'])['CaseCount'].sum().reset_index()
death_df = filtered_df.groupby(['CancerType'])['DeathCount'].sum().reset_index()
trace1 = go.Bar(x=case_df['CancerType'], y=case_df['CaseCount'], name='Cases', marker={'color': '#FFD700'})
trace2 = go.Bar(x=death_df['CancerType'], y=death_df['DeathCount'], name='Deaths', marker={'color': '#CD7F32'})
data_barchart = [trace1, trace2]

app.layout = html.Div(style={'background-color': '#567ca7', 'margin': '-21px -8px', 'height': '1000px'}, children=[
    html.Br(),
    html.H1(children='CANCER RATES OF 2017',
            style={
                'text-align': 'center',
                'color': 'white',
                'font-family': 'helvetica',
                'font-size': '40px'
            }),
    html.H2(children='This page provides data information on cancer throughout the United States',
            title='This information was taken from the CDCs website',
            style={
                'textAlign': 'center', 'font-family': 'helvetica', 'color': 'white'
            }),
    html.Br(),
    dcc.Tabs([
        dcc.Tab(label='MAPS', style={'background': '#47678c', 'border': 'none', 'font-family': 'helvetica',
                                     'color': 'white', 'font-weight': 'bold'},
                selected_style={'background': '#6796cb', 'border': 'none', 'font-family': 'helvetica',
                                'color': 'white', 'font-weight': 'bold'},
                children=[
                    html.Br(),
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
                        placeholder='Select a Cancer Type',
                        style={'margin': 'auto', 'width': '40%'}
                    ),
                    html.Br(),
                    dcc.Tabs([
                        dcc.Tab(label='CASES',
                                style={'background': '#47678c', 'border': 'none', 'font-family': 'helvetica',
                                       'color': 'white', 'font-weight': 'bold'},
                                selected_style={'background': '#6796cb', 'border': 'none', 'font-family': 'helvetica',
                                                'color': 'white', 'font-weight': 'bold'},
                                children=[
                                    html.P("This map shows the amount of cases of cancer type selected above by state:",
                                           style={'font-family': 'helvetica', 'color': 'white',
                                                  'text-align': 'center', 'margin': '50px 200px 0px',
                                                  'font-weight': 'bold', 'font-size': '18px'}),
                                    dcc.Graph(id='choropleth')
                                ]),
                        dcc.Tab(label='DEATHS',
                                style={'background': '#47678c', 'border': 'none', 'font-family': 'helvetica',
                                       'color': 'white', 'font-weight': 'bold'},
                                selected_style={'background': '#6796cb', 'border': 'none', 'font-family': 'helvetica',
                                                'color': 'white', 'font-weight': 'bold'},
                                children=[
                                    html.P("This map shows the amount of deaths due to the cancer type selected above"
                                           " by state:",
                                           style={'font-family': 'helvetica', 'color': 'white',
                                                  'text-align': 'center', 'margin': '50px 200px 0px',
                                                  'font-weight': 'bold', 'font-size': '18px'}),
                                    dcc.Graph(id='choropleth1')
                                ])
                    ])
                ]),
        dcc.Tab(label='CASES VS DEATHS', style={'background': '#47678c', 'border': 'none', 'font-family': 'helvetica',
                                                'color': 'white', 'font-weight': 'bold'},
                selected_style={'background': '#6796cb', 'border': 'none', 'font-family': 'helvetica',
                                'color': 'white', 'font-weight': 'bold'},
                children=[
                    html.P("This graph shows the amount of cases and deaths for each cancer type for"
                           " the entire United States:", style={'font-family': 'helvetica', 'color': 'white',
                                                                'text-align': 'center', 'margin': '50px 200px 0px',
                                                                'font-weight': 'bold', 'font-size': '18px'}),
                    dcc.Graph(id='graph',
                              figure={
                                  'data': data_barchart,
                                  'layout': go.Layout(xaxis={'title': 'Cancer Type',
                                                             'automargin': True, },
                                                      yaxis={'title': 'Cases vs Deaths'},
                                                      paper_bgcolor='#567ca7', font={'color': 'white'})
                              },
                              style={'height': '700px'},
                              )
                ]),
        dcc.Tab(label='MORE INFORMATION', style={'background': '#47678c', 'border': 'none', 'font-family': 'helvetica',
                                                 'color': 'white', 'font-weight': 'bold'},
                selected_style={'background': '#6796cb', 'border': 'none', 'font-family': 'helvetica',
                                'color': 'white', 'font-weight': 'bold'},
                children=[
                    html.Br(),
                    html.Div(style={'text-align': 'center'}, children=[
                    html.Div([
                    html.Div(dcc.Input(id='input-on-submit', type='email')),
                    html.Br(),
                    html.Button('Submit', id='submit-val'),
                    html.P("Enter your email and press submit to receive updates about cancer."),
                    html.Div(id='container-button-basic',
                             children='Please enter your email and press submit.')]),
                        html.P(
                            "Below is a list of links to Cancer.net where you can find "
                            "much more information on each cancer type.",
                            style={'color': 'white', 'font-family': 'helvetica', 'font-size': '18px',
                                   'font-weight': 'bold'}),
                        html.Br(),
                        html.Br(),
                        html.A("Cancer.net's Homepage", href='https://www.cancer.net/',
                               target='_blank', style={'background-color': '#edd139', 'padding': '15px 50px',
                                                       'display': 'inline-block', 'text-decoration': 'none',
                                                       'font-family': 'helvetica', 'font-size': '18px',
                                                       'margin': '10px'}),
                        html.Br(),
                        html.Div(className='flex-container', style={'display': 'flex', 'height': '150px',
                                                                    'flex-wrap': 'wrap', 'justify-content': 'center'},
                                 children=[
                                     html.A("Brain and Nervous System Cancer",
                                            href='https://www.cancer.net/cancer-types/brain-tumor/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Breast Cancer",
                                            href='https://www.cancer.net/cancer-types/breast-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Cervical Cancer",
                                            href='https://www.cancer.net/cancer-types/cervical-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Colon and Rectal Cancer",
                                            href='https://www.cancer.net/cancer-types/colorectal-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Uterine Cancer",
                                            href='https://www.cancer.net/cancer-types/uterine-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Esophageal Cancer",
                                            href='https://www.cancer.net/cancer-types/esophageal-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Hodgkin Lymphoma",
                                            href='https://www.cancer.net/cancer-types/lymphoma-hodgkin/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Kaposi Sarcoma",
                                            href='https://www.cancer.net/cancer-types/sarcoma-kaposi/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Kidney",
                                            href='https://www.cancer.net/cancer-types/kidney-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Larynx - Laryngeal and Hypopharyngeal",
                                            href='https://www.cancer.net/cancer-types/laryngeal-and-hypopharyngeal-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Leukemia",
                                            href='https://www.cancer.net/navigating-cancer-care/videos/cancer-research-news/leukemia-adults-%E2%80%93-introduction-with-dr-bruno-medeiros',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Liver",
                                            href='https://www.cancer.net/cancer-types/liver-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Lung, Non-Small Cell",
                                            href='https://www.cancer.net/cancer-types/lung-cancer-non-small-cell/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Lung, Small Cell",
                                            href='https://www.cancer.net/cancer-types/lung-cancer-small-cell/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Melanoma",
                                            href='https://www.cancer.net/cancer-types/melanoma/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Mesothelioma",
                                            href='https://www.cancer.net/cancer-types/mesothelioma/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Multiple Myeloma",
                                            href='https://www.cancer.net/cancer-types/multiple-myeloma/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Oral and Oropharyngeal",
                                            href='https://www.cancer.net/cancer-types/oral-and-oropharyngeal-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Ovary, Fallopian Tube, and Peritoneal",
                                            href='https://www.cancer.net/cancer-types/ovarian-fallopian-tube-and-peritoneal-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Pancreas",
                                            href='https://www.cancer.net/cancer-types/pancreatic-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Prostate",
                                            href='https://www.cancer.net/cancer-types/prostate-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Stomach",
                                            href='https://www.cancer.net/cancer-types/stomach-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Testicular",
                                            href='https://www.cancer.net/cancer-types/testicular-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Thyroid",
                                            href='https://www.cancer.net/cancer-types/thyroid-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br(),
                                     html.A("Urinary Bladder",
                                            href='https://www.cancer.net/cancer-types/bladder-cancer/introduction',
                                            target='_blank',
                                            style={'background-color': '#edd139', 'padding': '15px 50px',
                                                   'display': 'inline-block', 'text-decoration': 'none',
                                                   'font-family': 'helvetica', 'font-size': '18px',
                                                   'margin': '5px'}),
                                     html.Br()
                                 ])
                    ])
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
    fig = px.choropleth(new_df, locations='Code', locationmode='USA-states', color_continuous_scale='deep',
                        color='CaseCount', hover_name='Area')

    fig.update_layout(
        geo_scope='usa',
        height=700,
        paper_bgcolor='#567ca7',
        font={'color': 'white'},
        geo=dict(showlakes=True, lakecolor='rgb(255,255,255)')
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
    fig = px.choropleth(new_df, locations=new_df['Code'], locationmode='USA-states', color_continuous_scale='deep',
                        color='DeathCount', hover_name='Area')

    fig.update_layout(
        geo_scope='usa',
        height=700,
        paper_bgcolor='#567ca7',
        font={'color': 'white'},
        geo=dict(showlakes=True, lakecolor='rgb(255,255,255)')
    )
    return fig


if __name__ == '__main__':
    app.run_server()
