"""
SNCF ARTIFICIAL DATA ANALYSIS

We propose here an analysis of the artificial data created with copilot 
(see data/synthetic/train_delays_synthetic_2025_2026.csv)

OBJECTIVE:
* analyse the propagation of delays over the train network
* identify the main factors influencing delays' occurence
* predict the delay of a train given its characteristics and the current state of the network 
"""


"""
PACKAGES
"""

import pandas as pd
import numpy as np







"""
DATA AND PATHS
"""

path_data = "data/synthetic/"

df = pd.read_parquet(path_data + "train_delays_synthetic_2025_2026.parquet")



"""
DESCRITPIVE STATISTICS
"""










