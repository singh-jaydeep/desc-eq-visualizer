import plotly.graph_objects as go
import numpy as np
'''
# Non-uniform x and y
x = np.array([0.1, 0.4, 1.0, 2.0])
y = np.array([0.0, 1.5, 3.0])
x2d, y2d = np.meshgrid(x, y, indexing='ij')
z = np.sin(x2d**2 + y2d**2)  # shape (4, 3)

fig = go.Figure(data=[
    go.Surface(
        x=x2d,
        y=y2d,
        z=np.zeros_like(z),  # flatten the surface at z=0
        surfacecolor=z,      # color based on actual function value
        colorscale='Viridis',
        cmin=np.min(z),
        cmax=np.max(z),
        showscale=True
    )
])

# Optional: make it look top-down (like a 2D heatmap)
fig.update_layout(
    title="2D Density Map on Non-Uniform Grid",
)
fig.update_layout(
    scene_camera=dict(eye=dict(x=0., y=0., z=2.)),
    scene_dragmode=False,  # disables rotation but allows panning
    scene=dict(
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        zaxis=dict(visible=False)
    )
)

fig.show()'''

