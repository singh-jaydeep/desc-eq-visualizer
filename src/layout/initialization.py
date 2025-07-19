import os
import desc
import h5py
from plotly.io import from_json
from desc.equilibrium import EquilibriaFamily

import file_io


def initialize(params):
    print("initializing")

    visible_files = file_io.visible_files(params.base_desc_path)

    for item in visible_files:
        desc_path = os.path.join(params.base_desc_path, item)
        params.eq_names_list.append(item)
        eq = desc.io.load(desc_path)
        if isinstance(eq, EquilibriaFamily):
            eq = eq[-1]
        params.eq_loaded.append(eq)  ## loading the equilibrium via DESC

    load_meshes(0, params)
    load_cached_figures(0, params)


def load_meshes(eq_index, params):
    with h5py.File(
        params.pp_desc_path + "/pp_" + params.eq_names_list[eq_index], "r"
    ) as f:
        mesh_data = f["3d/mesh_3d_"]
        params.meshes_loaded = [
            mesh_data["mesh_3d_" + rf"{j}/{params.surf3d_num_rho}"][:]
            for j in range(1, params.surf3d_num_rho + 1)
        ]


def load_cached_figures(eq_index, params):
    with h5py.File(
        params.pp_desc_path + "/pp_" + params.eq_names_list[eq_index], "r"
    ) as f:
        params.cached_figures = {
            "profile_1d_A": from_json(f["cached_profile_1d_A"][()]),
            "profile_1d_B": from_json(f["cached_profile_1d_B"][()]),
            "fluxsurfaces_2d_": from_json(f["cached_fluxsurfaces_2d_"][()]),
            "constrho_2d_": from_json(f["cached_constrho_2d_"][()]),
            "fluxsurfaces_3d_": from_json(f["cached_fluxsurfaces_3d_"][()]),
        }


def reset_sliders(params):
    return [0, params.surf2d_num_rho, params.surf3d_num_rho - 1]


def reset_dropdowns(params):
    return [
        params.attrs_profiles[0],
        params.attrs_profiles[1],
        "const_rho",
        params.attrs_2d[0],
        params.attrs_3d[0],
    ]
