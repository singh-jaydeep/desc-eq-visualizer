from dash import Dash, html, dash_table,dcc, callback, Output, Input, State, no_update
import dash_bootstrap_components as dbc
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
    ac.comp_tabs(params),


    dcc.Store(id='dummy-dcc-store'), ## Used only for chaining callbacks
    dcc.Store(id='visited-tabs', data=[])
])

#################################################
# Callbacks
#################################################

###################
# Prelims
###################
@callback(
    Output('dummy-dcc-store', 'data'),
    Output('visited-tabs','data'),
    Output('slider_fluxsurf','value', allow_duplicate=True),
    Output('slider_2d', 'value', allow_duplicate=True),
    Output('slider_3d', 'value', allow_duplicate=True),
    Output('dropdown_1dprofiles_left', 'value', allow_duplicate=True),
    Output('dropdown_1dprofiles_right', 'value', allow_duplicate=True),
    Output('dropdown_2d_whichview', 'value', allow_duplicate=True),
    Output('dropdown_2dprofiles_list', 'value', allow_duplicate=True),
    Output('dropdown_3d', 'value', allow_duplicate=True),
    Input('submit-eq-button', 'n_clicks'),
    State('main_dropdown', 'value'),
    prevent_initial_call=True
)
def load_equilibrium(_,eq_index):
    ac.load_meshes(int(eq_index),params)
    ac.load_cached_figures(int(eq_index),params)
    return_list = [0, []]
    return_list += ac.reset_sliders(params)
    return_list += ac.reset_dropdowns(params)
    return return_list
    

###################
# Code to initialize 
# a tab after selected
###################
@callback(
    Output('figure_fluxsurf', 'figure', allow_duplicate=True),
    Output('figure_2d', 'figure', allow_duplicate=True),
    Output('fig_3d', 'figure', allow_duplicate=True),
    Output('visited-tabs','data', allow_duplicate=True),
    Input('tabs', 'active_tab'),
    Input('dummy-dcc-store', 'data'),
    State('visited-tabs','data'),
    prevent_initial_call=True
)
def load_tab(active_tab, _, visited_tabs):
    if active_tab in visited_tabs:
        return no_update, no_update, no_update, visited_tabs
    else:
        visited_tabs.append(active_tab)
        if active_tab == 'tab1':
            return no_update, no_update, no_update, visited_tabs
        elif active_tab == 'tab2':
            return no_update, no_update, no_update, visited_tabs
        elif active_tab == 'tab3':
            figA = params.cached_figures['fluxsurfaces_2d_']
            figA.update_layout(title_x=.5, title_y=.85)
            figB = params.cached_figures['constrho_2d_']
            figB.update_layout(title_x=.5, title_y=.85)
            return figA, figB, no_update, visited_tabs
        elif active_tab == 'tab4':
            fig = params.cached_figures['fluxsurfaces_3d_']
            fig.update_layout(title_x=.5, title_y=.9)
            return no_update, no_update, fig, visited_tabs
        else:
            return no_update, no_update, no_update, visited_tabs
        
    

###################
# Tab 1
###################
@callback(
    Output('summary-table', 'data'),
    Output('summary-table', 'tooltip_data'),
    Input('dummy-dcc-store', 'data'),
    State('main_dropdown', 'value')
)
def update_table_states(_,eq_index):
    return ac.update_table_stats(int(eq_index),params)

###################
# Tab 2
###################
@callback(
    Output('fig_1dprofiles_left','figure'),
    Input('dropdown_1dprofiles_left', 'value'),
    Input('dummy-dcc-store', 'data'),
    State('main_dropdown', 'value')
) 
def update_fig_1dprofiles(quantity, _, eq_index):
    return ac.update_figure_1dprofiles(int(eq_index),quantity,params)

@callback(
    Output('fig_1dprofiles_right','figure'),
    Input('dropdown_1dprofiles_right', 'value'),
    Input('dummy-dcc-store', 'data'),
    State('main_dropdown', 'value')
) 
def update_fig_1dprofiles(quantity,_, eq_index):
    return ac.update_figure_1dprofiles(int(eq_index),quantity,params)

###################
# Tab 3
###################

@callback(
    Output('figure_fluxsurf', 'figure'),
    Input('slider_fluxsurf', 'value'),
    Input('dummy-dcc-store', 'data'),
    State('main_dropdown', 'value')
)
def update_figure_fluxsurf(slider_val,_, eq_index):
    return ac.update_figure_fluxsurf(int(eq_index),slider_val, params)

@callback(
    Output('slider_2d', 'max'),
    Output('slider_2d', 'marks'),
    Output('slider_2d', 'value'),
    Input('dropdown_2d_whichview', 'value')
) 
def update_slider_2dprofiles(view):
    return ac.update_slider_2dprofiles(view,params)

@callback(
    Output('figure_2d', 'figure'),
    Input('dropdown_2d_whichview', 'value'),
    Input('dropdown_2dprofiles_list','value'),
    Input('slider_2d', 'value'),
    Input('dummy-dcc-store', 'data'),
    State('main_dropdown', 'value')
    
) 
def update_figure_2dprofiles(view, quantity, slider_val,_, eq_index):
    return ac.update_figure_2dprofiles(int(eq_index),view, quantity, slider_val,params)

###################
# Tab 4
###################
@callback(
    Output('fig_3d', 'figure'),
    Input('dropdown_3d','value'),
    Input('slider_3d', 'value'),
    Input('dummy-dcc-store', 'data'),
    State('main_dropdown', 'value')
) 
def update_figure_3dprofiles(quantity, slider_val,_, eq_index):
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














