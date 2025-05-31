from dash import Dash, html, dash_table,dcc, callback, Output, Input, State
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from params import viz_params
import pandas as pd
import app_components as ac
from desc.grid import LinearGrid


def update_figure_1Dprofiles(eq_index,quantity,params):
    data = params.pp_eq_loaded[eq_index][quantity]
    rho_grid = params.grid_profiles
    df = pd.DataFrame(dict(
        x=rho_grid,
        y=data
    ))
    fig = px.line(df, x='x', y='y')
    return fig





params = viz_params()
ac.initialize(params)
data = params.pp_eq_loaded[0]['iota']
rho_grid = params.grid_profiles
df = pd.DataFrame(dict(
    x=rho_grid,
    y=data
))
fig = px.line(df, x='x', y='y')
#fig = update_figure_1Dprofiles(0,'iota',params)
print(rho_grid.nodes[:,0])
print(data)
#fig.show()