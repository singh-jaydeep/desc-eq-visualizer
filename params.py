from dataclasses import dataclass, field
from desc.equilibrium import Equilibrium
from desc.grid import LinearGrid

@dataclass
class viz_params:
    attrs_scalars = ['<beta>_vol','<|grad(p)|>_vol']
    attrs_profiles= ['iota','<|B|>']
    attrs_2d = ['B^rho', 'J^rho']
    attrs_3d = []
    attrs = [attrs_scalars, attrs_profiles, attrs_2d, attrs_3d]
    attrs_label_dict: dict = field(default_factory = dict)

    #### Quantities used for 1D profiles
    grid_profiles = LinearGrid(20,0,0,1)

    #### Quantities used for flux surfaces
    fx_num_rho = 8
    fx_num_theta = 8
    fx_num_phi = 12

    #### Quantities used for 2D plots
    
    grid_const_rho_args = {
       # "NFP": eq_tok.NFP,
        "sym": False,
        "axis": False,
        "endpoint": True,
        "M": 33, 
        "N": 33,
        #"rho": np.array([1.0])
    }
    surf2d_num_rho = 6
    surf2d_num_phi = 8




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


    
    
