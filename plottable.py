
######### File contains all parameters which will be precomputed, and available to plot
######### Variables which are not included here, but are plottable, are '1' (flux surfaces)
######### in attrs_3d, and 'X', 'Y', 'Z' (spatial coordinates) in attrs_mag_axis
######### Can add additional quantities which are implemented in DESC

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