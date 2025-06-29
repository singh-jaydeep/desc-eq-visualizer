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
app = Dash(external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div([
    ac.comp_title(),
    ac.comp_eq_dropdown(params),
    html.Hr(),
    ac.comp_tabs(params)
])

#################################################
# Callbacks
#################################################


###################
# Tab 1
###################
@callback(
    Output('summary-table', 'data'),
    Input('main_dropdown', 'value')
)
def update_table_states(eq_index):
    return ac.update_table_stats(int(eq_index),params)

###################
# Tab 2
###################
@callback(
    Output('fig_1dprofiles_left','figure'),
    Input('dropdown_1dprofiles_left', 'value'),
    Input('main_dropdown', 'value')
) 
def update_fig_1dprofiles(quantity, eq_index):
    return ac.update_figure_1dprofiles(int(eq_index),quantity,params)

@callback(
    Output('fig_1dprofiles_right','figure'),
    Input('dropdown_1dprofiles_right', 'value'),
    Input('main_dropdown', 'value')
) 
def update_fig_1dprofiles(quantity, eq_index):
    return ac.update_figure_1dprofiles(int(eq_index),quantity,params)

###################
# Tab 3
###################
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

@callback(
    Output('slider_2d', 'max'),
    Output('slider_2d', 'marks'),
    Input('main_dropdown', 'value'),
    Input('dropdown_2d_whichview', 'value')
) 
def update_slider_2dprofiles(eq_index, view):
    return ac.update_slider_2dprofiles(int(eq_index),view,params)

@callback(
    Output('figure_2d', 'figure'),
    Input('main_dropdown', 'value'),
    Input('dropdown_2d_whichview', 'value'),
    Input('dropdown_2dprofiles_list','value'),
    Input('slider_2d', 'value'),
) 
def update_figure_2dprofiles(eq_index, view, quantity, slider_val):
    return ac.update_figure_2dprofiles(int(eq_index),view, quantity, slider_val,params)

###################
# Tab 4
###################
@callback(
    Output('fig_3d', 'figure'),
    Input('main_dropdown', 'value'),
    Input('dropdown_3d','value'),
    Input('slider_3d', 'value'),
) 
def update_figure_3dprofiles(eq_index,quantity, slider_val):
    fig = ac.update_figure_3dprofiles(int(eq_index), quantity, slider_val, params)
    return fig



@callback(
    Output('slider_3d', 'disabled'),
    Input('dropdown_3d', 'value')
)
def disable_slider_if_axis(quantity):
    return quantity == 'magnetic axis'




#################################################
# Runtime
#################################################
if __name__ == '__main__':
    app.run(debug=True)














