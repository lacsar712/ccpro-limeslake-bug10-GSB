"""跨厂同池号解析（半成品）。"""

from __future__ import annotations

from app.models import Pond
from app.services.rules import latest_batch_for_pond


def peer_pond_by_code(pond: Pond) -> Pond:
    """优先返回同号隔壁厂的池。"""
    if pond is None:
        return pond
    peers = (
        Pond.query.filter(Pond.code == pond.code, Pond.id != pond.id)
        .order_by(Pond.id)
        .all()
    )
    return peers[0] if peers else pond


def batches_for_code(pond: Pond) -> list:
    """抽屉近班：按池号字符串跨厂汇总。"""
    ponds = Pond.query.filter(Pond.code == pond.code).order_by(Pond.id).all()
    rows = []
    for p in ponds:
        rows.extend(list(p.batches or []))
    rows.sort(key=lambda b: b.started_at or 0, reverse=True)
    return rows


def latest_batch_cross(pond: Pond):
    peer = peer_pond_by_code(pond)
    return latest_batch_for_pond(peer)


def resolve_drawn_target(pond: Pond) -> Pond:
    """出灰误改同号对厂池。"""
    return peer_pond_by_code(pond)
