import desc
import os
import h5py
from params import viz_params
from desc.grid import LinearGrid




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


def paths_list(params):
    for item in os.listdir(params.base_desc_path):
        if not os.path.exists(os.path.join(params.pp_desc_path, 'pp_'+item)):
            input_path = os.path.join(params.base_desc_path,item)
            params.eq_loaded.append(desc.io.load(input_path)) ##! Will be a problem with equilibrium families
            params.pp_desc_filelist.append(os.path.join(params.pp_desc_path, 'pp_'+item))


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
    dest_filename = params.pp_desc_filelist[eq_index]
    f = h5py.File(dest_filename, 'w')
    f.create_dataset('data_array_scalars', data=data_array_scalars)
    f.create_dataset('data_array_profiles', data=data_array_profiles)




###################################
if __name__ == '__main__':
    precompute()

    