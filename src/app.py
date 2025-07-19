from dash import Dash, html, dcc, callback, Output, Input, State, no_update
import dash_bootstrap_components as dbc


from params_class import Params
import layout.main_layout as layout
import layout.initialization as init
from layout import tab1, tab2, tab3, tab4


#################################################
# Global stuff
#################################################
params = Params()
init.initialize(params)


#################################################
# App layout
#################################################
app = Dash(external_stylesheets=[dbc.themes.DARKLY])

app.layout = html.Div(
    [
        layout.comp_title(),
        layout.comp_eq_dropdown(params),
        html.Hr(),
        layout.comp_tabs(params),
        dcc.Store(id="dummy-dcc-store"),  ## Used only for chaining callbacks
        dcc.Store(id="visited-tabs", data=[]),
    ]
)


#################################################
# Callbacks
#################################################


###################
# After equilibrium
# is selected
###################
@callback(
    Output("dummy-dcc-store", "data"),
    Output("visited-tabs", "data"),
    Output("slider_fluxsurf", "value", allow_duplicate=True),
    Output("slider_2d", "value", allow_duplicate=True),
    Output("slider_3d", "value", allow_duplicate=True),
    Output("dropdown_1dprofiles_left", "value", allow_duplicate=True),
    Output("dropdown_1dprofiles_right", "value", allow_duplicate=True),
    Output("dropdown_2d_whichview", "value", allow_duplicate=True),
    Output("dropdown_2dprofiles_list", "value", allow_duplicate=True),
    Output("dropdown_3d", "value", allow_duplicate=True),
    Input("submit-eq-button", "n_clicks"),
    State("main_dropdown", "value"),
    prevent_initial_call=True,
)
def load_equilibrium(_, eq_index):
    init.load_meshes(int(eq_index), params)
    init.load_cached_figures(int(eq_index), params)
    return_list = [0, []]
    return_list += init.reset_sliders(params)
    return_list += init.reset_dropdowns(params)
    return return_list


###################
# After tab is
# visited for first time
###################
@callback(
    Output("fig_1dprofiles_left", "figure", allow_duplicate=True),
    Output("fig_1dprofiles_right", "figure", allow_duplicate=True),
    Output("figure_fluxsurf", "figure", allow_duplicate=True),
    Output("figure_2d", "figure", allow_duplicate=True),
    Output("fig_3d", "figure", allow_duplicate=True),
    Output("visited-tabs", "data", allow_duplicate=True),
    Input("tabs", "active_tab"),
    Input("dummy-dcc-store", "data"),
    State("visited-tabs", "data"),
    prevent_initial_call=True,
)
def load_tab(active_tab, _, visited_tabs):
    return_list = [no_update for i in range(0, 5)] + [visited_tabs]

    if active_tab in visited_tabs:
        return return_list
    else:
        return_list[-1].append(active_tab)
        if active_tab == "tab1":
            pass  ## Add tab1 specific code if needed
        if active_tab == "tab2":
            return_list[0] = params.cached_figures["profile_1d_A"]
            return_list[0].update_layout(title_x=0.5, title_y=0.93)
            return_list[1] = params.cached_figures["profile_1d_B"]
            return_list[1].update_layout(title_x=0.5, title_y=0.93)
        elif active_tab == "tab3":
            return_list[2] = params.cached_figures["fluxsurfaces_2d_"]
            return_list[2].update_layout(title_x=0.5, title_y=0.85)
            return_list[3] = params.cached_figures["constrho_2d_"]
            return_list[3].update_layout(title_x=0.5, title_y=0.85)
        elif active_tab == "tab4":
            return_list[4] = params.cached_figures["fluxsurfaces_3d_"]
            return_list[4].update_layout(title_x=0.5, title_y=0.9)

        return return_list


###################
# Tab 1
###################
@callback(
    Output("summary-table", "data"),
    Output("summary-table", "tooltip_data"),
    Input("dummy-dcc-store", "data"),
    State("main_dropdown", "value"),
)
def update_table_states(_, eq_index):
    return tab1.update_table_stats(int(eq_index), params)


###################
# Tab 2
###################
@callback(
    Output("fig_1dprofiles_left", "figure"),
    Input("dropdown_1dprofiles_left", "value"),
    Input("dummy-dcc-store", "data"),
    State("main_dropdown", "value"),
)
def update_fig_1dprofiles(quantity, _, eq_index):
    return tab2.update_figure_1dprofiles(int(eq_index), quantity, params)


@callback(
    Output("fig_1dprofiles_right", "figure"),
    Input("dropdown_1dprofiles_right", "value"),
    Input("dummy-dcc-store", "data"),
    State("main_dropdown", "value"),
)
def update_fig_1dprofiles(quantity, _, eq_index):
    return tab2.update_figure_1dprofiles(int(eq_index), quantity, params)


###################
# Tab 3
###################


@callback(
    Output("figure_fluxsurf", "figure"),
    Input("slider_fluxsurf", "value"),
    Input("dummy-dcc-store", "data"),
    State("main_dropdown", "value"),
)
def update_figure_fluxsurf(slider_val, _, eq_index):
    return tab3.update_figure_fluxsurf(int(eq_index), slider_val, params)


@callback(
    Output("slider_2d", "max"),
    Output("slider_2d", "marks"),
    Output("slider_2d", "value"),
    Input("dropdown_2d_whichview", "value"),
)
def update_slider_2dprofiles(view):
    return tab3.update_slider_2dprofiles(view, params)


@callback(
    Output("figure_2d", "figure"),
    Input("dropdown_2d_whichview", "value"),
    Input("dropdown_2dprofiles_list", "value"),
    Input("slider_2d", "value"),
    Input("dummy-dcc-store", "data"),
    State("main_dropdown", "value"),
)
def update_figure_2dprofiles(view, quantity, slider_val, _, eq_index):
    return tab3.update_figure_2dprofiles(
        int(eq_index), view, quantity, slider_val, params
    )


###################
# Tab 4
###################
@callback(
    Output("fig_3d", "figure"),
    Input("dropdown_3d", "value"),
    Input("slider_3d", "value"),
    Input("dummy-dcc-store", "data"),
    State("main_dropdown", "value"),
)
def update_figure_3dprofiles(quantity, slider_val, _, eq_index):
    fig = tab4.update_figure_3dprofiles(int(eq_index), quantity, slider_val, params)
    return fig


@callback(Output("slider_3d", "disabled"), Input("dropdown_3d", "value"))
def disable_slider_if_axis(quantity):
    return quantity == "magnetic axis"


#################################################
# Runtime
#################################################
if __name__ == "__main__":
    app.run(debug=True)
