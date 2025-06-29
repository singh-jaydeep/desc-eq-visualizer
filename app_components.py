from dash import Dash, html, dash_table,dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import desc
from desc.grid import LinearGrid
from desc.compute import data_index
from desc.compute.utils import _parse_parameterization
from desc.equilibrium import Equilibrium
import plotly
import plotly.express as px
import plotly.graph_objects as go
import os 
import h5py
import pandas as pd
import json
import gzip
import numpy as np
from fractions import Fraction
import pprint

from plotly_plotting import plot_theme, borderstyle

#################################################
# Global style things
#################################################
blue = '#2c3e50'

#################################################
# Basic app components
#################################################

## Main title
def comp_title():
    div = html.Div(
            dbc.Row(
                    dbc.Col('DESC Visualization Dashboard', 
                            width=12, 
                            className='mb-4 mt-4 ms-3',
                            style ={
                                'color': 'white',
                                'fontSize': 25,
                                #'font-weight': 'bold'
                            }
                    )
            )
    )
    return div


## dropdown with list of equilibria
def comp_eq_dropdown(params):
     indices = range(0,len(params.eq_names_list))
     options={i: params.eq_names_list[i] for i in indices}
     div = dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        options=options,
                        id='main_dropdown',
                        value='0',
                        style={'margin-bottom':'20px', 
                               'margin-left': '10px',
                                }
                    )
                ], className='justify-content-center', width=2)
            ])
     return div

def comp_tabs(params):
    div = dbc.Row([
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(
                        label = 'Summary Statistics',
                        tab_id = 'tab1',
                        children=[comp_tab1(params)]
                    ),
                    dbc.Tab(
                        label = '1D Profiles',
                        tab_id = 'tab2',
                        children=[comp_tab2(params)]
                    ),
                    dbc.Tab(
                        label = 'Cross sections',
                        tab_id = 'tab3',
                        children=[comp_tab3(params)]
                    ),
                    dbc.Tab(
                        label = '3D Views',
                        tab_id = 'tab4',
                        children=[comp_tab4(params)]
                    )
                ], id="tabs", active_tab="tab2", style=dict(color="primary"))
            ], width=12)
    ])
    return div


#################################################
# Tab 1
#################################################

def comp_tab1(params):
    div = dbc.Container([
            dbc.Row([
                dbc.Col([
                    dash_table.DataTable(data=None,
                                         columns=[
                                            {"name": "Parameter", "id": "Parameter"},
                                            {"name": "Value", "id": "Value"}
                                        ],
                                        style_table={
                                            'overflowX': 'auto',
                                            'backgroundColor': '#343a40'  # Table wrapper (optional)
                                        },
                                        style_cell={
                                            'backgroundColor': '#343a40',
                                            'color': 'white',
                                            'border': '1px solid #495057'
                                        },
                                        style_header={
                                            'backgroundColor': '#495057',
                                            'color': 'white',
                                            'fontWeight': 'bold',
                                            'border': '1px solid #6c757d'
                                        },
                                        style_data_conditional=[
                                            {
                                                'if': {'row_index': 'odd'},
                                                'backgroundColor': '#3e444a',
                                            },
                                            {
                                                'if': {'state': 'active'},  # Clicked row
                                                'backgroundColor': '#495057',
                                                'border': '1px solid #adb5bd'
                                            },
                                            {
                                                'if': {'state': 'selected'},  # Selected via checkbox
                                                'backgroundColor': '#198754',  # Bootstrap 'success' green
                                                'color': 'white'
                                            }
                                        ],
                                        id='summary-table')
                ], width=6)
            ])
    ], className='mt-5')
    return div

## Tab 1 update, triggered by callback 
def update_table_stats(eq_index,params):
    return to_dataframe(eq_index,params).to_dict('records')

## Convert data to dataframe for passing into table 
def to_dataframe(eq_index,params):
    dict_whole = params.pp_eq_loaded[eq_index]
    dict_restrict = {key: dict_whole[key] for key in params.attrs_scalars}
    return pd.DataFrame([
        {"Parameter": key, "Value": f"{value:.3e}" if isinstance(value, float) and abs(value) >= 1000 
         else f"{value:.3f}" if isinstance(value, float) 
         else str(value)}
        for key, value in dict_restrict.items()
    ])



#################################################
# Tab 2
#################################################

def comp_tab2(params):
    div = html.Div([
            dbc.Row([
                panel_1dprofiles_left(params),
                panel_1dprofiles_right(params),
            ], justify='center')
        ])
    return div



def panel_1dprofiles_left(params):
    dropdown = dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        options={i: i for i in params.attrs_profiles},
                        id='dropdown_1dprofiles_left',
                        value=params.attrs_profiles[0],
                        style={'margin-bottom':'20px',
                               'margin-top':'20px'}
                    )], className='justify-content-center', width=3)
            ], justify='center')
    column_left = dbc.Col([
                   dropdown,
                   figure_1dprofiles_left()
               ], width=5) 

    return column_left

def panel_1dprofiles_right(params):
    dropdown = dbc.Row([
                dbc.Col([
                        dcc.Dropdown(
                            options={i: i for i in params.attrs_profiles},
                            id='dropdown_1dprofiles_right',
                            value=params.attrs_profiles[1],
                            style={'margin-bottom':'20px',
                                   'margin-top':'20px'}
                        )
                    ], className='justify-content-center', width=3)
            ], justify='center')
    column_right = dbc.Col([
                   dropdown,
                   figure_1dprofiles_right()
               ], width=5) 
    return column_right

def figure_1dprofiles_left():
    fig_row_left = dbc.Row([
                        dbc.Col(
                            html.Div(
                                dcc.Graph(figure={}, id='fig_1dprofiles_left', mathjax=True),
                                style=borderstyle()
                            ), 
                        className = 'mb-3 align-items-center')])
    return fig_row_left

def figure_1dprofiles_right():
    fig_row_right = dbc.Row([
                        dbc.Col(
                            html.Div(
                                dcc.Graph(figure={}, id='fig_1dprofiles_right', mathjax=True),
                                style=borderstyle()
                            ), 
                        className = 'mb-3 align-items-center')])
    return fig_row_right



## Tab 2 Update, triggered by callback 
def update_figure_1dprofiles(eq_index,quantity,params):
    data = params.pp_eq_loaded[eq_index][quantity]
    rho_grid = params.grid_profiles.nodes[:,0]
    df = pd.DataFrame(dict(
        x=rho_grid,
        y=data
    ))
    labels = {'x': r'$\rho$', 'y': ''}
    fig = px.line(df, x='x', y='y', labels=labels)
    title = fr'$\text{{Radial profile of }} {params.attrs_label_dict[quantity]}$'
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'y': 0.93,
        }
    )
    return plot_theme(fig)



#################################################
# Tab 3
#################################################
def comp_tab3(params):
    div = html.Div([
            dbc.Row([
                panel_2d_left(params),
                panel_2d_right(params)
            ], justify='center'
            )
        ])
    return div

def panel_2d_left(params):
    col = dbc.Col([
                    html.Div([figure_fluxsurf()], style={'margin-top':'60px'}),
                    slider_fluxsurf()
                ], width=5
                )
    return col

def panel_2d_right(params):
    selection_row1 = dbc.Col([html.Div(children=[
                                html.Div(children='View: '),
                                dcc.Dropdown(
                                    options={'const_rho': 'Fixed flux surface', 
                                            'const_phi': 'Fixed toroidal angle'},
                                    id='dropdown_2d_whichview',
                                    value='const_rho',
                                )
                            ])
                    ], width=5)
    selection_row2 = dbc.Col([html.Div(children=[
                                    html.Div(children='Quantity: '),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            options={i: i for i in params.attrs_2d},
                                            id='dropdown_2dprofiles_list',
                                            value=params.attrs_2d[0]
                                        )
                                    ])
                                ])
                    ], width=5)
    column = dbc.Col([
                dbc.Row([selection_row1, selection_row2], justify='center'),
                figure_2d(),
                slider_2dprofiles()
            ], className='mb-3', width=5
            )
    return column

def figure_fluxsurf():
    fig_display = html.Div(children=[dcc.Graph(figure={}, id='figure_fluxsurf', mathjax=True)],
                            style=borderstyle())
    column = dbc.Col(fig_display, 
                    className = 'mb-3')
    return column

def update_figure_fluxsurf(eq_index,slider_val, params):
    fig = params.pp_eq_loaded[eq_index]['flux_surfaces'][slider_val]
    return fig


def slider_fluxsurf():
    slider=dcc.Slider(min=0, max = 0, step = None, marks={}, value=0, id='slider_fluxsurf')
    col = dbc.Row([
            dbc.Col([
                slider
            ], className = 'mb-3 align-items-center', width=8)
    ], justify='center')
    return col

def update_slider_fluxsurf(eq_index,params):
    eq = params.eq_loaded[eq_index]
    max = params.fx_num_phi-1
    marks={i:'' for i in range(0,params.fx_num_phi)}
    return max, marks


def figure_2d():
    fig_display = html.Div(children=[dcc.Graph(figure={}, id='figure_2d', mathjax=True)],
                            style=borderstyle())
    column = dbc.Col(fig_display, 
                    className = 'mb-3')
    return column

def update_figure_2dprofiles(eq_index,view, quantity, slider_val,params):
    if view == 'const_rho':
        fig = params.pp_eq_loaded[eq_index][quantity+'2d'+'const_rho'][slider_val]
    else:
        fig = params.pp_eq_loaded[eq_index][quantity+'2d'+'const_phi'][slider_val]
    return fig

def slider_2dprofiles():
    slider=dcc.Slider(min=0, max = 0, step = None, marks={}, value=0, id='slider_2d')
    col = dbc.Row([
            dbc.Col([
                slider
            ], className = 'mb-3 align-items-center', width=8)
    ], justify='center')
    return col

def update_slider_2dprofiles(eq_index,view, params):
    eq = params.eq_loaded[eq_index]
    if view == 'const_rho':
        max = params.surf2d_num_rho
        marks = {i: '' for i in range(0,params.surf2d_num_rho+1)}
    else:
        max = params.surf2d_num_phi-1
        marks = {i: '' for i in range(0,params.surf2d_num_phi)}
    return max, marks


#################################################
# Tab 4
#################################################

def comp_tab4(params):
    div = html.Div([
            dbc.Row([
                panel_3d_left(params),
                panel_3d_right(params),
            ])
        ])
    return div



def panel_3d_left(params):
    options = {i: i for i in params.attrs_3d}
    options['1'] = 'flux surfaces'
    options['magnetic axis'] = 'magnetic axis'

    dropdown = dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        options=options,
                        id='dropdown_3d',
                        value=params.attrs_3d[0],
                        style={'margin-top':'20px', 'margin-bottom': '20px'}
                    )], className='justify-content-center', width=6)
            ], justify='center')
    column_left = dbc.Col([
                   dropdown,
                   slider_3d(params)
               ], width=3) 

    return column_left

def panel_3d_right(params):
    column_right = dbc.Col(html.Div(children=[figure_3d()], style={'margin-top': '20px'}), width=6) 
    return column_right



def figure_3d():
    fig_row = dbc.Row([
                dbc.Col(html.Div(children=[dcc.Graph(figure={}, id='fig_3d', mathjax=True)], style=borderstyle()), 
                            className = 'mb-3')
            ])
    return fig_row


def slider_3d(params):
    max = params.surf3d_num_rho-1
    marks = {i: '' for i in range(0,params.surf3d_num_rho)} 
    slider=dcc.Slider(min=0, max = max, step = None, marks=marks, value=params.surf3d_num_rho-1, id='slider_3d')
    col = dbc.Row([
            dbc.Col([
                slider
            ], className = 'mb-3 align-items-center', width=8)
    ], justify='center')
    return col



def update_figure_3dprofiles(eq_index, quantity, slider_val, params):
    if quantity == 'magnetic axis':
        fig = params.pp_eq_loaded[eq_index]['magnetic axis3d']
    else:
        fig = params.pp_eq_loaded[eq_index][quantity+'3d'][slider_val] 
    return fig











#################################################
# Initialization code
#################################################
def initialize(params):
    print("initializing")
    for item in os.listdir(params.base_desc_path):
        desc_path = os.path.join(params.base_desc_path, item)
        params.eq_names_list.append(item.removesuffix('.h5'))
        params.eq_loaded.append(desc.io.load(desc_path)) ## loading the equilibrium via DESC
        params.pp_eq_loaded.append(build_data_dict(item, params)) ## loading the precomputed data




## unpacks the preprocessed files
def build_data_dict(curr_eq, params): 
    data_dict = {}
    path_json = os.path.join(params.pp_desc_path, 'pp_'+curr_eq.removesuffix('.h5')+'.json')
    with gzip.open(path_json, 'rt') as g:
        data_collected = json.load(g)
    
    params.attrs_label_dict = data_collected[0]
    data_array = data_collected[1]
    figure_list = data_collected[2]

    ######## Loading summary statistics
    for i in range(0, len(params.attrs_scalars)):
        data_dict[params.attrs_scalars[i]] = data_array[0][i]

    ######## Loading 1D profiles
    for i in range(0, len(params.attrs_profiles)):
        data_dict[params.attrs_profiles[i]] = data_array[1][i]

    ######### Loading flux surface figures, 2dplots, and 3d plots, reconverting to plotly
    data_dict['flux_surfaces'] = [plotly.io.from_json(fig) for fig in figure_list[0]]
    for i in range(0,len(params.attrs_2d)):
        q = params.attrs_2d[i]
        data_dict[q+'2d'+'const_rho'] = [plotly.io.from_json(fig) for fig in figure_list[i+1]]
        data_dict[q+'2d'+'const_phi'] = [plotly.io.from_json(fig) for fig in figure_list[i+1+len(params.attrs_2d)]]
    for i in range(0, len(params.attrs_3d)):
        q = params.attrs_3d[i]
        data_dict[q+'3d'] = [plotly.io.from_json(fig) for fig in figure_list[i + 1 + len(params.attrs_2d) + len(params.attrs_2d)]]

    ######## Loading magnetic axis
    data_dict['magnetic axis3d'] = plotly.io.from_json(figure_list[1+2*len(params.attrs_2d)+len(params.attrs_3d)])


    

    return data_dict

