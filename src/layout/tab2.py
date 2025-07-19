#################################################
# Tab 2 plots functions of rho
#################################################
import h5py
from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from plotting.plot_utils import borderstyle
from plotting.plot_building import plot_1d


def comp_tab(params):
    div = html.Div(
        [
            dbc.Row(
                [
                    panel_1dprofiles_left(params),
                    panel_1dprofiles_right(params),
                ],
                justify="center",
            )
        ]
    )
    return div


def panel_1dprofiles_left(params):
    dropdown = dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Dropdown(
                        options={i: i for i in params.attrs_profiles},
                        id="dropdown_1dprofiles_left",
                        value=params.attrs_profiles[0],
                        style={"margin-bottom": "20px", "margin-top": "20px"},
                    )
                ],
                className="justify-content-center",
                width=3,
            )
        ],
        justify="center",
    )
    column_left = dbc.Col([dropdown, figure_1dprofiles_left()], width=5)

    return column_left


def panel_1dprofiles_right(params):
    dropdown = dbc.Row(
        [
            dbc.Col(
                [
                    dcc.Dropdown(
                        options={i: i for i in params.attrs_profiles},
                        id="dropdown_1dprofiles_right",
                        value=params.attrs_profiles[1],
                        style={"margin-bottom": "20px", "margin-top": "20px"},
                    )
                ],
                className="justify-content-center",
                width=3,
            )
        ],
        justify="center",
    )
    column_right = dbc.Col([dropdown, figure_1dprofiles_right()], width=5)
    return column_right


def figure_1dprofiles_left():
    fig_row_left = dbc.Row(
        [
            dbc.Col(
                html.Div(
                    dcc.Graph(figure={}, id="fig_1dprofiles_left", mathjax=True),
                    style=borderstyle(),
                ),
                className="mb-3 align-items-center",
            )
        ]
    )
    return fig_row_left


def figure_1dprofiles_right():
    fig_row_right = dbc.Row(
        [
            dbc.Col(
                html.Div(
                    dcc.Graph(figure={}, id="fig_1dprofiles_right", mathjax=True),
                    style=borderstyle(),
                ),
                className="mb-3 align-items-center",
            )
        ]
    )
    return fig_row_right


## Tab 2 Update, triggered by callback
def update_figure_1dprofiles(eq_index, quantity, params):
    with h5py.File(
        params.pp_desc_path + "/pp_" + params.eq_names_list[eq_index], "r"
    ) as f:
        data = f[f"/1d/" + quantity + "_1d_"]
        label = data.attrs["_label_"]
        return plot_1d(data[:], label, params)
