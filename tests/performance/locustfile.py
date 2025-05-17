"""Модуль нагрузочного тестирования."""

# ruff: noqa: D101, D102
from locust import FastHttpUser, between, task


class GetVideoURLUser(FastHttpUser):
    wait_time = between(1, 2)

    @task
    def get_video_url(self) -> None:
        self.client.get("/balancer", params={"video": "http://example.com"})
