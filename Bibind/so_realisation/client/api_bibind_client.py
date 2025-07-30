"""Client used to notify the Bibind API of progress."""

import httpx


async def notify(status: str) -> None:
    """Send status update to the Bibind API."""
    async with httpx.AsyncClient() as client:
        await client.post("http://apibibind/notify", json={"status": status})
