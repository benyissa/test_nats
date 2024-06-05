import os

import pytest
import nats
import asyncio


@pytest.mark.asyncio
async def test_nats():
    # Connect to the NATS server
    nats_url = os.getenv('NATS_SERVER', 'nats://localhost:4222')
    nc = await nats.connect(nats_url)
    assert nc.is_connected

    # Callback function to handle messages
    messages = []

    async def message_handler(msg):
        messages.append(msg.data.decode())

    # Subscribe to a subject
    await nc.subscribe("test_subject", cb=message_handler)

    # Publish a message
    await nc.publish("test_subject", b"Hello, NATS!")

    # Give some time for the message to be processed
    await asyncio.sleep(1)

    # Check if the message was received
    assert "Hello, NATS!" in messages

    await nc.close()
