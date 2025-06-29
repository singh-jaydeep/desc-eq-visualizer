import plotly.express as px
import plotly.graph_objects as go
import plotly
from desc.plotting import plot_surfaces
import numpy as np

def plotly_plot_fluxsurf(xdata1, ydata1, xdata2, ydata2, phi_index, eq_NFP, params): 
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
    

    phi_curr = np.round(2*phi_index/params.fx_num_phi*eq_NFP,3)

    fig.update_layout(
        title={
            'text': fr"$\text{{Flux surfaces at toroidal angle }} \phi = {phi_curr}\pi$",
            'x': 0.5,
            'y': 0.85,
        },
        xaxis=dict(
            title=dict(
                text="R"
            )
        )
    )
    fig.update_layout(
        annotations=[
            {
                'text': 'Z',
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
    


def plotly_plot_2dsurf_const_rho(data, quantity, rho_index, params):
    fig = go.Figure()
    ############
    # FIX #
    numtheta = 2*params.grid_const_rho_args["M"]+1
    numzeta = 2*params.grid_const_rho_args["N"]+1
    thetadata = np.linspace(0,2*3.14159, numtheta)
    zetadata = np.linspace(0, 2*3.14159, numzeta)
    ############
    fig.add_heatmap(autocolorscale=False, colorscale='plasma', y=thetadata, x=zetadata, z=data) ## Check order

    rho_curr = round(1/params.surf2d_num_rho * rho_index,3)
    title = fr'${params.attrs_label_dict[quantity]} \ \text{{at flux surface }} \rho={rho_curr}$'

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


def plotly_plot_2dsurf_const_phi(xdata,ydata,zdata, quantity, phi_index, eq_NFP, params):
    fig = go.Figure(data=[
                    go.Surface(
                        x=xdata,
                        y=ydata,
                        z=np.zeros_like(zdata),  
                        surfacecolor=zdata,      
                        showscale=True
                    )
        ])
    phi_curr = round(2*np.pi/(params.surf2d_num_phi*eq_NFP) * phi_index,3)
    title=fr'${params.attrs_label_dict[quantity]} \ \text{{at toroidal angle }} \phi={phi_curr}\pi$'
    fig.update_layout(
        scene_camera=dict(eye=dict(x=0., y=0., z=2.)),
        scene_dragmode=False,  
        scene=dict(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            zaxis=dict(visible=False)
        ),
        title={
            'text': title,
            'x': 0.5,
            'y': 0.85,
        },
    )
    return plot_theme(fig)
    


def plotly_plot_3dsurf(fig, eq_index, quantity, rho_index, params):
    plot_params = compute_3dplot_params(eq_index, quantity, rho_index, params)
    fig.data[0].update(colorbar=plot_params['colorbar'])
    
    fig.update_layout(title={'text': plot_params['title'], 'x': 0.45, 'y': 0.9})
    fig.update_layout(scene = plot_params['scene'], autosize=False, width= plot_params['width'], height=plot_params['height'],
                      scene_camera = plot_params['scene_camera'])
    
    if quantity == '1':
        fig.update_traces(opacity=.4, showscale=False)


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


def compute_3dplot_params(eq_index,quantity, rho_index, params):
    eq = params.eq_loaded[eq_index]
    plot_params = {}
    rho_curr = round(1/params.surf3d_num_rho * rho_index,3)

    if quantity == '1':
        plot_params['title'] = fr'$\text{{Flux surface }} \rho={rho_curr}$'
    elif quantity == 'magnetic axis':
        plot_params['title'] = fr'$\text{{Magnetic axis}}$'
    else:
        plot_params['title'] = fr'${params.attrs_label_dict[quantity]} \ \text{{at flux surface }} \rho={rho_curr}$'

    plot_params['colorbar'] = dict(
        lenmode = 'pixels',
        len = 400
    )
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


