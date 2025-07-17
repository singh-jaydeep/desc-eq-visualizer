#################################################
# Tab 3 plots 2D flux surfaces, and densities
# at const rho, const phi
#################################################
import h5py
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from plotting.plot_utils import borderstyle
from plotting.plot_building import plot_fluxsurf, plot_2dsurf_const_rho, plot_2dsurf_const_phi

def comp_tab(params):
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
                            style=borderstyle())
    column = dbc.Col(fig_display, 
                    className = 'mb-3')
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
        fig = plot_fluxsurf(xdata1,ydata1,xdata2,ydata2,phi_curr,params, xrange=x, yrange=y)
    
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
                            style=borderstyle())
    column = dbc.Col(fig_display, 
                    className = 'mb-3')
    return column


def update_figure_2dprofiles(eq_index,view, quantity, slider_val,params):
    if view == 'const_rho':
        with h5py.File(params.pp_desc_path+'/pp_'+params.eq_names_list[eq_index],'r') as f:
            data= f['/2d/constrho_2d_/' + quantity + 'constrho_2d_' + rf'{slider_val}/{params.surf2d_num_rho}']
            label = data.attrs['_label_']
            rho_curr = data.attrs['_rho_curr_']
            fig = plot_2dsurf_const_rho(data[:], label, rho_curr, params)
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
            fig =  plot_2dsurf_const_phi(data[0],data[1],data[2], lcfs_data[0], lcfs_data[1], phi_curr, label, units, params, xrange=x, yrange=y)
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
    else:
        max = params.surf2d_num_phi-1
        marks = {i: '' for i in range(0,params.surf2d_num_phi)}
    return max, marks, 0
