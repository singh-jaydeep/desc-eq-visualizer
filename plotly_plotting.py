import plotly.express as px
import plotly.graph_objects as go
import plotly
from desc.plotting import plot_surfaces

def plotly_plot_surface(xdata1, ydata1, xdata2, ydata2, params): 
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
    