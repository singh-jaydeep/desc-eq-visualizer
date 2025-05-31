from dash import Dash, html, dash_table,dcc, callback, Output, Input, State
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
    return html.Div(
        className = 'row', 
        children='DESC Visualization Dashboard',
        style={
            'color': 'black',
            'fontSize': 30
        }
    )

## dropdown with list of equilibria
def comp_eq_dropdown(params):
     indices = range(0,len(params.eq_names_list))
     options={i: params.eq_names_list[i] for i in indices}
     return dcc.Dropdown(
            options=options,
            value = 0,
            id='dropdown_eqlist'
            )

## div element for 1D profiles
def comp_figure_1Dprofiles():
    fig_display = html.Div(className='row', 
                           children=[dcc.Graph(figure={}, id='fig_1Dprofiles')],
                            style={'display': 'flex', 
                                   'margin': 'auto', 
                                   'height': '80vh', 
                                   'width': '70%'}
                            )
    return fig_display


## radio buttons with options for different 1D profiles
def comp_buttons_1Dprofiles(params):
    buttons = dcc.RadioItems(options=params.attrs_profiles,
                            value=params.attrs_profiles[0],
                            inline=True,
                            id='buttons_1Dprofiles'
                            )
    buttons_display = html.Div(className='row',
                               children=[buttons])
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