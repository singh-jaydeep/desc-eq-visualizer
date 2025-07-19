from dash import html, dcc, callback
import dash_bootstrap_components as dbc
from desc.compute import data_index
from desc.compute.utils import _parse_parameterization


from . import tab1, tab2, tab3, tab4


## Main title
def comp_title():
    div = html.Div(
        dbc.Row(
            dbc.Col(
                "DESC Visualization Dashboard",
                width=12,
                className="mb-4 mt-4 ms-3",
                style={
                    "color": "white",
                    "fontSize": 25,
                },
            )
        )
    )
    return div


## dropdown with list of equilibria, and selection button
def comp_eq_dropdown(params):
    indices = range(0, len(params.eq_names_list))
    options = {i: params.eq_names_list[i].removesuffix(".h5") for i in indices}
    button = dbc.Col(
        dbc.Button(
            "Submit",
            id="submit-eq-button",
            color="secondary",  # choose color: "secondary", "info", etc.
            className="me-1",
            n_clicks=0,
        ),
        width=4,
    )
    dropdown = dbc.Col(
        [
            dcc.Dropdown(
                options=options,
                id="main_dropdown",
                value="0",
                style={
                    "margin-bottom": "20px",
                    "margin-left": "10px",
                },
            )
        ],
        className="justify-content-center",
        width=2,
    )
    div = dbc.Row([dropdown, button])
    return div


def comp_tabs(params):
    div = dbc.Row(
        [
            dbc.Col(
                [
                    dbc.Tabs(
                        [
                            dbc.Tab(
                                label="Summary Statistics",
                                tab_id="tab1",
                                children=[tab1.comp_tab()],
                            ),
                            dbc.Tab(
                                label="1D Profiles",
                                tab_id="tab2",
                                children=[tab2.comp_tab(params)],
                            ),
                            dbc.Tab(
                                label="Cross sections",
                                tab_id="tab3",
                                children=[tab3.comp_tab(params)],
                            ),
                            dbc.Tab(
                                label="3D Views",
                                tab_id="tab4",
                                children=[tab4.comp_tab(params)],
                            ),
                        ],
                        id="tabs",
                        active_tab="tab1",
                        style=dict(color="primary"),
                    )
                ],
                width=12,
            )
        ]
    )
    return div
