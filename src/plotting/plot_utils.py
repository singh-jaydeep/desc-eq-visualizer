#####################################################
# Functions to aid in building/styling plots
#####################################################


from desc.equilibrium.equilibrium import EquilibriaFamily
import numpy as np


def plot_theme(fig, change_grid=0):
    fig.update_layout(
        paper_bgcolor="#2c3034",
        plot_bgcolor="#2c3034",
        font_color="white",
        font_family="Times New Roman",
    )
    if change_grid > 0:
        fig.update_xaxes(gridcolor="lightgray", gridwidth=0.5)
        fig.update_yaxes(gridcolor="lightgray", gridwidth=0.5)
    return fig


def borderstyle():
    return {
        "border": "1px solid #495057",
        "border-radius": "4px",
        "padding": "5px",
        "backgroundColor": "#2c3034",
    }


def compute_3dplot_params(eq_index, params):
    eq = params.eq_loaded[eq_index]

    if isinstance(eq, EquilibriaFamily):
        eq = eq[-1]  ## take the final entry

    plot_params = {}

    coord_r = eq.compute("R")["R"]
    coord_z = eq.compute("Z")["Z"]
    xyrange = 1.2 * np.max(np.abs(coord_r))
    zrange = 1.2 * np.max(np.abs(coord_z))
    inv_ar = 1 / float(eq.compute("R0/a")["R0/a"])

    plot_params["scene"] = dict(
        aspectmode="manual",
        aspectratio={"x": 1, "y": 1, "z": inv_ar},
        xaxis=dict(range=[-xyrange, xyrange], autorange=False),
        yaxis=dict(range=[-xyrange, xyrange], autorange=False),
        zaxis=dict(range=[-zrange, zrange], autorange=False),
    )
    plot_params["height"] = 500
    plot_params["width"] = 700
    plot_params["scene_camera"] = dict(eye=dict(x=0.8, y=0.8, z=0.7))

    return plot_params
