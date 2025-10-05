import pandas as pd

from backend.indices.compute_g4 import G4Config, G4Inputs, compute_g4_usd_level
from backend.indices.compute_gli_credit import CreditConfig, CreditInputs, compute_gli_credit_usd
from backend.indices.composite import blend_indices, scale_index
from backend.indices.standardize import zscore


def test_pipeline_smoke():
    idx = pd.date_range("2020-01-31", periods=24, freq="M")
    ones = pd.Series(1.0, index=idx)

    g4 = compute_g4_usd_level(G4Config(use_fed_net=False), G4Inputs(ones, ones, ones, ones, ones, ones))
    gli = compute_gli_credit_usd(CreditConfig(step_hold_gli=True), CreditInputs(ones, ones, ones))

    g4_z = zscore(g4 + pd.Series(range(24), index=idx), window_months=12)
    gli_z = zscore(gli + pd.Series(range(24), index=idx), window_months=12)

    composite = blend_indices({"GLI_G4_CB": g4_z, "GLI_Credit": gli_z}, {"GLI_G4_CB": 0.5, "GLI_Credit": 0.5})
    scaled = scale_index(composite)

    assert not scaled.isna().any()
