from dataclasses import dataclass
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Kyiv")


@dataclass(frozen=True)
class SlotConfig:
    work_days: tuple[int, ...] = (0, 1, 2, 3, 4)  # пн-пт
    work_start: time = time(10, 0)
    work_end: time = time(19, 0)
    lesson_minutes: int = 60
    buffer_minutes: int = 15
    min_notice_hours: int = 3
    horizon_days: int = 14


def _overlaps(a_start: datetime, a_end: datetime, b_start: datetime, b_end: datetime) -> bool:
    return a_start < b_end and b_start < a_end


def generate_slots(
    busy: list[tuple[datetime, datetime]],
    now: datetime,
    cfg: SlotConfig = SlotConfig(),
) -> list[tuple[datetime, datetime]]:
    """Повертає вільні слоти. Усі datetime мають бути timezone-aware."""
    lesson = timedelta(minutes=cfg.lesson_minutes)
    buffer = timedelta(minutes=cfg.buffer_minutes)
    earliest = now + timedelta(hours=cfg.min_notice_hours)
    today = now.astimezone(TZ).date()

    slots = []
    for offset in range(cfg.horizon_days + 1):
        day = today + timedelta(days=offset)
        if day.weekday() not in cfg.work_days:
            continue
        start = datetime.combine(day, cfg.work_start, tzinfo=TZ)
        day_end = datetime.combine(day, cfg.work_end, tzinfo=TZ)
        while start + lesson <= day_end:
            end = start + lesson
            is_free = not any(
                _overlaps(start - buffer, end + buffer, b0, b1) for b0, b1 in busy
            )
            if start >= earliest and is_free:
                slots.append((start, end))
            start = end
    return slots