"""Модуль логики приложения."""

from httpx import URL


def is_request_to_origin(current_request_num: int, balancing_factor: int) -> bool:
    """Определяет, необходимо ли перенаправлять запрос на cdn.

    Можно было реализовать свойство в классе BalancerSettings, но лучше разделить
    логику от статичных данных.

    Args:
        current_request_num (int): Номер текущего запроса
        balancing_factor (int): Коэффициент редиректов

    Returns:
        bool - Должен ли текущий запрос отправляться на origin-сервер

    Raises:
        ValueError - Если balancing_factor < 1

    """
    if balancing_factor < 1:
        msg = "Коэффициент балансировки не может быть меньше 1."
        raise ValueError(msg)
    return current_request_num % balancing_factor == 0


def replace_hostname(url: str, new_host: str) -> str:
    """Замена исходного хоста на новый.

    Args:
        url (str): Исходный URL, в котором нужно заменить хост.
        new_host (str): Новый хост, который будет установлен.

    Returns:
        str: Новый URL с заменённым хостом.

    """
    new_url = URL(url).copy_with(host=new_host)
    return str(new_url)
