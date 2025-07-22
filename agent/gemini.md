# Gemini Code Assist
This file provides guidance to Gemini Code Assist when working with code in this repository.

## Quick Start for New Sessions

Before starting any work, read these files in order:
- pair_programming.md - Our workflow process for story-driven development
- project_plan_{some_extension}.md - Current progress and next story to work on
- technical_considerations.md - Lessons learned and implementation decisions

## Overview
Spendcast-mcp is a Model Context Protocol (MCP) server that enables connections and access to a triple-store (GraphDB). It functions similarly to Wikidata-MCT, allowing llm chattbots to access and query the triple store using SPARQL queries.

## Development Commands
This is a python project that uses `uv`as the package manager.

### Package Management
- Uses uv as the package manager (not pip)
- Lock file: uv.lock

### Install Dependencies 
Install dependencies using uv:
```bash
uv sync
```

### Install Additional Dependencies
```bash
uv add <dependency_name>
```

## Architecture Overview
Technology Stack
 - Python 
 - MCP Integration: fastmcp, pydantic, httpx.AsyncClient()
    
Implementation Status: ✅ Complete - Direct process management, universal command support, enhanced error messaging, JSON-RPC protocol, process lifecycle management, and tool execution all working.

## Project Structure Overview

See mcp-browser-architecture.md for detailed component organization. Key locations:

    src/ - Python mcp server-files
    test/ - Python unittests

## Appendix: What is MCP?

The Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to Large Language Models (LLMs). Think of MCP like a USB-C port for AI applications - just as USB-C provides a standardized way to connect devices to various peripherals, MCP provides a standardized way to connect AI models to different data sources and tools.
Key MCP Concepts:

MCP Servers are lightweight programs that expose specific capabilities (tools, prompts, and resources) through the protocol. For example, a Git MCP server might expose tools like git_status, git_commit, and git_diff that an LLM can call.

MCP Clients are applications (like Claude Desktop or IDEs) that connect to MCP servers to access their capabilities. They maintain 1:1 connections with servers.

Core Primitives:
 - Resources: Data and content that servers expose (files, documents, live data)
 - Tools: Functions that LLMs can execute through the server (API calls, system commands, calculations)
 - Prompts: Reusable prompt templates and workflows
 - Sampling: Allows servers to request LLM completions

Transport Layers: MCP supports multiple transport mechanisms:
 - stdio: Communication through standard input/output (for local processes)
 - SSE (Server-Sent Events): For HTTP-based connections
 - WebSocket: For bidirectional streaming (planned)

The protocol enables LLMs to interact with external systems in a controlled, secure way while maintaining clear boundaries between the AI model and the tools/data it accesses. This standardization means developers can write MCP servers once and have them work with any MCP-compatible client, similar to how REST APIs work with any HTTP client

