from datetime import datetime

from app.slots import TZ, SlotConfig, generate_slots


def dt(y, m, d, h, mi=0):
    return datetime(y, m, d, h, mi, tzinfo=TZ)


def test_weekend_has_no_slots():
    cfg = SlotConfig(horizon_days=0)
    assert generate_slots([], now=dt(2026, 10, 31, 12), cfg=cfg) == []  # субота


def test_busy_interval_removes_slot():
    cfg = SlotConfig(horizon_days=0, buffer_minutes=0)
    busy = [(dt(2026, 11, 2, 14), dt(2026, 11, 2, 15))]
    starts = [s.hour for s, _ in generate_slots(busy, now=dt(2026, 11, 2, 6), cfg=cfg)]
    assert 14 not in starts
    assert 13 in starts and 15 in starts


def test_min_notice_hides_near_slots():
    cfg = SlotConfig(horizon_days=0)  # notice = 3 год
    slots = generate_slots([], now=dt(2026, 11, 2, 9), cfg=cfg)
    assert slots[0][0].hour == 12