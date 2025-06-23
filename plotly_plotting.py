import plotly.express as px
import plotly.graph_objects as go
import plotly
from desc.plotting import plot_surfaces
import numpy as np

def plotly_plot_fluxsurf(xdata1, ydata1, xdata2, ydata2, params): 
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
    fig.update_layout(
        title = dict(
            text='Flux surfaces with [??]'
        )
    )

    return fig 
    

def plotly_plot_2dsurf_const_rho(data, params):
    fig = go.Figure()
    ############
    # FIX #
    numtheta = 2*params.grid_const_rho_args["M"]+1
    numzeta = 2*params.grid_const_rho_args["N"]+1
    thetadata = np.linspace(0,2*3.14159, numtheta)
    zetadata = np.linspace(0, 2*3.14159, numzeta)
    ############
    fig.add_heatmap(autocolorscale=True, y=thetadata, x=zetadata, z=data) ## Check order
    return fig


def plotly_plot_2dsurf_const_phi(xdata,ydata,zdata, params):
    fig = go.Figure(data=[
                    go.Surface(
                        x=xdata,
                        y=ydata,
                        z=np.zeros_like(zdata),  
                        surfacecolor=zdata,      
                        colorscale='Viridis',
                        #cmin=np.min(zdata),
                        #cmax=np.max(zdata),
                        showscale=True
                    )
        ])
    fig.update_layout(
        scene_camera=dict(eye=dict(x=0., y=0., z=2.)),
        scene_dragmode=False,  
        scene=dict(
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            zaxis=dict(visible=False)
        )   
    )
    return fig
    

    