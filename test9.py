import desc
from desc.equilibrium import Equilibrium
from desc.grid import LinearGrid
import numpy as np
from desc.plotting import plot_2d, plot_section, plot_3d
import plotly.graph_objects as go
import plotly
import pandas as pd

import matplotlib.pyplot as plt


def wrap_around(arr):
    assert len(arr) != 0 
    return np.append(arr, [arr[0]])

eq = desc.io.load('equilibria/base_desc_outputs/eq_tok_eps_0.4.h5')

axis = eq.get_axis()
grid = LinearGrid(N=40)

xdata,ydata,zdata = np.array(axis.compute('X', grid=grid)['X']), np.array(axis.compute('Y', grid=grid)['Y']), np.array(axis.compute('Z', grid=grid)['Z'])

xdata=np.append(xdata,[xdata[0]])
ydata=np.append(ydata,[ydata[0]])
zdata=np.append(zdata,[zdata[0]])


curvdata = wrap_around(np.array(axis.compute('curvature', grid=grid)['curvature']))


params_list=['X', 'Y', 'Z', 'curvature']
data = {q: wrap_around(np.array(axis.compute(q, grid=grid)[q])) for q in params_list}
df = pd.DataFrame(data)

fig=go.Figure(data=[go.Scatter3d(x=xdata,y=ydata,z=zdata, mode='lines')])

hovertemplate0 = '(x,y,z): (%{customdata[1]:.3f}, %{customdata[2]:.3f}, %{customdata[3]:.3f})<br>'
for i in ['curvature']:
    hovertemplate0 += i + '%{customdata[0]:.3f}' + '<br>'
hovertemplate = hovertemplate0 + '<extra></extra>'

#hovertemplate='(x,y,z): (%{customdata[1]:.3f}, %{customdata[2]:.3f}, %{customdata[3]:.3f})<br>' + 'Curvature: %{customdata[0]:.3f} <extra></extra>'

fig.update_traces(
    customdata=df[['curvature', 'X','Y','Z']],
    hovertemplate = hovertemplate
)
fig.update_layout(
    scene=dict(
        xaxis=dict(showbackground=True, showgrid=True, backgroundcolor='#2c3034',gridcolor='lightgray',color='white',zeroline=False),
        yaxis=dict(showbackground=True, showgrid=True, backgroundcolor='#2c3034',gridcolor='lightgray',color='white',zeroline=False),
        zaxis=dict(showbackground=True, showgrid=True, backgroundcolor='#2c3034',gridcolor='lightgray',color='white',zeroline=False)
    ), paper_bgcolor='#2c3034', plot_bgcolor='#2c3034'
)

fig.show()
