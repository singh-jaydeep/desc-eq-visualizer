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
                                    color='blue',
                                    width=3
                                )))
        fig.update_traces(showlegend=False)
    for i in range(0,params.fx_num_theta):
        fig.add_trace(go.Scatter(x=xdata2[:,i], y= ydata2[:,i], 
                                mode = 'lines',
                                line = dict(
                                    color='black',
                                    width=2,
                                    dash='dash'
                                )))
        fig.update_traces(showlegend=False)
    
    
    num = 2*phi_index
    denom = params.fx_num_phi*eq_NFP

    fig.update_layout(
        title={
            'text': fr"$\text{{Flux surfaces at toroidal angle }} \phi = \frac{{{num}}}{{{denom}}}\pi$",
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
    

    return fig 
    


def plotly_plot_2dsurf_const_rho(data, quantity, rho_index, params):
    fig = go.Figure()
    ############
    # FIX #
    numtheta = 2*params.grid_const_rho_args["M"]+1
    numzeta = 2*params.grid_const_rho_args["N"]+1
    thetadata = np.linspace(0,2*3.14159, numtheta)
    zetadata = np.linspace(0, 2*3.14159, numzeta)
    ############
    fig.add_heatmap(autocolorscale=True, y=thetadata, x=zetadata, z=data) ## Check order

    rho_curr = round(1/params.surf2d_num_rho * rho_index,3)
    title = fr'${params.attrs_label_dict[quantity]} \ \text{{at fixed flux surface }} \rho={rho_curr}$'

    fig.update_layout(
        title={
            'text': title,
            'x': 0.5,
            'y': 0.85,
        },
        xaxis=dict(
            title=dict(
                text= fr'$\zeta$'
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



    return fig


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
    title=fr'${params.attrs_label_dict[quantity]} \ \text{{at fixed toroidal angle }} \phi={phi_curr}\pi$'
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
    return fig
    


def plotly_plot_3dsurf(fig, quantity, rho_index, params):
    fig.data[0].update(colorbar=dict(
        lenmode = 'pixels',
        len = 400
    ))
    rho_curr = round(1/params.surf3d_num_rho * rho_index,3)
    title = fr'${params.attrs_label_dict[quantity]} \ \text{{at fixed flux surface }} \rho={rho_curr}$'
    fig.update_layout(title={
            'text': title,
            'x': 0.5,
            'y': 0.85,
            },
            scene_camera=dict(eye=dict(x=2., y=2., z=2.))
    )
    return fig