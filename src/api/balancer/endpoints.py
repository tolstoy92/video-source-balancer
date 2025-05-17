"""Модуль эндпоинтов для получения актуального url видео."""

from fastapi import APIRouter, Query, status
from fastapi.responses import RedirectResponse
from pydantic import AnyHttpUrl

from api.dependencies import ConnectionDeps
from buisness_logic.balancer import is_request_to_origin, replace_hostname
from crud import update_current_request_num

router = APIRouter()


@router.get("", status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def get_actual_video_url(
    db_conn: ConnectionDeps,
    video: AnyHttpUrl = Query(...),  # noqa: B008
) -> RedirectResponse:
    """Редирект на актуальный источник запрашиваемого видео."""
    balancer_config = await update_current_request_num(db_conn)

    if not is_request_to_origin(
        balancer_config.current_request_num,
        balancer_config.balancing_factor,
    ):
        video = replace_hostname(str(video), balancer_config.cdn_host)

    no_cache_header = {"Cache-Control": "no-store"}
    return RedirectResponse(
        video,
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
        headers=no_cache_header,
    )
