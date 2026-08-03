import csv
import io
import json

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from ..db import models
from ..db.session import get_db

router = APIRouter(prefix="/uploads", tags=["uploads"])
MAX_UPLOAD_BYTES = 5 * 1024 * 1024


@router.post("/activity")
async def upload_activity(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filename = file.filename or "upload"
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the 5 MB limit")

    try:
        if filename.lower().endswith(".json"):
            data = json.loads(content)
        elif filename.lower().endswith(".csv"):
            reader = csv.DictReader(io.StringIO(content.decode("utf-8")))
            data = list(reader)
        else:
            raise HTTPException(
                status_code=400,
                detail="Only JSON and CSV files are supported",
            )
    except (UnicodeDecodeError, json.JSONDecodeError, csv.Error) as exc:
        raise HTTPException(status_code=400, detail="Invalid upload data") from exc

    upload = models.UploadedActivity(filename=filename, data=data)
    db.add(upload)
    db.commit()
    db.refresh(upload)
    return {
        "message": "File uploaded successfully",
        "id": upload.id,
        "rows": len(data) if isinstance(data, list) else 1,
    }

