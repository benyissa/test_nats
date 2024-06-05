import pytest
from testcontainers.nats import NatsContainer
import nats

@pytest.fixture(scope="module")
def nats_container():
    container = NatsContainer(image="nats:latest")
    container.start()
    yield container
    container.stop()

def test_nats(nats_container):
    # Connect to the NATS server
    nats_url = f"nats://{nats_container.get_container_host_ip()}:{nats_container.get_exposed_port(4222)}"
    nc = nats.connect(nats_url)
    assert nc.is_connected
    nc.close()

