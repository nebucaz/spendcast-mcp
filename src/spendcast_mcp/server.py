import json
import logging
import os
from typing import Any, Dict

import httpx
from dotenv import load_dotenv
from fastmcp import Context, FastMCP
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# --- Configuration ---
class GraphDBConfig(BaseModel):
    """Configuration for the GraphDB connection."""

    url: str = Field(..., description="The URL of the GraphDB SPARQL endpoint.")


def get_config() -> GraphDBConfig:
    """Loads configuration from environment variables."""
    graphdb_url = os.getenv("GRAPHDB_URL")
    if not graphdb_url:
        logging.error("GRAPHDB_URL environment variable not set.")
        raise ValueError("GRAPHDB_URL environment variable not set.")
    return GraphDBConfig(url=graphdb_url)

mcp = FastMCP()

# --- Tool Definition ---
@mcp.tool()
async def execute_sparql(ctx: Context, query: str) -> Dict[str, Any]:
    """
    Executes a SPARQL query against the GraphDB instance.

    :param ctx: The tool context (unused in this implementation).
    :param query: The SPARQL query string to execute.
    :return: The JSON result from GraphDB or an error dictionary.
    """
    config = get_config()
    logging.info(f"Executing SPARQL query on {config.url}")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/sparql-results+json",
    }
    data = {"query": query}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                config.url, headers=headers, data=data, timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        error_msg = f"HTTP error occurred: {e.response.status_code} - {e.response.text}"
        logging.error(error_msg)
        return {"error": error_msg}
    except httpx.RequestError as e:
        error_msg = f"An error occurred while connecting to GraphDB: {e}"
        logging.error(error_msg)
        return {"error": error_msg}
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON response from GraphDB.")
        return {"error": "Invalid JSON response from GraphDB."}


# # --- Server Setup ---
# def main():
#     """Main function to set up and run the MCP server."""
#     load_dotenv()  # Load environment variables from .env file

#     get_config()  # Validate config on startup

#     mcp = FastMCP()
#     execute_sparql_tool = Tool(
#         name="execute_sparql",
#         description="Executes a SPARQL query against the Spendcast GraphDB.",
#         fn=execute_sparql,
#     )
#     mcp.register_tool(execute_sparql_tool)

#     logging.info("Starting Spendcast MCP server...")
#     asyncio.run(server.start())


if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    get_config()  # Validate config on startup

    mcp.run()
