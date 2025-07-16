from dash import html, dash_table,dcc, callback
import dash_bootstrap_components as dbc
import desc

from desc.compute import data_index
from desc.compute.utils import _parse_parameterization
from desc.equilibrium import Equilibrium

import plotly.express as px
import os 
import h5py
import pandas as pd
import numpy as np


import plotly
import plotly_plotting as pplotting

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
                            }
                    )
            )
    )
    return div


## dropdown with list of equilibria, and selection button
def comp_eq_dropdown(params):
     
     indices = range(0,len(params.eq_names_list))
     options={i: params.eq_names_list[i].removesuffix('.h5') for i in indices}

     button = dbc.Col(
                dbc.Button(
                    "Submit",
                    id="submit-eq-button",
                    color="secondary",  # choose color: "secondary", "info", etc.
                    className="me-1",
                    n_clicks=0
                ),
                width=4
            )
     dropdown = dbc.Col([
                    dcc.Dropdown(
                        options=options,
                        id='main_dropdown',
                        value='0',
                        style={'margin-bottom':'20px', 
                               'margin-left': '10px',
                                }
                    )
                ], className='justify-content-center', width=2)
     div = dbc.Row([dropdown,
                    button])

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
                ], id="tabs", active_tab="tab1", style=dict(color="primary"))
            ], width=12)
    ])
    return div


#################################################
# Prelims
#################################################
def load_meshes(eq_index,params):
    with h5py.File(params.pp_desc_path+'/pp_'+params.eq_names_list[eq_index],'r') as f:
            mesh_data = f['3d/mesh_3d_']
            params.meshes_loaded = [mesh_data["mesh_3d_" + rf"{j}/{params.surf3d_num_rho}"][:] for j in range(1,params.surf3d_num_rho+1)]
    
def load_cached_figures(eq_index,params):
    with h5py.File(params.pp_desc_path+'/pp_'+params.eq_names_list[eq_index],'r') as f:
        params.cached_figures = {'profile_1d_A':  plotly.io.from_json(f['cached_profile_1d_A'][()]),
                                 'profile_1d_B':  plotly.io.from_json(f['cached_profile_1d_B'][()]),
                                'fluxsurfaces_2d_': plotly.io.from_json(f['cached_fluxsurfaces_2d_'][()]),
                                 'constrho_2d_': plotly.io.from_json(f['cached_constrho_2d_'][()]),
                                 'fluxsurfaces_3d_': plotly.io.from_json(f['cached_fluxsurfaces_3d_'][()])
                                  }
        

def reset_sliders(params):
    return [0, params.surf2d_num_rho, params.surf3d_num_rho-1]

def reset_dropdowns(params):
    return [params.attrs_profiles[0], params.attrs_profiles[1], 'const_rho', params.attrs_2d[0], params.attrs_3d[0]]

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
                                        tooltip_data = None,
                                        tooltip_duration = None,
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
    with h5py.File(params.pp_desc_path+'/pp_'+params.eq_names_list[eq_index],'r') as f:
        data_scalars = f['/scalars'] ## This is a group, with attributes corresponding to the values
        
        df_list=[]
        hover_list=[]
        for q in params.attrs_scalars:
            val = data_scalars.attrs[q+'_scalar_'+'_value_']
            if isinstance(val, (int, np.float32, np.float64)):
                val = val.astype(float)
            
            val_str = ''
            if isinstance(val, float) and abs(val) >= 1000:
                val_str = f'{val:.3e}'
            elif isinstance(val, float):
                val_str = f'{val:.3f}'
            else: 
                val_str = str(val)


            text = f'Quantity: {data_scalars.attrs[q+'_scalar_'+'_description_']}  \n Units: {data_scalars.attrs[q+'_scalar_'+'_units_']}'
            df_list += [{'Parameter': q, 'Value': f'{val_str}'}]
            hover_list += [{'Parameter': {'value': text, 'type': 'markdown'}, 'Value': None}]

    df = pd.DataFrame(df_list)
    return df.to_dict('records'), hover_list

    






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
                                style=pplotting.borderstyle()
                            ), 
                        className = 'mb-3 align-items-center')])
    return fig_row_left

def figure_1dprofiles_right():
    fig_row_right = dbc.Row([
                        dbc.Col(
                            html.Div(
                                dcc.Graph(figure={}, id='fig_1dprofiles_right', mathjax=True),
                                style=pplotting.borderstyle()
                            ), 
                        className = 'mb-3 align-items-center')])
    return fig_row_right



## Tab 2 Update, triggered by callback 
def update_figure_1dprofiles(eq_index,quantity,params):
    with h5py.File(params.pp_desc_path+'/pp_'+params.eq_names_list[eq_index],'r') as f:
        data= f[f'/1d/'+ quantity +'_1d_']
        label = data.attrs['_label_']
        return pplotting.plotly_plot_1d(data[:],label,params)


#################################################
# Tab 3
#################################################
def comp_tab3(params):
    div = dbc.Col([panel_2d_row1(params), panel_2d_row2(params)])
    return div

def panel_2d_row1(params):
    col1 = dbc.Col([], width=5)
    dropdown1 = dbc.Col([html.Div(children=[
                                html.Div(children='View: '),
                                dcc.Dropdown(
                                    options={'const_rho': 'Fixed flux surface', 
                                            'const_phi': 'Fixed toroidal angle'},
                                    id='dropdown_2d_whichview',
                                    value='const_rho',
                                )
                            ])
                    ], width=2)
    dropdown2 = dbc.Col([html.Div(children=[
                                    html.Div(children='Quantity: '),
                                    dbc.Col([
                                        dcc.Dropdown(
                                            options={i: i for i in params.attrs_2d},
                                            id='dropdown_2dprofiles_list',
                                            value=params.attrs_2d[0]
                                        )
                                    ])
                                ])
                    ], width=2)
    return dbc.Row([col1, dropdown1, dropdown2] ,  justify='center', className='mt-3 mb-2')


def panel_2d_row2(params):
    col_left = dbc.Col([figure_fluxsurf(), slider_fluxsurf(params)], width=5)
    col_right = dbc.Col([figure_2d(), slider_2dprofiles(params)], width=5)
    return dbc.Row([col_left, col_right], justify='center')




def figure_fluxsurf():
    fig_display = html.Div(children=[dcc.Graph(figure={}, id='figure_fluxsurf', mathjax=True)],
                            style=pplotting.borderstyle())
    column = dbc.Col(fig_display, className = 'mb-3')
    return column

def update_figure_fluxsurf(eq_index,slider_val, params):
    with h5py.File(params.pp_desc_path+'/pp_'+params.eq_names_list[eq_index],'r') as f:
        data= f['/2d/fluxsurfaces_2d_']

        x = data.attrs['xrange']
        y = data.attrs['yrange']
        xdata1= data['rho_R'+'fluxsurfaces_2d_'+ rf'{slider_val}/{params.fx_num_phi-1}']
        ydata1= data['rho_Z'+'fluxsurfaces_2d_'+ rf'{slider_val}/{params.fx_num_phi-1}'][:]
        xdata2= data['vartheta_R'+'fluxsurfaces_2d_'+ rf'{slider_val}/{params.fx_num_phi-1}'][:]
        ydata2= data['vartheta_Z'+'fluxsurfaces_2d_'+ rf'{slider_val}/{params.fx_num_phi-1}'][:]
        phi_curr = xdata1.attrs['phi_curr']
        xdata1 = xdata1[:] ## Load into memory 
        fig = pplotting.plotly_plot_fluxsurf(xdata1,ydata1,xdata2,ydata2,phi_curr,params, xrange=x, yrange=y)
    
    return fig




def slider_fluxsurf(params):
    max = params.fx_num_phi-1
    marks={i:'' for i in range(0,params.fx_num_phi)}
    slider=dcc.Slider(min=0, max = max, step = None, marks=marks, value=0, id='slider_fluxsurf')
    col = dbc.Row([
            dbc.Col([
                slider
            ], className = 'mb-3 align-items-center', width=8)
    ], justify='center')
    return col




def figure_2d():
    fig_display = html.Div(children=[dcc.Graph(figure={}, id='figure_2d', mathjax=True)],
                            style=pplotting.borderstyle())
    column = dbc.Col(fig_display, 
                    className = 'mb-3')
    return column

def update_figure_2dprofiles(eq_index,view, quantity, slider_val,params):
    if view == 'const_rho':
        with h5py.File(params.pp_desc_path+'/pp_'+params.eq_names_list[eq_index],'r') as f:
            data= f['/2d/constrho_2d_/' + quantity + 'constrho_2d_' + rf'{slider_val}/{params.surf2d_num_rho}']
            label = data.attrs['_label_']
            rho_curr = data.attrs['_rho_curr_']
            fig = pplotting.plotly_plot_2dsurf_const_rho(data[:], label, rho_curr, params)
    else:
        with h5py.File(params.pp_desc_path+'/pp_'+params.eq_names_list[eq_index],'r') as f:
            data0 = f['/2d/constphi_2d_']
            x = data0.attrs['xrange']
            y = data0.attrs['yrange']
            data = f['/2d/constphi_2d_/' + quantity + 'constphi_2d_' + rf'{slider_val}/{params.surf2d_num_phi - 1}']
            lcfs_data = f['/2d/constphi_2d_LCFS_/constphi_2d_LCFS_' + rf'{slider_val}/{params.surf2d_num_phi - 1}']
            label=data.attrs['_label_']
            units=data.attrs['_units_']
            phi_curr=data.attrs['_phi_curr_']
            data = data[:]
            fig =  pplotting.plotly_plot_2dsurf_const_phi(data[0],data[1],data[2], lcfs_data[0], lcfs_data[1], phi_curr, label, units, params, xrange=x, yrange=y)
    fig.update_layout(title_x=.5, title_y=.85)
    return fig


def slider_2dprofiles(params):
    slider=dcc.Slider(min=0, max = params.surf2d_num_rho, step = None, marks={}, value=params.surf2d_num_rho, id='slider_2d')
    col = dbc.Row([
            dbc.Col([
                slider
            ], className = 'mb-3 align-items-center', width=8)
    ], justify='center')
    return col

def update_slider_2dprofiles(view, params):
    if view == 'const_rho':
        max = params.surf2d_num_rho
        marks = {i: '' for i in range(0,params.surf2d_num_rho+1)}
        value = params.surf2d_num_rho
    else:
        max = params.surf2d_num_phi-1
        marks = {i: '' for i in range(0,params.surf2d_num_phi)}
        value = 0
    return max, marks, value


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
                dbc.Col(html.Div(children=[dcc.Graph(figure={}, id='fig_3d', mathjax=True)], style=pplotting.borderstyle()), 
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
        with h5py.File(params.pp_desc_path+'/pp_'+params.eq_names_list[eq_index],'r') as f:
            curve_data= f['/3d/magaxis_3d_/magaxis_3d_']
            hovertemplate = curve_data.attrs['hovertemplate']
            fig=pplotting.plotly_plot_3dmagax(eq_index,curve_data[:], hovertemplate, params)
    else:
        with h5py.File(params.pp_desc_path+'/pp_'+params.eq_names_list[eq_index],'r') as f:
            color_data = f['/3d/constrho_3d_/' +quantity+"constrho_3d_"+rf"{slider_val+1}/{params.surf3d_num_rho}"]
            fig=pplotting.plotly_plot_3dsurf(color_data,params.meshes_loaded[slider_val],eq_index,quantity,slider_val+1,params)
    return fig
    








#################################################
# Initialization code
#################################################
def initialize(params):
    print("initializing")

    visible_files = [] 
    for item in os.listdir(params.base_desc_path):
        if not item.startswith('.'):
            visible_files.append(item)

    for item in visible_files:
        desc_path = os.path.join(params.base_desc_path, item)
        params.eq_names_list.append(item)
        params.eq_loaded.append(desc.io.load(desc_path)) ## loading the equilibrium via DESC

    load_meshes(0,params)
    load_cached_figures(0,params)




