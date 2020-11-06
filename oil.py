import copy
import datetime as dt
import math
import os
import pickle

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
from dash.dependencies import Input, Output
from flask import Flask
from collections import Counter
from dash.dependencies import Input, Output, State


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__)
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

df = pd.read_csv('oil.csv')

re = df.rename(columns={'API Well Number':'api_well_no','Company Name':'company_name','API Hole Number':'api_hole_no',
                        'Well Type':'well_type','Production Field Name':'production_field_name','Well Status':'well_status',
                        'Well Name':'well_name','Producing Formation':'producing_formation','Months in Production':'months_in_production',
                        'Gas Produced, MCF':'gas_produced_mcf','Water Produced, bbl':'water_produced','Reporting Year':'reporting_year',
                        'Location 1':'location'})

drop = re.drop(['location'],axis=1)

dropp = re.drop(['api_well_no','api_hole_no','well_type','well_status','location','water_produced','Sidetrack',
                'months_in_production','Completion','County'], axis=1)


droppp = re.drop(['api_well_no','api_hole_no','well_type','water_produced','location','Sidetrack'], axis=1)
#comp_options = re["company_name"].unique()
droped = dropp.drop(['well_name','production_field_name','Town','producing_formation','reporting_year'], axis=1)


dropppp = re.drop(['api_well_no','api_hole_no','well_type','location','Sidetrack'], axis=1)
dropeddd = dropppp.drop(['well_name','production_field_name','Town','producing_formation','reporting_year','Completion' ,'well_status'  ,
                        'months_in_production', 'gas_produced_mcf','County'], axis=1)
#droped_sum = dropeddd.sum()

#dropedd = droped.sum()

totall = drop.pivot_table('gas_produced_mcf', index='reporting_year',
                           columns='well_type', aggfunc=sum)

companies = drop.groupby('company_name').gas_produced_mcf.sum()

boys = drop[drop.company_name == 'Ardent Resources, Inc.']

total_gas = drop.pivot_table('gas_produced_mcf', index='reporting_year',
                            columns='company_name',
                            aggfunc=sum)

subset = total_gas[['Belden & Blake Corporation','Columbia Natural Resources, Inc.','United States Gypsum Co.']]

comp_options = dropp["producing_formation"].unique()

comp_option = dropp["production_field_name"].unique()
#a = comp_option.sort()
company = dropp["Town"].unique()

df[' index'] = range(1, len(df) + 1)

dd = droppp.groupby('production_field_name').gas_produced_mcf.sum()



PAGE_SIZE = 5

n = droppp[droppp.well_status == 'AC']

group = droppp.groupby(['Town','producing_formation'], as_index=False).mean()


ggroup = droppp.groupby(['Town','producing_formation','company_name'], as_index=False).mean()

comp_names = n["company_name"].unique()




card = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Total gas produced", className="card-title"),
            html.H4(
                dropedd
            ),
        ]
    ),
    style={"width": "25rem"},
)


card1 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("water produced", className="card-title"),
            html.H4(
                droped_sum
            ),
        ]
    ),
    style={"width": "25rem"},
)


card2 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Custom CSS", className="card-title"),
            html.H4(
                ""
            ),
        ]
    ),
    style={"width": "25rem"},
)


card3 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Custom CSS", className="card-title"),
            html.H4(
                ""
            ),
        ]
    ),
    style={"width": "25rem"},
)


card4 = dbc.Card(
    dbc.CardBody(
        [
            html.H5("Custom CSS", className="card-title"),
            html.H4(
                ""
            ),
        ]
    ),
    style={"width": "25rem"},
)


nav1 = dbc.Nav(
    [
        html.Div([html.H3("Oil companies Data v2.0")]),
        #dbc.NavItem(dbc.NavLink("Another link with a longer label", href="#")),
    ],
    fill=True,
    
    #class="navbar navbar-expand-lg sticky-top navbar-light bg-light"
    #align ='center'



)

navs = html.Div([nav1])

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])






app.layout = html.Div([
    dbc.Navbar(navs),
    html.Br(),
    html.Div([
        
        html.Div([
         #   html.H1("Oil companies Data v2"),
        ],className='six columns'),
        #dbc.Alert("This is a primary alert about the oil produced worldwide check the info and dm me bout your insights", color="primary"),
        dbc.Card(card, color="info", outline=True),
        html.Hr(),
        dbc.Card(card1,color="info", outline=True),
        html.Hr(),
        
        #dbc.Card(card2,color="info", outline=True),
        #dbc.Card(card3,color="info", outline=True),
        #dbc.Card(card4,color="info", outline=True),
        #dbc.Button(
        #    "interactive data",
        #    color="info",
        #    block=True,
        #    id="button",
        #    className="mb-3",
        #),
        
    ],className="row"),
     

html.Div([
    html.Div([
    #html.Div([
    
    html.Div(
        [
            dcc.Dropdown(
                id="Manager", 
                #options=[{'label': i, 'value': i} for i in comp_options],
                options=[
                    {'label': i, 'value': i} for i in comp_options
                    #{'label': 'Montréal', 'value': 'MTL'},
                    #{'label': 'San Francisco', 'value': 'SF'}
                ],
                #value='MTL'
                value='All Companies'),
        ],
        style={'width': '25%',
                'display': 'inline-block'}
    ),

    

   
    dcc.Graph(
        #html.H4("Oil gas produced"),
        id='linechartoilproduced',
        #figure=fig
        
        
    ),
    dcc.Slider(
        id='Managerrr',
        min=dropp['reporting_year'].min(),
        max=dropp['reporting_year'].max(),
        value= dropp['reporting_year'].min(),#dropp['reporting_year'].min(),
        marks= {str(reporting_year): str(reporting_year) for reporting_year in dropp['reporting_year'].unique()},
        step=None
    )
    ]),
    

    html.Div([
     html.Div(
        [
            dcc.Dropdown(
                id="Managerr",
                options=[{
                    'label':i,
                   'value':i
                } for i in comp_option],
                value='All Managers'
            ),
        ],
        style={'width': '25%',
                'display': 'inline-block'}
    ),

    dcc.Graph(
        #html.H4("Oil gas produced"),
        id='linechartoil',
        #figure=fig
    )
    ]),
    #],className='row'),
    


    #html.Div([
    html.Div([
    html.Div(
        [
            dcc.Dropdown(
                id= "Manage",
                options=[{
                    'label':i,
                   'value':i
                } for i in company],
                value='all companies'
            ),
        ],
        style={'width': '25%',
                'display': 'inline-block'}
    ),
    
    
  
    dcc.Graph(
        #html.H4("Oil gas produced"),
        id='piechartoil',
        #figure=fig
    )
    ]),

    html.Div([
     html.Div(
        [
            dcc.Dropdown(
                id="Company_names",
                options=[{
                    'label':i,
                   'value':i
                } for i in comp_names],
                value='All Managerss'
            ),
        ],
        style={'width': '35%',
                'display': 'inline-block'}
    ),

    dcc.Graph(
        #html.H4("Oil gas produced"),
        id='linechartoilcompany',
        #figure=fig
    )
    ]), #
    #],className='row'),



html.Hr(),
    
    html.Div(
        
        dcc.Graph(
        
            id='activeinactive',
        #figure=fig
        ),
    ),

        
    html.Div(
        
        dcc.Graph(
        
            id='linegraph',
        #figure=fig
        ),
    ),
  
  

])

])
#className='offset-by-one'

@app.callback(
    dash.dependencies.Output('linechartoilproduced', 'figure'),
    [dash.dependencies.Input('Manager', 'value'),
    dash.dependencies.Input('Managerrr', 'value')]

)

def update_graph(Manager, Managerrr):
    if Manager == "All Companies":
        df_plot = dropp.copy()
    else:
        df_plot = dropp[dropp['producing_formation'] == Manager]#['Value']
        df_plot = dropp[dropp['reporting_year'] == Managerrr]

    #if Managerrr == "all_companies":
    #    df_plot = dropp.copy()
    #else:
    #    df_plot = dropp[dropp['reporting_year'] == Managerrr]
    

    fig = px.histogram(
        data_frame=df_plot,
        y='gas_produced_mcf',
        x='Town',
        title = 'Producing formation'#'well_name',
        #color='reporting_year'
    )

    return fig 



@app.callback(
    dash.dependencies.Output('linechartoil', 'figure'),
    [dash.dependencies.Input('Managerr', 'value')]

)

def update(Managerr):
    if Managerr == "All Managers":
        df_plott = drop.copy()
    else:
        df_plott = dropp[dropp['production_field_name'] == Managerr]#['Value']
    

    fig = px.histogram(
        data_frame=df_plott,
        y='gas_produced_mcf',
        x='company_name',
        title='Production field name, The data below shows the amount of gas produced by each companys field'
        #color='reporting_year'#
    )

    return fig 


@app.callback(
    dash.dependencies.Output('piechartoil', 'figure'),
    [dash.dependencies.Input('Manage', 'value')]

)

def pieupdate(Manage):
    if Manage == "all companies":
        vee = dropp.copy()
    else:
        vee = dropp[dropp['Town'] == Manage]#['Value']
    

    fig = px.pie(
        data_frame=vee,
        values='gas_produced_mcf',
        names='producing_formation',
        title = 'Pie Chart showing each Town and the producing formations in that town',
        color='producing_formation'#
    )

    return fig 


@app.callback(
    Output('datatable-paging', 'data'),
    [Input('datatable-paging', "page_current"),
     Input('datatable-paging', "page_size")])
def update_table(page_current,page_size):
    return df.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')



@app.callback(
    dash.dependencies.Output('linechartoilcompany', 'figure'),
    [dash.dependencies.Input('Company_names', 'value')]

)

def update(Company_names):
    if Company_names == "All Managerss":
        plot = n.copy()
    else:
        plot = n[n['company_name'] == Company_names]#['Value']
    

    fig = px.histogram(
        data_frame=plot,
        y='gas_produced_mcf',
        x='Town',
        title = 'Histogram showing companies, towns they are located and the gas produced at each Town'
        #color='reporting_year'#
    )

    return fig 


@app.callback(
    dash.dependencies.Output('activeinactive', 'figure'),
    [dash.dependencies.Input('Company_names', 'value')]

)

def update(Company_names):
    
    

    fig = px.pie(
        data_frame=droppp,
        values='gas_produced_mcf',
        names='well_status',
        title = 'companies well status',
        hover_data=['well_status'], labels={'well_status':'well status'}
        #color='reporting_year'#
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig 


@app.callback(
    dash.dependencies.Output('linegraph', 'figure'),
    [dash.dependencies.Input('Company_names', 'value')]

)

def update(line):
    
    

    fig = px.line(
        data_frame=dd,
        y='gas_produced_mcf',
        #names='well_status',
        title = 'line graph test'#,
        #hover_data=['well_status'], labels={'well_status':'well status'}
        #color='reporting_year'#
    )
   #fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig 



if __name__ == '__main__':
    app.run_server(debug=False)











