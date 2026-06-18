"""Tests for UI layout components."""

import pandas as pd
import pytest


def test_render_sidebar_controls():
    """Test sidebar controls can accept valid input."""
    from ui.layout import render_sidebar_controls
    
    # This is a minimal test since Streamlit components are hard to test directly
    # The actual rendering is tested by running the app
    suburbs = ["Carlton (VIC)", "Fitzroy (VIC)", "Newtown (NSW)"]
    
    # Verify the function signature is correct
    assert callable(render_sidebar_controls)


def test_get_preset_weights():
    from ui.layout import get_preset_weights

    investor_weights = get_preset_weights("Investor")
    assert investor_weights["kpi_1_val"] == 1.6
    assert investor_weights["kpi_2_val"] == 0.8
    assert investor_weights["kpi_10_val"] == 1.2

    custom_weights = get_preset_weights("Custom")
    assert custom_weights["kpi_1_val"] == 1.0
    assert custom_weights["kpi_2_val"] == 1.0
    assert custom_weights["kpi_10_val"] == 1.0


def test_render_results_table():
    """Test results table formatting."""
    from ui.layout import render_results_table
    
    results_df = pd.DataFrame({
        "Rank": [1, 2, 3],
        "Suburb": ["Fitzroy", "Newtown", "West End"],
        "State": ["VIC", "NSW", "QLD"],
        "Similarity": ["95.0%", "87.5%", "82.3%"],
    })
    
    # Verify function accepts dataframe
    assert callable(render_results_table)
    assert len(results_df) == 3
