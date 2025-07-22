import os
from unittest.mock import MagicMock

import httpx
import pytest
import pytest_asyncio
import respx

from spendcast_mcp.server import ToolContext, execute_sparql, get_config

# Mock GraphDB URL for testing
TEST_GRAPHDB_URL = "http://test-graphdb:7200/repositories/test"


@pytest.fixture
def mock_env():
    """Fixture to set environment variables for tests."""
    os.environ["GRAPHDB_URL"] = TEST_GRAPHDB_URL
    yield
    del os.environ["GRAPHDB_URL"]


def test_get_config_success(mock_env):
    """Test that get_config successfully loads the URL from the environment."""
    config = get_config()
    assert config.url == TEST_GRAPHDB_URL


def test_get_config_missing_variable():
    """Test that get_config raises ValueError if the env var is not set."""
    if "GRAPHDB_URL" in os.environ:
        del os.environ["GRAPHDB_URL"]
    with pytest.raises(ValueError, match="GRAPHDB_URL environment variable not set."):
        get_config()


@pytest_asyncio.fixture
async def mocked_sparql_endpoint():
    """Respx fixture to mock the GraphDB SPARQL endpoint."""
    async with respx.mock(base_url=TEST_GRAPHDB_URL) as mock:
        yield mock


@pytest.mark.asyncio
async def test_execute_sparql_success(mock_env, mocked_sparql_endpoint):
    """Test a successful SPARQL query execution."""
    mock_response_data = {
        "head": {"vars": ["s", "p", "o"]},
        "results": {
            "bindings": [{"s": {"type": "uri", "value": "http://example.com/s"}}]
        },
    }
    mocked_sparql_endpoint.post(url=TEST_GRAPHDB_URL).mock(
        return_value=httpx.Response(200, json=mock_response_data)
    )

    mock_ctx = MagicMock(spec=ToolContext)
    query = "SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 1"

    result = await execute_sparql(mock_ctx, query)

    assert result == mock_response_data
    assert mocked_sparql_endpoint.calls.call_count == 1
    request = mocked_sparql_endpoint.calls.last.request
    assert request.content == b"query=SELECT+%3Fs+%3Fp+%3Fo+WHERE+%7B%3Fs+%3Fp+%3Fo%7D+LIMIT+1"


@pytest.mark.asyncio
async def test_execute_sparql_http_error(mock_env, mocked_sparql_endpoint):
    """Test handling of an HTTP status error from GraphDB."""
    mocked_sparql_endpoint.post(url=TEST_GRAPHDB_URL).mock(
        return_value=httpx.Response(500, text="Internal Server Error")
    )
    mock_ctx = MagicMock(spec=ToolContext)
    result = await execute_sparql(mock_ctx, "SELECT ?s")
    assert "error" in result
    assert "500" in result["error"]


@pytest.mark.asyncio
async def test_execute_sparql_request_error(mock_env, mocked_sparql_endpoint):
    """Test handling of a network request error."""
    mocked_sparql_endpoint.post(url=TEST_GRAPHDB_URL).mock(side_effect=httpx.ConnectError("Connection failed"))
    mock_ctx = MagicMock(spec=ToolContext)
    result = await execute_sparql(mock_ctx, "SELECT ?s")
    assert "error" in result
    assert "Connection failed" in result["error"]