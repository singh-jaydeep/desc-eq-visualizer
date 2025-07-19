from dataclasses import dataclass, field
from desc.grid import LinearGrid
import constants as c


@dataclass
class Params:

    #### Various lists which will be filled out after instantiation
    attrs_scalars: list = field(default_factory=list)
    attrs_profiles: list = field(default_factory=list)
    attrs_2d: list = field(default_factory=list)
    attrs_3d: list = field(default_factory=list)
    attrs_mag_axis: list = field(default_factory=list)

    attrs_dict: dict = field(default_factory=dict)

    meshes_loaded: list = field(default_factory=list)
    cached_figures: dict = field(default_factory=dict)

    #### Paths to the folders which contain the base DESC output and
    #### preprocessed files, respectively
    base_desc_path: str = field(default_factory=str)
    pp_desc_path: str = field(default_factory=str)

    #### Lists of Equilibria objects and names for referring to them
    eq_loaded: list = field(default_factory=list)  ## list of Equilbrium objects
    eq_names_list: list = field(default_factory=list)  ## for displaying on the dropdown

    #### Grid for 1D profiles
    grid_profiles = LinearGrid(20, 0, 0, 1)

    #### Grid for 2D plots
    grid_const_rho_args = {
        "sym": False,
        "axis": False,
        "endpoint": True,
        "M": 33,
        "N": 33,
    }

    #### Grid for 3D plots
    grid_3d_args = {"M": 50, "NFP": 1, "endpoint": True}

    #### See constants.py for further explanation
    fx_num_rho: int = field(default_factory=int)
    fx_num_theta: int = field(default_factory=int)
    fx_num_phi: int = field(default_factory=int)
    surf2d_num_rho: int = field(default_factory=int)
    surf2d_num_phi: int = field(default_factory=int)
    surf3d_num_rho: int = field(default_factory=int)

    ## Loading in quantities from constants.py
    def __post_init__(self):
        self.attrs_scalars = c.attrs_scalars
        self.attrs_profiles = c.attrs_profiles
        self.attrs_2d = c.attrs_2d
        self.attrs_3d = [
            "1"
        ] + c.attrs_3d  ## Adding in variable corresponding to flux surfaces
        self.attrs_mag_axis = c.attrs_mag_axis
        self.base_desc_path = c.base_desc_path
        self.pp_desc_path = c.pp_desc_path
        self.fx_num_rho = c.fx_num_rho
        self.fx_num_theta = c.fx_num_theta
        self.fx_num_phi = c.fx_num_phi
        self.surf2d_num_rho = c.surf2d_num_rho
        self.surf2d_num_phi = c.surf2d_num_phi
        self.surf3d_num_rho = c.surf3d_num_rho
