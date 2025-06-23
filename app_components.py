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
                            className='text-center mb-4 mt-3',
                            style ={
                                'color': blue,
                                'fontSize': 30,
                                'font-weight': 'bold'
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
                        style={'margin-bottom':'20px'}
                    )
                ], className='justify-content-center', width=3)
            ], justify='center')
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
                        children=[]
                    ),
                ], id="tabs", active_tab="tab2")
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
                    html.Div(children="Computed scalar values",
                             style = {'color': blue,
                                      'fontSize': 20,
                                      'text-align': 'center'
                            },
                            className = 'mt-3 mb-3'
                    ),
                    dash_table.DataTable(data=None,
                                         columns=[
                                            {"name": "Parameter", "id": "Parameter"},
                                            {"name": "Value", "id": "Value"}
                                        ],
                                        id='summary-table')
                ])
            ])
    ])
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
                panel_1Dprofiles(params),
                figure_1Dprofiles()
            ], justify='center'
            )
        ])
    return div

## div element for 1D profile selection (left panel)
def panel_1Dprofiles(params):
     title = html.Div(
            children = 'Select profile type',
            style = {
                'color': blue,
                'fontSize': 20,
                'text-align': 'center'
            },
            className = 'mt-3 mb-3'
        )
     column = dbc.Col([
              title,
              html.Hr(),
              dbc.RadioItems(
                    options={i: params.attrs_label_dict[i] for i in params.attrs_profiles},
                    value=params.attrs_profiles[0],
                    id='buttons_1Dprofiles',
                    className = 'mb-3'
                ),
        
            ], className='mb-3', width=4
            )
     return column

## div element for 1D profile figures (right panel)
def figure_1Dprofiles():
    fig_display = html.Div(children=[dcc.Graph(figure={}, id='fig_1Dprofiles', mathjax=True)],
                            style={}
                            )
    column = dbc.Col(fig_display, 
                    width = 6,
                    className = 'mb-3 align-items-center')
    return column

## Tab 2 Update, triggered by callback 
def update_figure_1Dprofiles(eq_index,quantity,params):
    data = params.pp_eq_loaded[eq_index][quantity]
    rho_grid = params.grid_profiles.nodes[:,0]
    df = pd.DataFrame(dict(
        x=rho_grid,
        y=data
    ))
    labels = {'x': r'$\rho$', 'y': params.attrs_label_dict[quantity]}
    fig = px.line(df, x='x', y='y', labels=labels)
    return fig



#################################################
# Tab 3
#################################################
def comp_tab3(params):
    div = html.Div([
            dbc.Row([
                leftpanel_2D(params),
                rightpanel_2D(params)
            ], justify='center'
            )
        ])
    return div

def leftpanel_2D(params):
    col = dbc.Col([
                    figure_fluxsurf(),
                    slider_fluxsurf()
                ], width=4
                )
    return col

def rightpanel_2D(params):
    title = html.Div(
            children = 'Select profile type',
            style = {
                'color': blue,
                'fontSize': 20,
                'text-align': 'center'
            },
            className = 'mt-3 mb-3'
        )
    column = dbc.Col([
              figure_2D(),
              slider_2Dprofiles(),
              title,
              html.Hr(),
              dbc.RadioItems(
                    options={'const_rho': 'Constant rho surfaces', 'const_phi': 'Constant phi surfaces'},
                    value='const_rho',
                    id='buttons_2D_whichview',
                    className = 'mb-3'
                ),
              html.Hr(),
              dbc.RadioItems(
                    options={i: params.attrs_label_dict[i] for i in params.attrs_2d},
                    value=params.attrs_2d[0],
                    id='buttons_2Dprofiles_list',
                    className = 'mb-3'
                ),
        
            ], className='mb-3', width=4
            )
    return column

def figure_fluxsurf():
    fig_display = html.Div(children=[dcc.Graph(figure={}, id='figure_fluxsurf', mathjax=True)],
                            style={}
                            )
    column = dbc.Col(fig_display, 
                    className = 'mb-3')
    return column

def update_figure_fluxsurf(eq_index,slider_val, params):
    return params.pp_eq_loaded[eq_index]['flux_surfaces'][slider_val]


def slider_fluxsurf():
    slider=dcc.Slider(min=0, max = 0, step = None, marks={}, value=0, id='slider_fluxsurf')
    col = dbc.Row([
            dbc.Col([
                slider
            ], className = 'mb-3 align-items-center')
    ])
    return col

def update_slider_fluxsurf(eq_index,params):
    eq = params.eq_loaded[eq_index]
    max = round(2*3.14159/eq.NFP,2)
    marks = {i: f'{i}/{params.fx_num_phi} * 2 pi/{eq.NFP}' for i in range(0,params.fx_num_phi)}
    return max, marks


def figure_2D():
    fig_display = html.Div(children=[dcc.Graph(figure={}, id='figure_2d', mathjax=True)],
                            style={}
                            )
    column = dbc.Col(fig_display, 
                    className = 'mb-3')
    return column

def update_figure_2Dprofiles(eq_index,view, quantity, slider_val,params):
    if view == 'const_rho':
        return params.pp_eq_loaded[eq_index][quantity+'2d'+'const_rho'][slider_val]
    else:
        return params.pp_eq_loaded[eq_index][quantity+'2d'+'const_phi'][slider_val]

def slider_2Dprofiles():
    slider=dcc.Slider(min=0, max = 0, step = None, marks={}, value=0, id='slider_2d')
    col = dbc.Row([
            dbc.Col([
                slider
            ], className = 'mb-3 align-items-center')
    ])
    return col

def update_slider_2Dprofiles(eq_index,view, params):
    eq = params.eq_loaded[eq_index]
    if view == 'const_rho':
        max = 1
        marks = {i: f'{i}/{params.fx_num_rho}' for i in range(0,params.fx_num_rho)}
    else:
        max = round(2*3.14159/eq.NFP,2)
        marks = {i: f'{i}/{params.fx_num_phi} * 2 pi/{eq.NFP}' for i in range(0,params.fx_num_phi)}
    return max, marks




#################################################
# Initialization code
#################################################
def initialize(params):
    print("initializing")
    for item in os.listdir(params.base_desc_path):
        desc_path = os.path.join(params.base_desc_path, item)
        params.eq_names_list.append(item.removesuffix('.h5'))
        params.eq_loaded.append(desc.io.load(desc_path)) ## loading the equilibrium via DESC
        build_label_dict(params)
        params.pp_eq_loaded.append(build_data_dict(item, params)) ## loading the precomputed data


## unpacks the preprocessed files
def build_data_dict(curr_eq, params): 
    path_h5 = os.path.join(params.pp_desc_path, 'pp_'+curr_eq)
    f = h5py.File(path_h5, 'r')

    dict = {}

    ######### Loading scalar computed values 
    data_array_scalars = f['data_array_scalars'][()]
    for i in range(0, len(params.attrs_scalars)):
        dict[params.attrs_scalars[i]] = data_array_scalars[i]

    ######### Loading 1D profiles
    data_array_profiles = f['data_array_profiles'][()]
    for i in range(0, len(params.attrs_profiles)):
        dict[params.attrs_profiles[i]] = data_array_profiles[i]

    ######### Loading flux surface figures and 2dplots, reconverting to plotly
    path_json = os.path.join(params.pp_desc_path, 'pp_'+curr_eq.removesuffix('.h5')+'.json')
    with gzip.open(path_json, 'rt') as g:
        figure_list = json.load(g)
    dict['flux_surfaces'] = [plotly.io.from_json(fig) for fig in figure_list[0]]
    for i in range(0,len(params.attrs_2d)):
        q = params.attrs_2d[i]
        dict[q+'2d'+'const_rho'] = [plotly.io.from_json(fig) for fig in figure_list[i+1]]
        dict[q+'2d'+'const_phi'] = [plotly.io.from_json(fig) for fig in figure_list[i+1+len(params.attrs_2d)]]
    return dict


## loads labels for all plotted quantities
def build_label_dict(params):
    p = _parse_parameterization(params.eq_loaded[0])
    for i in range(0, len(params.attrs_scalars)):
        quantity = params.attrs_scalars[i]
        params.attrs_label_dict[quantity] = 'r$'+data_index[p][quantity]["label"]+'$'
    for i in range(0, len(params.attrs_profiles)):
        quantity = params.attrs_profiles[i]
        params.attrs_label_dict[quantity] = 'r$'+data_index[p][quantity]["label"]+'$'
    for i in range(0, len(params.attrs_2d)):
        quantity = params.attrs_2d[i]
        params.attrs_label_dict[quantity] = 'r$'+data_index[p][quantity]["label"]+'$'