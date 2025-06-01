from dash import Dash, html, dash_table,dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import desc
from desc.grid import LinearGrid
import plotly.express as px
import plotly.graph_objects as go
import os 
import h5py
import pandas as pd

#################################################
# Basic app components
#################################################

## Main title
def comp_title():
    div = html.Div(
            dbc.Row(dbc.Col('DESC Visualization Dashboard', 
                            width=12, 
                            className='text-center',
                            style ={
                                'fontSize': 30
                            }))
    )
    return div


## dropdown with list of equilibria
def comp_eq_dropdown(params):
     indices = range(0,len(params.eq_names_list))
     options={i: params.eq_names_list[i] for i in indices}
     return dcc.Dropdown(
            options=options,
            value = 0,
            id='dropdown_eqlist'
            )

## div element for 1D profile figures
def comp_figure_1Dprofiles():
    fig_display = html.Div(children=[dcc.Graph(figure={}, id='fig_1Dprofiles')],
                            style={}
                            )
    return fig_display

## div element for 1D profile left panel
def comp_panel_1Dprofiles(params):
     title = html.Div(
            children = '1D Profile Options',
            style = {
                'color': 'black',
                'fontSize': 20
            }
        )
     div = html.Div(
         children=[title, html.Hr(), comp_buttons_1Dprofiles(params)],
         style = {
            'border': 'solid gray'
         })
     return div


## radio buttons with options for different 1D profiles
def comp_buttons_1Dprofiles(params):
    buttons = dcc.RadioItems(options=params.attrs_profiles,
                            value=params.attrs_profiles[0],
                            id='buttons_1Dprofiles'
                            )
    buttons_display = html.Div(children=[buttons],
                               style = {'display': 'flex'}
                               )
    return buttons_display
                        



#################################################
# Update functions, triggered by callbacks
#################################################

## updates figure for 1D profiles
def update_figure_1Dprofiles(eq_index,quantity,params):
    data = params.pp_eq_loaded[eq_index][quantity]
    rho_grid = params.grid_profiles.nodes[:,0]
    df = pd.DataFrame(dict(
        x=rho_grid,
        y=data
    ))
    fig = px.line(df, x='x', y='y')
    return fig


#################################################
# Initialization code
#################################################
def initialize(params):
    print("initializing")
    for item in os.listdir(params.base_desc_path):
        desc_path = os.path.join(params.base_desc_path, item)
        pp_desc_path = os.path.join(params.pp_desc_path, 'pp_'+item)
        params.eq_names_list.append(item)
        params.eq_loaded.append(desc.io.load(desc_path)) ## loading the equilibrium via DESC
        params.pp_eq_loaded.append(build_dict(pp_desc_path,params)) ## loading the precomputed data


## unpacks the preprocessed files
def build_dict(pp_desc_path, params):
    f = h5py.File(pp_desc_path, 'r')
    dict = {}
    data_array_scalars = f['data_array_scalars'][()]
    for i in range(0, len(params.attrs_scalars)):
        dict[params.attrs_scalars[i]] = data_array_scalars[i]

    data_array_profiles = f['data_array_profiles'][()]
    for i in range(0, len(params.attrs_profiles)):
        dict[params.attrs_profiles[i]] = data_array_profiles[i]

    return dict