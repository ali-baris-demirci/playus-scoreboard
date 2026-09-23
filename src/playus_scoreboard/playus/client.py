from typing import Any

import httpx

from playus_scoreboard.config import Settings


class PlayusClient:
    """HTTP client for authenticated Playus backend access."""

    def __init__(
        self,
        settings: Settings,
        client: httpx.Client | None = None,
    ) -> None:
        self.settings = settings
        self._client = client or httpx.Client(
            base_url=settings.playus_firebase_database_url.rstrip("/") + "/",
            timeout=10.0,
        )

    def close(self) -> None:
        """Close the underlying HTTP client."""

        self._client.close()

    def __enter__(self) -> "PlayusClient":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def probe_database(self) -> httpx.Response:
        """Probe the Firebase root without authentication.

        This is diagnostic only. It does not assume that anonymous
        database access is permitted.
        """

        return self._client.get(".json")
