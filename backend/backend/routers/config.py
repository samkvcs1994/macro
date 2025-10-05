"""Configuration endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import get_settings_dict
from ..db import get_session
from ..models import IndicesConfig
from ..schemas import ConfigResponse

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/", response_model=ConfigResponse)
def get_config(session: Session = Depends(get_session)) -> ConfigResponse:
    db_config = session.execute(select(IndicesConfig).order_by(IndicesConfig.id.desc())).scalars().first()
    if db_config:
        payload = ConfigResponse(
            zscore_window_months=db_config.zscore_window_months,
            weights_json=db_config.weights_json or {},
            rebase_date=db_config.rebase_date.isoformat() if db_config.rebase_date else None,
            index_scale=db_config.index_scale,
            index_multiplier=db_config.index_multiplier,
            use_fed_net=db_config.use_fed_net,
            step_hold_gli=db_config.step_hold_gli,
            smooth_ma_months=db_config.smooth_ma_months,
        )
        return payload

    cfg = get_settings_dict()
    return ConfigResponse(
        zscore_window_months=cfg["default_z_window"],
        weights_json=cfg["weights_json"],
        rebase_date=cfg["rebase_date"],
        index_scale=cfg["index_scale"],
        index_multiplier=cfg["index_multiplier"],
        use_fed_net=cfg["use_fed_net"],
        step_hold_gli=cfg["step_hold_gli"],
        smooth_ma_months=cfg["smooth_ma_months"],
    )
