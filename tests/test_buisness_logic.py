import pytest

from buisness_logic.balancer import is_request_to_origin, replace_hostname


@pytest.mark.parametrize(
    ("current_request_num", "balancing_factor", "result"),
    [
        (3, 3, True),
        (4, 3, False),
        (5, 1, True),
        (0, 2, True),
    ],
)
def test_is_request_to_origin(
    current_request_num: int,
    balancing_factor: int,
    result: bool,  # noqa: FBT001
) -> None:
    """Тест логики определения нужен редирект или нет."""
    assert is_request_to_origin(current_request_num, balancing_factor) is result


@pytest.mark.parametrize("balancing_factor", [0, -1])
def test_is_request_to_origin_failed_on_zero_balancing_factor(balancing_factor: int) -> None:
    """Тест на некорректное значение balancing_factor."""
    with pytest.raises(ValueError):  # noqa: PT011
        is_request_to_origin(1, balancing_factor)


@pytest.mark.parametrize(
    ("url", "new_host", "excepted_url"),
    [
        (
            "http://origin.com/video.mp4",
            "cdn.com",
            "http://cdn.com/video.mp4",
        ),
        (
            "http://origin.com/path/to/video?quality=high",
            "cdn.com",
            "http://cdn.com/path/to/video?quality=high",
        ),
    ],
)
def test_replace_hostname_simple(url: str, new_host: str, excepted_url: str) -> None:
    """Тест на замену хоста."""
    assert replace_hostname(url, new_host) == excepted_url
