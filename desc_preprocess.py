import desc
import os
import gzip, json
import h5py
from params import viz_params
from desc.grid import LinearGrid
import matplotlib.pyplot as plt
from desc.plotting import plot_surfaces
import plotly

from plotly_plotting import plotly_plot_surface 




def precompute():
    params = viz_params()
    paths_list(params)
    num_eq = len(params.eq_loaded)
    if num_eq == 0:
        print("No equilibria to preprocess")
        return
    else:
        print(f"{num_eq} equilibria to preprocess")
        for i in range(0, len(params.eq_loaded)):
            data_array = compute_quantities(i,params)
            write_hdf5(i,params,data_array)
            figure_list = compute_fluxsurfaces(i, params)
            write_figures_json(i,params,figure_list)


def paths_list(params):
    for item in os.listdir(params.base_desc_path):
        if not os.path.exists(os.path.join(params.pp_desc_path, 'pp_'+item)):
            input_path = os.path.join(params.base_desc_path,item)
            params.eq_loaded.append(desc.io.load(input_path)) ##! Will be a problem with equilibrium families
            params.eq_names_list.append(item.removesuffix('.h5'))


def compute_quantities(eq_index, params):
    eq = params.eq_loaded[eq_index]
    data_array_scalars = []
    for q in params.attrs[0]:
        data_array_scalars.append(eq.compute(q)[q])
    data_array_profiles=[] 
    grid_profiles = params.grid_profiles
    for q in params.attrs[1]:
        data_array_profiles.append(eq.compute(q, grid_profiles)[q])
    return [data_array_scalars, data_array_profiles]


def write_hdf5(eq_index,params,data_array):
    data_array_scalars,data_array_profiles = data_array[0], data_array[1]
    dest_filename = os.path.join(params.pp_desc_path, 'pp_' + params.eq_names_list[eq_index]+'.h5')
    f = h5py.File(dest_filename, 'w')
    f.create_dataset('data_array_scalars', data=data_array_scalars)
    f.create_dataset('data_array_profiles', data=data_array_profiles)



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
        fig_list_json.append(plotly.io.to_json(plotly_plot_surface(xdata1, ydata1, xdata2, ydata2, params)))

    return fig_list_json  


def write_figures_json(eq_index, params, figure_list):
    dest_filename = os.path.join(params.pp_desc_path, 'pp_' + params.eq_names_list[eq_index]+'.json')
    with gzip.open(dest_filename, 'wt') as f:
         json.dump(figure_list,f)




###################################
if __name__ == '__main__':
    precompute()

    