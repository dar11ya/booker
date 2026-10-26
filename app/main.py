from datetime import datetime, timedelta, timezone

from fastapi import FastAPI

from app.calendar_service import get_busy, get_service
from app.slots import SlotConfig, generate_slots

app = FastAPI(title="Lesson Booker")
cfg = SlotConfig()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/slots")
def slots():
    now = datetime.now(timezone.utc)
    service = get_service()
    busy = get_busy(service, now, now + timedelta(days=cfg.horizon_days + 1))
    free = generate_slots(busy, now, cfg)
    return [{"start": s.isoformat(), "end": e.isoformat()} for s, e in free]