from dataclasses import dataclass, field
from desc.equilibrium import Equilibrium
from desc.grid import LinearGrid

@dataclass
class viz_params:
    attrs_scalars = ['<beta>_vol','<|grad(p)|>_vol']
    attrs_profiles= ['iota','<|B|>']
    attrs = [attrs_scalars, attrs_profiles]

    #### Grids used for computation
    grid_profiles = LinearGrid(20,0,0,1)

    #### Paths to the folders which contain the base DESC output and 
    #### preprocessed files, respectively
    base_desc_path: str = "equilibria/base_desc_outputs"
    pp_desc_path: str = "equilibria/preprocessed_desc_outputs"

    #### Listing of the files contained in the above folders
    base_desc_filelist: list = field(default_factory = list)
    pp_desc_filelist: list = field(default_factory = list)

    #### Lists of Equilibria objects and names for referring to them
    eq_loaded: list = field(default_factory = list)
    pp_eq_loaded: list = field(default_factory = list)
    eq_names_list: list = field(default_factory = list)


    
    
