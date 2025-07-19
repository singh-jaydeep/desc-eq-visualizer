import numpy as np


def display_number(val):
    if isinstance(val, (int, np.float32, np.float64)):
        val = val.astype(float)

    val_str = ""
    if isinstance(val, float) and abs(val) >= 1000:
        val_str = f"{val:.3e}"
    elif isinstance(val, float):
        val_str = f"{val:.3f}"
    else:
        val_str = str(val)
    return val_str
