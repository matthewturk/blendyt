import numpy as np
import pandas as pd

df = pd.read_csv("orbits_exponential_0025.csv")

bodies = set(_.split("_")[0] for _ in df.columns if "_" in _)

for body in sorted(bodies):
    pos = np.stack([df[f"{body}_{ax}"] for ax in "xyz"]).T
    with open(f"{body}_orbit.obj", "w") as f:
        for p in pos:
            f.write(f"v {p[0]:0.8f} {p[1]:0.8f} {p[2]:0.8f} 1.0\n")
