import desc
from desc.equilibrium import Equilibrium
from desc.grid import LinearGrid
import numpy as np
from desc.plotting import plot_2d, plot_section, plot_3d
import plotly.graph_objects as go
import plotly

import matplotlib.pyplot as plt

eq = desc.io.load('equilibria/base_desc_outputs/eq_tok_eps_0.4.h5')

fig,data = plot_3d(eq, 'J^rho', return_data=True)
print(data.keys())
print(np.shape(data['X']))
print(np.shape(data['Y']))
fig.show()

