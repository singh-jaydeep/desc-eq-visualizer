import desc
import os
import sys
import time
import matplotlib.pyplot as plt
import math
import numpy as np
import h5py
from desc.equilibrium import EquilibriaFamily
from desc.grid import LinearGrid
from desc.plotting import plot_surfaces, plot_2d, plot_section, plot_3d
from desc.compute.utils import _parse_parameterization
from desc.compute import data_index
from scipy.interpolate import griddata
from matplotlib.path import Path
import plotly

import plotting.plot_building as pbuild
from params_class import Params
import constants as c
import file_io


#################################################
# Reads in files in equilibria/desc_files. For
# any 'X.h5' without a corresponding 'pp_X.h5'
# file in equilbria/preprocessed, the script 
# calls DESC's API to compute all the necessary 
# quantities. Also caches some figures. Writes
# the corresponding 'pp_X.h5' file. Note these files 
# can be fairly large, depending on the complexity 
# of the equilibrium, the number of quantities in 
# constants.py, and the number of toroidal/poloidal
# slices requested.
#################################################
def preprocess():
    params = Params()

    paths_list(params)
    num_eq = len(params.eq_loaded)

    if num_eq == 0:
        print("No equilibria to preprocess")
        return
    else:
        print(f"{num_eq} equilibria to preprocess")
        build_attrs_dict(params)

        ## Iterate over equilibria which need to be processed
        for i in range(0, len(params.eq_loaded)):
            start_time = time.perf_counter()

            eq = params.eq_loaded[i]

            dest_filename = os.path.join(
                params.pp_desc_path, "pp_" + params.eq_names_list[i] + ".h5"
            )
            f = h5py.File(dest_filename, "w")

            compute_scalars(eq, f, params)
            compute_1dprofiles(eq, f, params)

            gp_2d = f.create_group("2d")
            subgp_2d_constrho = gp_2d.create_group("constrho_2d_")
            subgp_2d_constphi_LCFS = gp_2d.create_group("constphi_2d_LCFS_")
            subgp_2dflux = gp_2d.create_group("fluxsurfaces_2d_")
            subgp_2d_constphi = gp_2d.create_group("constphi_2d_")

            fluxsurface_mask = compute_2dfluxsurfaces(
                eq, f, subgp_2d_constphi_LCFS, subgp_2dflux, subgp_2d_constphi, params
            )
            compute_2dprofiles(
                eq, f, subgp_2d_constphi, subgp_2d_constrho, fluxsurface_mask, params
            )

            gp_3d = f.create_group("3d")
            compute_3dmagneticaxis(eq, gp_3d, params)
            compute_3dprofiles(eq, f, gp_3d, i, params)

            ## Conclude
            end_time = time.perf_counter()
            tot_time = end_time - start_time
            print(f"Equilibrium {i+1} took {tot_time:.3f} seconds to process")


def compute_scalars(eq, file, params):
    gp_scalars = file.create_group("scalars")
    for q in params.attrs_scalars:
        computed = eq.compute(q)[q]
        gp_scalars.attrs[q + "_scalar_" + "_value_"] = computed.astype(np.float32)
        gp_scalars.attrs[q + "_scalar_" + "_label_"] = params.attrs_dict[q]["label"]
        gp_scalars.attrs[q + "_scalar_" + "_units_"] = params.attrs_dict[q]["units"]
        gp_scalars.attrs[q + "_scalar_" + "_description_"] = params.attrs_dict[q][
            "description"
        ]


def compute_1dprofiles(eq, file, params):
    gp_1d = file.create_group("1d")
    grid_profiles = params.grid_profiles
    for q in params.attrs_profiles:
        computed = eq.compute(q, grid_profiles)[q]
        dset_1d = gp_1d.create_dataset(
            q + "_1d_", data=computed.astype(np.float32), compression="gzip"
        )
        dset_1d.attrs["_label_"] = params.attrs_dict[q]["label"]
        dset_1d.attrs["_units_"] = params.attrs_dict[q]["units"]
        dset_1d.attrs["_description_"] = params.attrs_dict[q]["description"]

        if q == params.attrs_profiles[0]:
            fig = pbuild.plot_1d(computed[:], params.attrs_dict[q]["label"], params)
            file.create_dataset("cached_profile_1d_A", data=plotly.io.to_json(fig))
        if q == params.attrs_profiles[1]:
            fig = pbuild.plot_1d(computed[:], params.attrs_dict[q]["label"], params)
            file.create_dataset("cached_profile_1d_B", data=plotly.io.to_json(fig))


def compute_2dfluxsurfaces(eq, f, gp_constphi_LCFS, gp_2dflux, gp_2d_constphi, params):
    params.grid_const_rho_args["NFP"] = eq.NFP

    fig, _, data = plot_surfaces(
        eq, rho=[1.0], phi=params.surf2d_num_phi, return_data=True
    )
    plt.close(fig)

    xmax = -1 * math.inf  ## Useful parameters for plotting
    ymax = -1 * math.inf
    xmin = math.inf
    ymin = math.inf
    mask_LCFS_total = []

    for j in range(0, params.surf2d_num_phi):
        outerflux_xdata = data["rho_R_coords"][:, 0, j]
        outerflux_ydata = data["rho_Z_coords"][:, 0, j]
        data_LCFS = [
            outerflux_xdata.astype(np.float32),
            outerflux_ydata.astype(np.float32),
        ]

        xmax = max(xmax, np.max(data_LCFS[0]))
        ymax = max(ymax, np.max(data_LCFS[1]))
        xmin = min(xmin, np.min(data_LCFS[0]))
        ymin = min(ymin, np.min(data_LCFS[1]))

        dset_2dconstphi_LCFS = gp_constphi_LCFS.create_dataset(
            "constphi_2d_LCFS_" + rf"{j}/{params.surf2d_num_phi - 1}",
            data=data_LCFS,
            compression="gzip",
        )
        dset_2dconstphi_LCFS.attrs["_phi_curr_"] = round(
            2 / (params.surf2d_num_phi * eq.NFP) * j, 3
        )

        mask_LCFS_total.append(compute_mask(data_LCFS))

    fig, _, data = plot_surfaces(
        eq,
        rho=params.fx_num_rho,
        theta=params.fx_num_theta,
        phi=params.fx_num_phi,
        return_data=True,
    )
    plt.close(fig)

    xdiff = abs(xmax - xmin)
    ydiff = abs(ymax - ymin)
    xrange = [xmin - 0.2 * xdiff, xmax + 0.2 * xdiff]
    yrange = [ymin - 0.2 * ydiff, ymax + 0.2 * ydiff]

    gp_2dflux.attrs["xrange"] = xrange
    gp_2dflux.attrs["yrange"] = yrange
    gp_2d_constphi.attrs["xrange"] = xrange
    gp_2d_constphi.attrs["yrange"] = yrange

    for j in range(0, params.fx_num_phi):
        xdata1 = data["rho_R_coords"][:, :, j]
        ydata1 = data["rho_Z_coords"][:, :, j]
        xdata2 = data["vartheta_R_coords"][:, :, j].T
        ydata2 = data["vartheta_Z_coords"][:, :, j].T

        dset_2dflux_A = gp_2dflux.create_dataset(
            "rho_R" + "fluxsurfaces_2d_" + rf"{j}/{params.fx_num_phi-1}",
            data=xdata1.astype(np.float32),
            compression="gzip",
        )
        dset_2dflux_A.attrs["label"] = "Flux surface"
        dset_2dflux_A.attrs["phi_curr"] = np.round(
            2 * j / (params.fx_num_phi * eq.NFP), 3
        )

        dset_2dflux_B = gp_2dflux.create_dataset(
            "rho_Z" + "fluxsurfaces_2d_" + rf"{j}/{params.fx_num_phi-1}",
            data=ydata1.astype(np.float32),
            compression="gzip",
        )
        dset_2dflux_B.attrs["label"] = "Flux surface"
        dset_2dflux_B.attrs["phi_curr"] = np.round(
            2 * j / (params.fx_num_phi * eq.NFP), 3
        )

        dset_2dflux_C = gp_2dflux.create_dataset(
            "vartheta_R" + "fluxsurfaces_2d_" + rf"{j}/{params.fx_num_phi-1}",
            data=xdata2.astype(np.float32),
            compression="gzip",
        )
        dset_2dflux_C.attrs["label"] = "Flux surface"
        dset_2dflux_C.attrs["phi_curr"] = np.round(
            2 * j / (params.fx_num_phi * eq.NFP), 3
        )

        dset_2dflux_D = gp_2dflux.create_dataset(
            "vartheta_Z" + "fluxsurfaces_2d_" + rf"{j}/{params.fx_num_phi-1}",
            data=ydata2.astype(np.float32),
            compression="gzip",
        )
        dset_2dflux_D.attrs["label"] = "Flux surface"
        dset_2dflux_D.attrs["phi_curr"] = np.round(
            2 * j / (params.fx_num_phi * eq.NFP), 3
        )

        if j == 0:
            fig = pbuild.plot_fluxsurf(
                xdata1, ydata1, xdata2, ydata2, 0, params, xrange=xrange, yrange=yrange
            )
            f.create_dataset("cached_fluxsurfaces_2d_", data=plotly.io.to_json(fig))

    return mask_LCFS_total


def compute_2dprofiles(eq, f, gp_2d_constphi, gp_2d_constrho, fluxsurface_mask, params):
    rho_grid = np.linspace(0, 1, params.surf2d_num_rho + 1)
    for q in params.attrs_2d:
        ## First, constant rho
        for j in range(0, params.surf2d_num_rho + 1):
            params.grid_const_rho_args["rho"] = np.array([rho_grid[j]])
            grid = LinearGrid(**params.grid_const_rho_args)
            try:
                fig, _, data = plot_2d(eq, q, grid=grid, return_data=True)
                data = data[q]
                plt.close(fig)
            except:
                data = np.array([0.0])  ## trivial data

            dset_2dconstrho = gp_2d_constrho.create_dataset(
                q + "constrho_2d_" + rf"{j}/{params.surf2d_num_rho}",
                data=data.astype(np.float32),
                compression="gzip",
            )
            dset_2dconstrho.attrs["_label_"] = params.attrs_dict[q]["label"]
            dset_2dconstrho.attrs["_units_"] = params.attrs_dict[q]["units"]
            dset_2dconstrho.attrs["_description_"] = params.attrs_dict[q]["description"]
            dset_2dconstrho.attrs["_rho_curr_"] = round(
                1 / params.surf2d_num_rho * j, 3
            )

            if q == params.attrs_2d[0] and j == params.surf2d_num_rho:
                fig = pbuild.plot_2dsurf_const_rho(
                    data, params.attrs_dict[q]["label"], 1, params
                )
                f.create_dataset("cached_constrho_2d_", data=plotly.io.to_json(fig))

        ## Next, constant phi
        fig, _, data = plot_section(eq, q, phi=params.surf2d_num_phi, return_data=True)
        plt.close(fig)

        for j in range(0, params.surf2d_num_phi):
            xdata = data["R"][:, :, j].flatten()
            ydata = data["Z"][:, :, j].flatten()
            zdata = data[q][:, :, j].flatten()

            xlow, xhigh = min(xdata), max(xdata)
            ylow, yhigh = min(ydata), max(ydata)

            xtarget = np.linspace(xlow, xhigh, 100)
            ytarget = np.linspace(ylow, yhigh, 100)
            targetX, targetY = np.meshgrid(xtarget, ytarget)

            targetZ = griddata(
                (xdata, ydata), zdata, (targetX, targetY), method="linear"
            )
            targetZ = np.where(fluxsurface_mask[j], targetZ, np.nan)

            data_2d_ = [
                targetX.astype(np.float32),
                targetY.astype(np.float32),
                targetZ.astype(np.float32),
            ]

            dset_constphi_2d_ = gp_2d_constphi.create_dataset(
                q + "constphi_2d_" + rf"{j}/{params.surf2d_num_phi - 1}",
                data=data_2d_,
                compression="gzip",
            )
            dset_constphi_2d_.attrs["_label_"] = params.attrs_dict[q]["label"]
            dset_constphi_2d_.attrs["_units_"] = params.attrs_dict[q]["units"]
            dset_constphi_2d_.attrs["_description_"] = params.attrs_dict[q][
                "description"
            ]
            dset_constphi_2d_.attrs["_phi_curr_"] = round(
                2 / (params.surf2d_num_phi * eq.NFP) * j, 3
            )


def compute_3dmagneticaxis(eq, gp, params):
    subgp_3d_magaxis = gp.create_group("magaxis_3d_")
    n = 2 * eq.NFP + 40
    grid = LinearGrid(N=n)
    axis = eq.get_axis()

    def wrap_around(arr):
        assert len(arr) != 0
        return np.append(arr, [arr[0]])

    curve_data = [
        wrap_around(np.array(axis.compute(q, grid=grid)[q])).astype(np.float32)
        for q in ["X", "Y", "Z"] + params.attrs_mag_axis
    ]
    hovertemplate = "(x,y,z): (%{customdata[0]:.3f}, %{customdata[1]:.3f}, %{customdata[2]:.3f})<br>"
    for j in range(0, len(params.attrs_mag_axis)):
        hovertemplate += (
            params.attrs_mag_axis[j] + ": %{" + f"customdata[{3+j}]" + ":.3f}" + "<br>"
        )
    hovertemplate += "<extra></extra>"
    dset_3d_magaxis = subgp_3d_magaxis.create_dataset(
        "magaxis_3d_", data=curve_data, compression="gzip"
    )
    dset_3d_magaxis.attrs["hovertemplate"] = hovertemplate


def compute_3dprofiles(eq, f, gp, eq_index, params):
    subgp_3d_mesh = gp.create_group("mesh_3d_")
    subgp_3d_constrho = gp.create_group("constrho_3d_")

    params.grid_3d_args["N"] = int(50 * eq.NFP)
    rho_grid = np.linspace(0, 1, params.surf3d_num_rho + 1)
    for q in params.attrs_3d:
        for j in range(
            1, params.surf3d_num_rho + 1
        ):  ## Won't evaluate rho=0, i.e. the axis
            params.grid_3d_args["rho"] = np.array([rho_grid[j]])
            grid = LinearGrid(**params.grid_3d_args)
            fig, data_3d_ = plot_3d(eq, q, grid=grid, return_data=True)

            if q == "1":  ## Only store the mesh once
                data_mesh_3d_ = [
                    data_3d_["X"].astype(np.float32),
                    data_3d_["Y"].astype(np.float32),
                    data_3d_["Z"].astype(np.float32),
                ]
                dset_mesh_3d_ = subgp_3d_mesh.create_dataset(
                    "mesh_3d_" + rf"{j}/{params.surf3d_num_rho}",
                    data=data_mesh_3d_,
                    compression="gzip",
                )
                dset_mesh_3d_.attrs["_rho_curr_"] = round(
                    1 / params.surf3d_num_rho * j, 3
                )

                if j == params.surf3d_num_rho:
                    fig = pbuild.plot_3dsurf(
                        data_3d_[q],
                        data_mesh_3d_,
                        eq_index,
                        "1",
                        params.surf3d_num_rho,
                        params,
                        label_in=params.attrs_dict[q]["label"],
                        units_in=params.attrs_dict[q]["units"],
                    )
                    f.create_dataset(
                        "cached_fluxsurfaces_3d_", data=plotly.io.to_json(fig)
                    )

            dset_3d_constrho_ = subgp_3d_constrho.create_dataset(
                q + "constrho_3d_" + rf"{j}/{params.surf3d_num_rho}",
                data=data_3d_[q].astype(np.float32),
                compression="gzip",
            )
            dset_3d_constrho_.attrs["_label_"] = params.attrs_dict[q]["label"]
            dset_3d_constrho_.attrs["_units_"] = params.attrs_dict[q]["units"]
            dset_3d_constrho_.attrs["_description_"] = params.attrs_dict[q][
                "description"
            ]
            dset_3d_constrho_.attrs["_rho_curr_"] = round(
                1 / params.surf3d_num_rho * j, 3
            )


def paths_list(params):
    visible_files = []
    for item in os.listdir(params.base_desc_path):
        if not item.startswith("."):
            visible_files.append(item)

    for item in visible_files:
        if not os.path.exists(os.path.join(params.pp_desc_path, "pp_" + item)):
            input_path = os.path.join(params.base_desc_path, item)
            eq = desc.io.load(input_path)
            if isinstance(
                eq, EquilibriaFamily
            ):  ## If an equilibrium family, only take the final entry
                eq = eq[-1]

            params.eq_loaded.append(eq)
            params.eq_names_list.append(item.removesuffix(".h5"))


def build_attrs_dict(params):
    p = _parse_parameterization(params.eq_loaded[0])

    copy_keys = ["label", "units", "description"]
    attrs = (
        params.attrs_scalars + params.attrs_profiles + params.attrs_2d + params.attrs_3d
    )
    for q in attrs:
        if q not in params.attrs_dict and q != "1":
            params.attrs_dict[q] = {r: data_index[p][q][r] for r in copy_keys}
        elif q == "1":
            params.attrs_dict[q] = {
                "label": "flux surfaces",
                "units": "",
                "description": "flux surfaces",
            }


def compute_mask(data_LCFS):
    x = data_LCFS[0]
    y = data_LCFS[1]

    xlow, xhigh = min(x.flatten()), max(x.flatten())
    ylow, yhigh = min(y.flatten()), max(y.flatten())

    x_rect = np.linspace(xlow, xhigh, 100)
    y_rect = np.linspace(ylow, yhigh, 100)
    targetX, targetY = np.meshgrid(x_rect, y_rect)

    path = Path(np.array(data_LCFS).T)
    points = np.array([targetX.flatten(), targetY.flatten()]).T
    mask = path.contains_points(points).reshape(targetX.shape)

    return mask


#################################################
# Runtime
#################################################
if __name__ == "__main__":
    if len(sys.argv) > 1:
        arg0 = sys.argv[1]
        if arg0 == "--list":
            file_io.list_directory(c.pp_desc_path)
        elif arg0 == "--clear":
            file_io.clear_directory(c.pp_desc_path)
        elif arg0 == "--clear+":
            file_io.clear_directory(c.pp_desc_path)
            preprocess()
        else:
            print("Unrecognized argument")
    else:
        preprocess()
