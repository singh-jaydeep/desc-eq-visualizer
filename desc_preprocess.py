import desc
import os
import gzip, json
import h5py
from params import viz_params

import matplotlib.pyplot as plt

import numpy as np

import plotly
from plotly_plotting import plotly_plot_fluxsurf, plotly_plot_2dsurf_const_rho, plotly_plot_2dsurf_const_phi, plotly_plot_3dsurf
import plotly.graph_objects as go

from desc.equilibrium import Equilibrium
from desc.grid import LinearGrid
from desc.plotting import plot_surfaces, plot_2d, plot_section, plot_3d
from desc.compute.utils import _parse_parameterization
from desc.compute import data_index





def precompute():
    params = viz_params()
    paths_list(params)
    num_eq = len(params.eq_loaded)
    if num_eq == 0:
        print("No equilibria to preprocess")
        return
    else:
        print(f"{num_eq} equilibria to preprocess")
        build_label_dict(params)
        for i in range(0, len(params.eq_loaded)):
            data_array = compute_quantities(i,params)
            figure_list_fluxsurf = compute_fluxsurfaces(i, params)
            figure_list_2dplots_const_rho = compute_2dsurfaces_const_rho(i,params)
            figure_list_2dplots_const_phi = compute_2dsurfaces_const_phi(i,params)
            figure_list_3dplots = compute_3dsurfaces(i,params)
            figure_list = figure_list_fluxsurf + figure_list_2dplots_const_rho + figure_list_2dplots_const_phi + figure_list_3dplots
            write_json(i,data_array,figure_list,params)


def paths_list(params):
    for item in os.listdir(params.base_desc_path):
        if not os.path.exists(os.path.join(params.pp_desc_path, 'pp_'+item.removesuffix('.h5') + '.json')):
            input_path = os.path.join(params.base_desc_path,item)
            params.eq_loaded.append(desc.io.load(input_path)) ##! Will be a problem with equilibrium families
            params.eq_names_list.append(item.removesuffix('.h5'))


def compute_quantities(eq_index, params):
    eq = params.eq_loaded[eq_index]
    data_array_scalars = []
    for q in params.attrs_scalars:
        computed = eq.compute(q)[q]
        data_array_scalars.append(computed.tolist())
    data_array_profiles=[] 
    grid_profiles = params.grid_profiles
    for q in params.attrs_profiles:
        computed = eq.compute(q, grid_profiles)[q]
        data_array_profiles.append(computed.tolist())
    return [data_array_scalars, data_array_profiles]






def compute_fluxsurfaces(eq_index, params):
    eq = params.eq_loaded[eq_index]

    fig0, _, data = plot_surfaces(eq, rho = params.fx_num_rho, theta = params.fx_num_theta ,phi = params.fx_num_phi, return_data = True)
    plt.close(fig0)

    fig_list_json = []
    for i in range(0,params.fx_num_phi):
        xdata1 = data['rho_R_coords'][:,:,i]
        ydata1 = data['rho_Z_coords'][:,:,i]
        xdata2 = data['vartheta_R_coords'][:,:,i].T
        ydata2 = data['vartheta_Z_coords'][:,:,i].T
        fig_list_json.append(plotly.io.to_json(plotly_plot_fluxsurf(xdata1, ydata1, xdata2, ydata2, i, eq.NFP, params)))

    return [fig_list_json]  

def compute_2dsurfaces_const_rho(eq_index,params): ## computes for a fixed equilibrium, across all 2d attributes
    eq = params.eq_loaded[eq_index]
    params.grid_const_rho_args['NFP'] = eq.NFP
    rho_grid = np.linspace(0,1,params.surf2d_num_rho+1)
    fig_list_json_A = []
    for q in params.attrs_2d:
        fig_list_json_B = []
        for i in range(0,params.surf2d_num_rho+1):
            params.grid_const_rho_args['rho'] = np.array([rho_grid[i]])
            grid = LinearGrid(**params.grid_const_rho_args)

            try:
                fig,_,data = plot_2d(eq, q, grid = grid, return_data=True)
                data = data[q]
                plt.close(fig)
            except:
                data=None

            fig_list_json_B.append(plotly.io.to_json(plotly_plot_2dsurf_const_rho(data, q, i, params)))
        fig_list_json_A.append(fig_list_json_B)
    return fig_list_json_A


def compute_2dsurfaces_const_phi(eq_index,params):
    eq = params.eq_loaded[eq_index]

    fig_list_json_A = []
    for q in params.attrs_2d:
        fig_list_json_B = []

        try:
            fig,_,data = plot_section(eq,q, phi = params.surf2d_num_phi, return_data=True)
            plt.close(fig)
            for i in range(0,params.surf2d_num_phi):
                xdata = data['R'][:,:,i]
                ydata = data['Z'][:,:,i]
                zdata = data[q][:,:,i]
                fig_list_json_B.append(plotly.io.to_json(plotly_plot_2dsurf_const_phi(xdata,ydata,zdata,q,i, eq.NFP, params)))
        except:
            for i in range(0,params.surf2d_num_phi):
                fig_empty = go.Figure()
                fig_list_json_B.append(plotly.io.to_json(fig_empty))

        fig_list_json_A.append(fig_list_json_B)

    return fig_list_json_A

    
def compute_3dsurfaces(eq_index,params):
    eq = params.eq_loaded[eq_index]
    params.grid_3d_args['N'] = int(50 * eq.NFP)

    rho_grid = np.linspace(0,1,params.surf3d_num_rho+1)

    fig_list_json_A = []
    for q in params.attrs_3d:
        fig_list_json_B = []
        for i in range(0,params.surf3d_num_rho+1):
            params.grid_3d_args['rho'] = np.array([rho_grid[i]])
            grid = LinearGrid(**params.grid_3d_args)

            try:
                fig = plotly_plot_3dsurf(plot_3d(eq, q, grid=grid), q, i, params)
            except:
                fig = go.Figure()

            fig_list_json_B.append(plotly.io.to_json(fig))

        fig_list_json_A.append(fig_list_json_B)

    return fig_list_json_A


def write_json(eq_index, data_array, figure_list, params):
    dest_filename = os.path.join(params.pp_desc_path, 'pp_' + params.eq_names_list[eq_index]+'.json')
    data_collected = [params.attrs_label_dict, data_array, figure_list]
    with gzip.open(dest_filename, 'wt') as f:
         json.dump(data_collected,f)

def build_label_dict(params):
    p = _parse_parameterization(params.eq_loaded[0])
    for q in params.attrs:
        if q not in params.attrs_label_dict:
            params.attrs_label_dict[q] = data_index[p][q]["label"]


###################################
if __name__ == '__main__':
    precompute()

    