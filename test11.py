import desc
from desc.equilibrium import Equilibrium, EquilibriaFamily
from desc.grid import LinearGrid
import numpy as np
from desc.plotting import plot_2d, plot_section, plot_3d, plot_surfaces
import plotly.graph_objects as go
import plotly
import pandas as pd

import matplotlib.pyplot as plt
from scipy.interpolate import griddata

'''
x = np.linspace(-1,1,100)
y = np.linspace(-1,1,100)
a,b = np.meshgrid(x,y)
z = a
for i in range(0,100):
    for j in range(0,100):
        if x[i]**2 + y[j]**2 > .25:
            z[i][j] = np.nan
'''


eq = desc.io.load('equilibria/base_desc_outputs/eq_tok_eps_0.4.h5')
fig,_,data = plot_section(eq, 'J^rho', phi = 8, return_data=True)
xdata = data['R'][:,:,0].flatten()
ydata = data['Z'][:,:,0].flatten()
zdata = data['J^rho'][:,:,0].flatten()

xlow, xhigh = min(xdata), max(xdata)
ylow, yhigh = min(ydata), max(ydata)


xtarget = np.linspace(xlow,xhigh,100)
ytarget = np.linspace(ylow, yhigh,100)
targetX, targetY = np.meshgrid(xtarget, ytarget)

ztarget = griddata((xdata,ydata), zdata, (targetX, targetY) , method='linear')

fig0, _, data0 = plot_surfaces(eq, rho=[1.0], phi=[0.0], return_data = True)
plt.close(fig0)


fig = go.Figure(go.Heatmap(x=xtarget, y=ytarget, z= ztarget, colorscale='Viridis'))

fig00, _, data00 = plot_surfaces(eq, rho=[1.0], phi=2, return_data = True)
print(np.shape(data00['rho_R_coords']))


fig.add_trace(go.Scatter(
    x = data0['rho_R_coords'][:,0,0],
    y = data0['rho_Z_coords'][:,0,0],
    mode='lines',
    line=dict(color='black', width=2)
))


fig.show()
