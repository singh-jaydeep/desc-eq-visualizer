import desc
from desc.compute import data_index
from desc.equilibrium import Equilibrium
from desc.compute.utils import _parse_parameterization




eq = desc.io.load('equilibria/base_desc_outputs/eq_tok_eps_0.4.h5')
p = _parse_parameterization(eq)
print(data_index[p]['<|B|>']["label"])
