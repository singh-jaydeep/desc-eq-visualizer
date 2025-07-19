#################################################
# Tab 4 plots 3D flux surfaces, densities, and
# the magnetic axis
#################################################

import h5py
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from plotting.plot_utils import borderstyle
from plotting.plot_building import plot_3dsurf, plot_3dmagax


def comp_tab(params):
    div = html.Div(
        [
            dbc.Row(
                [
                    panel_3d_left(params),
                    panel_3d_right(params),
                ]
            )
        ]
    )
    return div


def panel_3d_left(params):
    options = {i: i for i in params.attrs_3d}
    options["1"] = "flux surfaces"
    options["magnetic axis"] = "magnetic axis"

    dropdown = dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Dropdown(
                        options=options,
                        id="dropdown_3d",
                        value=params.attrs_3d[0],
                        style={"margin-top": "20px", "margin-bottom": "20px"},
                    )
                ],
                className="justify-content-center",
                width=6,
            )
        ],
        justify="center",
    )
    column_left = dbc.Col([dropdown, slider_3d(params)], width=3)

    return column_left


def panel_3d_right(params):
    column_right = dbc.Col(
        html.Div(children=[figure_3d()], style={"margin-top": "20px"}), width=6
    )
    return column_right


def figure_3d():
    fig_row = dbc.Row(
        [
            dbc.Col(
                html.Div(
                    children=[dcc.Graph(figure={}, id="fig_3d", mathjax=True)],
                    style=borderstyle(),
                ),
                className="mb-3",
            )
        ]
    )
    return fig_row


def slider_3d(params):
    max = params.surf3d_num_rho - 1
    marks = {i: "" for i in range(0, params.surf3d_num_rho)}
    slider = dcc.Slider(
        min=0,
        max=max,
        step=None,
        marks=marks,
        value=params.surf3d_num_rho - 1,
        id="slider_3d",
    )
    col = dbc.Row(
        [dbc.Col([slider], className="mb-3 align-items-center", width=8)],
        justify="center",
    )
    return col


def update_figure_3dprofiles(eq_index, quantity, slider_val, params):
    if quantity == "magnetic axis":
        with h5py.File(
            params.pp_desc_path + "/pp_" + params.eq_names_list[eq_index], "r"
        ) as f:
            curve_data = f["/3d/magaxis_3d_/magaxis_3d_"]
            hovertemplate = curve_data.attrs["hovertemplate"]
            fig = plot_3dmagax(eq_index, curve_data[:], hovertemplate, params)
    else:
        with h5py.File(
            params.pp_desc_path + "/pp_" + params.eq_names_list[eq_index], "r"
        ) as f:
            color_data = f[
                "/3d/constrho_3d_/"
                + quantity
                + "constrho_3d_"
                + rf"{slider_val+1}/{params.surf3d_num_rho}"
            ]
            fig = plot_3dsurf(
                color_data,
                params.meshes_loaded[slider_val],
                eq_index,
                quantity,
                slider_val + 1,
                params,
            )
    return fig
