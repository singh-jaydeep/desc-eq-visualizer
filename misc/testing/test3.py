###### Paths dont work for this test as is. Copy to main directory


import h5py
from app_components import *
from params import viz_params


params = viz_params()
initialize(params)
print(params.pp_eq_loaded[0]['<beta>_vol'])
print(params.pp_eq_loaded[0]['iota'])

