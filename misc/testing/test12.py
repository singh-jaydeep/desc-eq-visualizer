 
import h5py


file_path = "equilibria/preprocessed_desc_outputs/pp_eq_tok_eps_0.4.h5"

with h5py.File(file_path,'r') as f:
        data_scalars = f['scalars']
        print("type:", type(data_scalars))
        print("repr:", repr(data_scalars))

# for k in data_scalars.attrs:
#     print(f"{repr(k)} — type: {type(k)}")