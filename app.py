from dash import Dash, html, dash_table,dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from params import viz_params

import app_components as ac



#################################################
# Global stuff
#################################################
params = viz_params()
ac.initialize(params)


#################################################
# App layout
#################################################
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = [
    ac.comp_title(),
    ac.comp_eq_dropdown(params),
    html.Hr(),
    ac.comp_tabs(params)
]

#################################################
# Callbacks
#################################################
@callback(
    Output('fig_1Dprofiles','figure'),
    Input('buttons_1Dprofiles', 'value'),
    Input('main_dropdown', 'value')
) 
def update_fig_1Dprofiles(quantity, eq_index):
    return ac.update_figure_1Dprofiles(int(eq_index),quantity,params)

@callback(
    Output('summary-table', 'data'),
    Input('main_dropdown', 'value')
)
def update_table_states(eq_index):
    return ac.update_table_stats(int(eq_index),params)



@callback(
    Output('slider_fluxsurf', 'max'),
    Output('slider_fluxsurf', 'marks'),
    Input('main_dropdown', 'value')
)
def update_slider_fluxsurf(eq_index):
    return ac.update_slider_fluxsurf(int(eq_index),params)

@callback(
    Output('figure_fluxsurf', 'figure'),
    Input('main_dropdown', 'value'),
    Input('slider_fluxsurf', 'value')
)
def update_figure_fluxsurf(eq_index, slider_val):
    return ac.update_figure_fluxsurf(int(eq_index),slider_val, params)
    


#################################################
# Runtime
#################################################
if __name__ == '__main__':
    app.run(debug=True)









