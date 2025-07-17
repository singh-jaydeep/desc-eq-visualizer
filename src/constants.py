
#####################################################
# Various quantities which the user can modify.
#####################################################





#####################################################
# Variables which are not included here, but are plottable, 
# are '1' (flux surfaces) in attrs_3d, and 'X', 'Y', 'Z' 
# (spatial coordinates) in attrs_mag_axis. Can add additional 
# quantities which are implemented in DESC
#####################################################
attrs_scalars = ['a', 
                 'R0', 
                 'R0/a',
                 '<beta>_vol',
                 '<|grad(p)|>_vol', 
                 '<|F|>_vol'] 

attrs_profiles= ['iota',
                 '<|B|>', 
                 '<J*B>', 
                 'p', 
                 'q']

attrs_2d = ['J^rho', 
            'B^theta', 
            'sqrt(g)', 
            '|B|']

attrs_3d = ['J^rho', 
            'B^theta', 
            'sqrt(g)', 
            '|B|']

attrs_mag_axis = ['curvature',
                  'torsion']



#####################################################
# Paths to the folders which contain the base DESC output 
# and preprocessed files, respectively
#####################################################
base_desc_path = "../equilibria/desc_files"
pp_desc_path = "../equilibria/preprocessed"



#####################################################
# Parameters used for plotting
#####################################################
fx_num_rho = 8  #2D flux surfaces, number of rho contours shown
fx_num_theta = 8 #2D flux surfaces, number of const. theta contours shown
fx_num_phi = 12 #2D flux surfaces, number of toroidal slices


surf2d_num_rho = 6 #2D (theta,phi) plots, number of flux surfaces
surf2d_num_phi = 8 #2D (rho, theta) plots, number of toroidal slices

surf3d_num_rho = 6 #3D, number of flux surfaces