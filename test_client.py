import asyncio
import json

from fastmcp.client import MCPClient


async def main():
    """Connects to the MCP server and executes a SPARQL query."""
    client = MCPClient()
    # Assumes the server is running and listening on the default port
    await client.start()

    print("MCP Client connected.")

    # The SPARQL query from the project plan
    query = "SELECT ?s ?p ?o WHERE {?s ?p ?o} LIMIT 10"

    print(f"Executing tool 'execute_sparql' with query:\n{query}\n")

    try:
        result = await client.execute_tool("execute_sparql", {"query": query})
        print("--- Server Response ---")
        print(json.dumps(result, indent=2))
        print("-----------------------")

        if result and "error" not in result:
            print("\n✅ Test successful: Received a valid response from the server.")
        else:
            print(f"\n❌ Test failed: Server returned an error: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"\n❌ An error occurred while executing the tool: {e}")
    finally:
        await client.stop()
        print("\nMCP Client disconnected.")


if __name__ == "__main__":
    asyncio.run(main())