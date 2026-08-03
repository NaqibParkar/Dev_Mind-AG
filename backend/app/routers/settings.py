from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..db.session import get_db

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=schemas.AppSettings)
def read_settings(db: Session = Depends(get_db)):
    settings = crud.get_settings(db)
    if not settings:
        raise HTTPException(status_code=404, detail="Settings not found")
    return {
        "id": settings.id,
        "smartBreaks": settings.smart_breaks,
        "comparativeMode": settings.comparative_mode,
        "reflectionJournal": settings.reflection_journal,
        "passiveMode": settings.passive_mode,
        "alerts": {
            "enabled": True,
            "sensitivity": settings.alert_sensitivity,
            "types": {
                "burnout": settings.alert_burnout,
                "focusDrop": settings.alert_focus_drop,
                "contextSwitching": settings.alert_context_switching,
                "prolongedWork": settings.alert_prolonged_work,
            },
        },
    }


@router.put("", response_model=schemas.AppSettings)
def update_settings(
    settings: schemas.AppSettingsBase,
    db: Session = Depends(get_db),
):
    return crud.update_settings(db=db, settings=settings)

