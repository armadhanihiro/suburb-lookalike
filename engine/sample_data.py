"""Sample/placeholder data for UI development and testing."""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def get_sample_suburbs():
    """
    Create sample suburb data for UI skeleton testing.
    
    Returns:
        tuple: (df, X, scaler) matching the structure of load_suburb_data
    """
    suburbs_data = {
        "sa2_code": [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
        "sa2_name": [
            "Carlton",
            "Fitzroy",
            "Newtown",
            "West End",
            "Northcote",
            "Brunswick",
            "Collingwood",
            "Abbotsford",
        ],
        "state": ["VIC", "VIC", "NSW", "QLD", "VIC", "VIC", "VIC", "VIC"],
        "kpi_1_val": [78, 82, 75, 71, 79, 76, 81, 77],
        "kpi_2_val": [65, 68, 62, 59, 66, 61, 69, 64],
        "kpi_3_val": [88, 91, 85, 80, 89, 84, 92, 87],
        "kpi_4_val": [52, 55, 50, 48, 53, 49, 56, 51],
        "kpi_5_val": [72, 75, 70, 68, 73, 69, 76, 71],
        "kpi_6_val": [41, 44, 39, 37, 42, 38, 45, 40],
        "kpi_7_val": [83, 86, 81, 79, 84, 80, 87, 82],
        "kpi_8_val": [57, 60, 55, 53, 58, 54, 61, 56],
        "kpi_9_val": [69, 72, 67, 65, 70, 66, 73, 68],
        "kpi_10_val": [48, 51, 46, 44, 49, 45, 52, 47],
    }
    
    df = pd.DataFrame(suburbs_data)
    
    kpi_cols = [f"kpi_{i}_val" for i in range(1, 11)]
    scaler = StandardScaler()
    X = scaler.fit_transform(df[kpi_cols])
    
    return df, X, scaler
