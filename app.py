from dash import Dash, html, dash_table,dcc, callback, Output, Input, State
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
app = Dash()
app.layout = [
    ac.comp_title(),
    ac.comp_eq_dropdown(params),
    html.Hr(),
    ac.comp_buttons_1Dprofiles(params),
    ac.comp_figure_1Dprofiles(),
]

#################################################
# Callbacks
#################################################
@callback(
    Output('fig_1Dprofiles','figure'),
    Input('buttons_1Dprofiles', 'value'),
    State('dropdown_eqlist', 'value')
) 
def update_fig_1Dprofiles(quantity, eq_index):
    return ac.update_figure_1Dprofiles(int(eq_index),quantity,params)


#################################################
# Runtime
#################################################
if __name__ == '__main__':
    app.run(debug=True)









