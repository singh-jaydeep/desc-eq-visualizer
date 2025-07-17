import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from desc.plotting import plot_surfaces

from . import plot_utils as pu



def plot_1d(data, label, params):
    rho_grid = params.grid_profiles.nodes[:,0]
    df = pd.DataFrame(dict(
                        x=rho_grid,
                        y=data
                        ))
    
    labels = {'x': r'$\rho$', 
              'y': ''}
    title = fr'$\text{{Radial profile of }} {label}$'

    fig = px.line(df, x='x', y='y', labels=labels)
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'y': 0.93,
        }
    )
    fig = pu.plot_theme(fig, change_grid=1)   
    return fig
     

def plot_fluxsurf(xdata1, ydata1, xdata2, ydata2, phi_curr, params, xrange=None, yrange=None): 
    fig = go.Figure()

    for i in range(0,params.fx_num_rho):
        fig.add_trace(go.Scatter(x=xdata1[:,i], 
                                 y= ydata1[:,i], 
                                 mode = 'lines',
                                 line = dict(
                                            color='#759eeb',
                                            width=2
                                        )
                                ))
        fig.update_traces(showlegend=False)

    for i in range(0,params.fx_num_theta):
        fig.add_trace(go.Scatter(x=xdata2[:,i], 
                                 y= ydata2[:,i], 
                                 mode = 'lines',
                                 line = dict(
                                            color="#e65566",
                                            width=2,
                                            dash='dash'
                                        )
                                ))
        fig.update_traces(showlegend=False)

    fig.update_layout(
        title={
            'text': fr"$\text{{Flux surfaces at toroidal angle }} \phi = {phi_curr:.3f}\pi$",
            'x': 0.5,
            'y': 0.85,
        },
        xaxis=dict(
            title=dict(
                text="R (m)"
            )
        )
    )
    fig.update_layout(
        annotations=[
            {
                'text': 'Z (m)',
                'xref':"paper",
                'yref':"paper",
                'x': -.15,
                'y': .5,
                'showarrow': False,
                'textangle': 0,
                'xanchor':"left",
                'yanchor':"bottom",
                'font': dict(size=14)
            }
        ]
    )
    if np.any(xrange):
         fig.update_layout(xaxis=dict(range=xrange))
    
    if np.any(yrange):
         fig.update_layout(yaxis=dict(range=yrange))

    fig = pu.plot_theme(fig, change_grid=1)

    return fig
    


def plot_2dsurf_const_rho(data, label, rho_curr, params):

    numtheta = 2*params.grid_const_rho_args["M"]+1
    numzeta = 2*params.grid_const_rho_args["N"]+1
    thetadata = np.linspace(0,2*3.14159, numtheta)
    zetadata = np.linspace(0, 2*3.14159, numzeta)
    title = fr'${label} \ \text{{at flux surface }} \rho={rho_curr:.3f}$'

    fig = go.Figure()
    fig.add_heatmap(autocolorscale=False, 
                    colorscale='plasma', 
                    y=thetadata, 
                    x=zetadata, 
                    z=data) 

    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'y': 0.85,
        },
        xaxis=dict(
            title=dict(
                text= fr'$\phi$'
            )
        )
    )
    fig.update_layout(
        annotations=[
            {
                'text': fr'$\theta$',
                'xref':"paper",
                'yref':"paper",
                'x': -.15,
                'y': .5,
                'showarrow': False,
                'textangle': 0,
                'xanchor':"left",
                'yanchor':"bottom",
                'font': dict(size=14)
            }
        ]
    )
    fig = pu.plot_theme(fig)

    return fig



def plot_2dsurf_const_phi(xtarget,ytarget,ztarget, outerflux_xdata, outerflux_ydata, phi_curr, label, units, params, xrange=None, yrange=None):


    xtarget = xtarget[0,:]
    ytarget = ytarget[:,0]

    colorbartitle = rf'${label} \ \ ({units})$'
    title=fr'${label} \ \text{{at toroidal angle }} \phi={phi_curr:.3f}\pi$'

    fig = go.Figure(go.Heatmap(x=xtarget, 
                               y=ytarget, 
                               z= ztarget, 
                               colorscale='Viridis')
        )
    fig.add_trace(go.Scatter(x = outerflux_xdata,
                             y = outerflux_ydata,
                               mode='lines',
                               line=dict(color='black', width=2))
        )
    
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'y': 0.85,
        },
         xaxis=dict(
            title=dict(
                text="R (m)"
            )
        )
    )
    fig.update_layout(
            annotations=[
                {
                    'text': 'Z (m)',
                    'xref':"paper",
                    'yref':"paper",
                    'x': -.15,
                    'y': .5,
                    'showarrow': False,
                    'textangle': 0,
                    'xanchor':"left",
                    'yanchor':"bottom",
                    'font': dict(size=14)
                }
            ]
        )
    fig.add_annotation(
            text=colorbartitle,
            showarrow=False,
            xref="paper", yref="paper",
            x=1.0, y=1.0,  
            xanchor="left", yanchor="bottom"
        )
    if np.any(xrange):
         fig.update_layout(xaxis=dict(range=xrange))
    
    if np.any(yrange):
         fig.update_layout(yaxis=dict(range=yrange))

    fig = pu.plot_theme(fig)

    return fig



def plot_3dmagax(eq_index,curve_data, hovertemplate, params):
    attrs_list = ['X','Y','Z'] + params.attrs_mag_axis
    plot_params = pu.compute_3dplot_params(eq_index, params)

    df = pd.DataFrame({attrs_list[i]: curve_data[i] 
                       for i in range(0,len(attrs_list))})

    fig=go.Figure(data=[go.Scatter3d(x=curve_data[0],
                                     y=curve_data[1],
                                     z=curve_data[2], 
                                     mode='lines')]
        )

    fig.update_traces(customdata=df,
                      hovertemplate = hovertemplate
        )

    
    fig.update_layout(title={'text': fr'$\text{{Magnetic axis}}$', 
                             'x': 0.5, 
                             'y': 0.9}
        )
    fig.update_layout(scene = plot_params['scene'], 
                      autosize=False, 
                      width= plot_params['width'], 
                      height=plot_params['height'],
                      scene_camera = plot_params['scene_camera']
        )
    fig.update_layout(scene = {'xaxis_title': 'X (m)', 
                               'yaxis_title': 'Y (m)', 
                               'zaxis_title': 'Z (m)'}
        )

    fig = pu.plot_theme(fig)

    return fig



def plot_3dsurf(color_data, mesh_data, eq_index, quantity, rho_index, params, label_in=None, units_in=None):
    
    if label_in != None:
         label = label_in
    else:
         label = color_data.attrs['_label_']
    
    if units_in != None:
         units = units_in
    else: 
         units=color_data.attrs['_units_']

    plot_params = pu.compute_3dplot_params(eq_index, params)
    rho_curr = round(1/params.surf3d_num_rho * rho_index,3)
    colorbartitle = rf'${label} \ \ ({units})$'
    title = fr'${label} \ \text{{at flux surface }} \rho={rho_curr:.3f}$'
    if quantity=='1':
        title=fr'$\text{{Flux surface at }} \rho={rho_curr:.3f}$'


    fig = go.Figure(
        data=go.Surface(
            x=mesh_data[0][:,0,:],         
            y=mesh_data[1][:,0,:],         
            z=mesh_data[2][:,0,:],         
            surfacecolor=color_data[:][:,0,:],     
            colorscale='Viridis',  
            colorbar=dict(lenmode = 'pixels',
                          len=400)
        )
    )

    fig.update_layout(title={'text': title})
    fig.update_layout(scene = plot_params['scene'], 
                      autosize=False, 
                      width= plot_params['width'], 
                      height=plot_params['height'],
                      scene_camera = plot_params['scene_camera'])
    fig.update_layout(scene = {'xaxis_title': 'X (m)', 
                               'yaxis_title': 'Y (m)', 
                               'zaxis_title': 'Z (m)'})
    fig.update_layout(title_x=.5, title_y=.9)

    
    if quantity == '1':
        fig.update_traces(opacity=.4, showscale=False)
    else:
        fig.add_annotation(
            text=colorbartitle,
            showarrow=False,
            xref="paper", yref="paper",
            x=1.0, y=1.11,  
            xanchor="left", yanchor="bottom"
        )


    fig = pu.plot_theme(fig)

    return fig

















