import plotly.graph_objects as go
from desc.plotting import plot_surfaces
from desc.equilibrium.equilibrium import EquilibriaFamily
import numpy as np
import pandas as pd

def plotly_plot_fluxsurf(xdata1, ydata1, xdata2, ydata2, phi_curr, params): 
            ## takes in the R, Z data at constant phi, returns figure
    fig = go.Figure()
    for i in range(0,params.fx_num_rho):
        fig.add_trace(go.Scatter(x=xdata1[:,i], y= ydata1[:,i], 
                                mode = 'lines',
                                line = dict(
                                    color="#030E4D",
                                    width=3
                                )))
        fig.update_traces(showlegend=False)
    for i in range(0,params.fx_num_theta):
        fig.add_trace(go.Scatter(x=xdata2[:,i], y= ydata2[:,i], 
                                mode = 'lines',
                                line = dict(
                                    color="#000000",
                                    width=2,
                                    dash='dash'
                                )))
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
    

    return plot_theme(fig)
    


def plotly_plot_2dsurf_const_rho(data, label, rho_curr, params):
    fig = go.Figure()

    numtheta = 2*params.grid_const_rho_args["M"]+1
    numzeta = 2*params.grid_const_rho_args["N"]+1
    thetadata = np.linspace(0,2*3.14159, numtheta)
    zetadata = np.linspace(0, 2*3.14159, numzeta)

    fig.add_heatmap(autocolorscale=False, colorscale='plasma', y=thetadata, x=zetadata, z=data) ## Check order

    title = fr'${label} \ \text{{at flux surface }} \rho={rho_curr:.3f}$'

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



    return plot_theme(fig)



def plotly_plot_2dsurf_const_phi(xtarget,ytarget,ztarget, outerflux_xdata, outerflux_ydata, phi_curr, label, params):
    xtarget = xtarget[0,:]
    ytarget = ytarget[:,0]

    fig = go.Figure(go.Heatmap(x=xtarget, y=ytarget, z= ztarget, colorscale='Viridis'))
    fig.add_trace(go.Scatter(
        x = outerflux_xdata,
        y = outerflux_ydata,
        mode='lines',
        line=dict(color='black', width=2)
    ))
    title=fr'${label} \ \text{{at toroidal angle }} \phi={phi_curr:.3f}\pi$'
    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'y': 0.85,
        }
    )
    return plot_theme(fig)



def plotly_plot_3dmagax(eq_index,curve_data, hovertemplate, params):
    attrs_list = ['X','Y','Z'] + params.attrs_mag_axis
    df = pd.DataFrame({attrs_list[i]: curve_data[i] for i in range(0,len(attrs_list))})

    fig=go.Figure(data=[go.Scatter3d(x=curve_data[0],y=curve_data[1],z=curve_data[2], mode='lines')])

    fig.update_traces(
        customdata=df,
        hovertemplate = hovertemplate
    )

    plot_params = compute_3dplot_params(eq_index, params)
    fig.update_layout(title={'text': fr'$\text{{Magnetic axis}}$', 'x': 0.5, 'y': 0.9})
    fig.update_layout(scene = plot_params['scene'], 
                      autosize=False, 
                      width= plot_params['width'], 
                      height=plot_params['height'],
                      scene_camera = plot_params['scene_camera']
                      )
    fig.update_layout(scene = {'xaxis_title': 'X (m)', 'yaxis_title': 'Y (m)', 'zaxis_title': 'Z (m)'})


    return plot_theme(fig)



def plotly_plot_3dsurf(color_data, mesh_data, eq_index, quantity, rho_index, params, label_in=None, units_in=None):
    
    if label_in != None:
         label = label_in
    else:
         label = color_data.attrs['_label_']
    
    if units_in != None:
         units = units_in
    else: 
         units=color_data.attrs['_units_']

    plot_params = compute_3dplot_params(eq_index, params)
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
    fig.update_layout(scene = {'xaxis_title': 'X (m)', 'yaxis_title': 'Y (m)', 'zaxis_title': 'Z (m)'})
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


    return plot_theme(fig)



def plot_theme(fig):
    fig.update_layout(
        paper_bgcolor='#2c3034',
        plot_bgcolor='#2c3034',
        font_color='white',
        font_family='Times New Roman'
    )
    return fig

def borderstyle():
    return {'border': '1px solid #495057',   
            'border-radius': '4px',
            'padding': '5px',
            'backgroundColor': '#2c3034'}




def compute_3dplot_params(eq_index, params):
    eq = params.eq_loaded[eq_index]
    if isinstance(eq, EquilibriaFamily): ## If an equilibrium family, only take the final entry
                eq = eq[-1]
    plot_params = {}


    
    coord_r = eq.compute('R')['R']
    coord_z = eq.compute('Z')['Z']
    xyrange = 1.2*np.max(coord_r)
    zrange = 1.2*np.max(coord_z)
    inv_ar = 1/float(eq.compute('R0/a')['R0/a'])

    plot_params['scene'] = dict(aspectmode='manual', aspectratio = {'x': 1, 'y':1, 'z': inv_ar},
                                xaxis = dict(range=[- xyrange, xyrange], autorange=False),
                                yaxis = dict(range=[- xyrange , xyrange], autorange=False),
                                zaxis = dict(range=[- zrange, zrange], autorange=False))
    plot_params['height'] = 500
    plot_params['width'] = 700

    plot_params['scene_camera'] = dict(eye=dict(x=.8, y=.8, z=.7))


    return plot_params







