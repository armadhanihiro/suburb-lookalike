import os
import importlib

import pytest

import app


def test_load_engine_uses_sample_when_bigquery_unavailable(monkeypatch, tmp_path):
    # Ensure BIGQUERY_AVAILABLE is False for this test
    monkeypatch.setattr(app, "BIGQUERY_AVAILABLE", False)
    # Ensure no credentials are present
    monkeypatch.delenv("GOOGLE_APPLICATION_CREDENTIALS", raising=False)

    df, X, data_source = app._load_engine_uncached()

    assert data_source == "Sample data"
    assert "display_name" in df.columns
    # basic sanity: at least one row and X shape matches
    assert len(df) > 0
    assert hasattr(X, "shape")
