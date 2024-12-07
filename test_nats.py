import pytest
import nats
import asyncio
from testcontainers.nats import NatsContainer


@pytest.mark.asyncio
async def test_nats():
    with NatsContainer() as nats_container:
        nats_url = nats_container.nats_uri()

        nc = await nats.connect(nats_url)
        assert nc.is_connected
        messages = []

        async def message_handler(msg):
            messages.append(msg.data.decode())

        await nc.subscribe("test_subject", cb=message_handler)
        await nc.publish("test_subject", b"Hello, NATS!")
        await asyncio.sleep(1)
        assert "Hello, NATS!" in messages
        await nc.close()
