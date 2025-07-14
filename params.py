from dataclasses import dataclass, field
from desc.grid import LinearGrid
import plottable as pl

@dataclass
class viz_params:

    #### Various lists which will be filled out after instantiation
    attrs_scalars: list = field(default_factory = list)
    attrs_profiles: list = field(default_factory = list)
    attrs_2d: list = field(default_factory = list)
    attrs_3d: list = field(default_factory = list) 
    attrs_mag_axis: list = field(default_factory = list) 

    attrs_dict: dict = field(default_factory = dict)

    meshes_loaded: list = field(default_factory = list)
    cached_figures: dict = field(default_factory = dict)

    #### Paths to the folders which contain the base DESC output and 
    #### preprocessed files, respectively
    base_desc_path: str = "equilibria/base_desc_outputs"
    pp_desc_path: str = "equilibria/preprocessed_desc_outputs"

    #### Listing of the files contained in the above folder
    base_desc_filelist: list = field(default_factory = list)

    #### Lists of Equilibria objects and names for referring to them
    eq_loaded: list = field(default_factory = list) ## list of Equilbrium objects
    pp_eq_loaded: list = field(default_factory = list) ## list of dictionaries, one per Equilibrium object
    eq_names_list: list = field(default_factory = list) ## for displaying on the dropdown


    #### Quantities used for 1D profiles
    grid_profiles = LinearGrid(20,0,0,1)

    #### Quantities used for 2D flux surfaces
    fx_num_rho = 8
    fx_num_theta = 8
    fx_num_phi = 12

    #### Quantities used for 2D plots
    grid_const_rho_args = {
        "sym": False,
        "axis": False,
        "endpoint": True,
        "M": 33, 
        "N": 33,
    }
    surf2d_num_rho = 6
    surf2d_num_phi = 8


    #### Quantities used for 3D plots
    grid_3d_args = {
        "M": 50, 
        "NFP": 1, 
        "endpoint": True
    }
    surf3d_num_rho = 6
    



    ## Loading in quantities for plotting. see plottable.py
    def __post_init__(self):
       self.attrs_scalars = pl.attrs_scalars
       self.attrs_profiles = pl.attrs_profiles
       self.attrs_2d = pl.attrs_2d
       self.attrs_3d = ['1'] + pl.attrs_3d ## Adding in variable corresponding to flux surfaces
       self.attrs_mag_axis = pl.attrs_mag_axis

    
    
