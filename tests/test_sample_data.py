import numpy as np
import pandas as pd

from engine.sample_data import get_sample_suburbs


def test_sample_suburbs_structure():
    """Verify sample data has the correct structure for UI development."""
    df, X, scaler = get_sample_suburbs()
    
    # Check dataframe
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 8
    assert "sa2_name" in df.columns
    assert "state" in df.columns
    
    # Check feature matrix
    assert isinstance(X, np.ndarray)
    assert X.shape[0] == 8
    assert X.shape[1] == 10  # 10 KPI columns
    
    # Check scaler
    assert scaler is not None
    assert hasattr(scaler, "transform")
